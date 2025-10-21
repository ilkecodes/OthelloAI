# api/brand_voice.py
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text as sat
import json
import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# ---- Flexible imports ----
try:
    from database import get_db
except ImportError:
    from app.database import get_db

try:
    from models.brand_voice_models import (
        BrandCorpus,
        BrandVoiceProfile,
        BrandEmbedding,
        GenOutput,
        Feedback,
    )
except ImportError:
    from app.models.brand_voice_models import (
        BrandCorpus,
        BrandVoiceProfile,
        BrandEmbedding,
        GenOutput,
        Feedback,
    )

try:
    from services.brand_voice_service import brand_voice_service
except ImportError:
    from app.services.brand_voice_service import brand_voice_service

# Instagram sync (optional)
instagram_sync = None
try:
    from agents.instagram_sync import instagram_sync as _ig_sync
    instagram_sync = _ig_sync
except Exception:
    try:
        from app.agents.instagram_sync import instagram_sync as _ig_sync
        instagram_sync = _ig_sync
    except Exception:
        instagram_sync = None


# ---- Schemas ----
class CorpusAdd(BaseModel):
    client_id: str
    source: str = "instagram"
    texts: List[Dict[str, Any]]


class BuildRequest(BaseModel):
    client_id: str
    texts: Optional[List[str]] = None


class GenerateRequest(BaseModel):
    client_id: str
    platform: str
    content_type: str
    topic: str
    goal: str


# ---- Helpers ----
def _ensure_profile(db: Session, client_id: str) -> Dict:
    row = (
        db.query(BrandVoiceProfile)
        .filter(BrandVoiceProfile.client_id == client_id)
        .first()
    )
    if not row or not row.profile:
        raise HTTPException(status_code=404, detail="Brand voice profile not found")
    return row.profile


# ---- Endpoints ----
@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "brand-voice"}


@router.post("/corpus")
def add_to_corpus(data: CorpusAdd, db: Session = Depends(get_db)):
    """Add content to brand corpus"""
    if not data.texts:
        raise HTTPException(status_code=400, detail="texts is empty")

    items: List[BrandCorpus] = []
    for item in data.texts:
        text_val = (item.get("text") or "").strip()
        if not text_val:
            continue
        corpus_item = BrandCorpus(
            client_id=data.client_id,
            source=data.source,
            text=text_val,
            url=item.get("url"),
            engagement_score=int(item.get("engagement_score") or 0),
        )
        db.add(corpus_item)
        items.append(corpus_item)
    
    try:
        db.commit()
    except Exception as e:
        logger.error(f"❌ Corpus commit error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    texts = [it.text for it in items]
    if texts:
        try:
            embeddings = brand_voice_service.embed_texts(texts)
            for it, emb in zip(items, embeddings):
                db.add(
                    BrandEmbedding(
                        client_id=data.client_id,
                        text=it.text,
                        source=data.source,
                        embedding=emb,
                    )
                )
            db.commit()
        except Exception as e:
            logger.error(f"❌ Embedding error: {e}")
            db.rollback()
            # Continue without embeddings

    return {
        "ok": True,
        "client_id": data.client_id,
        "inserted": len(items),
        "source": data.source,
    }


@router.post("/build")
def build_brand_voice(req: BuildRequest, db: Session = Depends(get_db)):
    """Build brand voice profile from corpus"""
    try:
        texts: List[str]
        if req.texts and len(req.texts) > 0:
            texts = req.texts
        else:
            rows = (
                db.query(BrandCorpus.text)
                .filter(BrandCorpus.client_id == req.client_id)
                .all()
            )
            texts = [r[0] for r in rows if r and r[0]]

        if not texts:
            raise HTTPException(status_code=400, detail="No corpus data found")

        profile = brand_voice_service.summarize_brand_voice(texts)

        existing = (
            db.query(BrandVoiceProfile)
            .filter(BrandVoiceProfile.client_id == req.client_id)
            .first()
        )
        if existing:
            existing.profile = profile
            existing.updated_at = datetime.datetime.utcnow()
        else:
            db.add(BrandVoiceProfile(client_id=req.client_id, profile=profile))
        
        db.commit()

        return {"ok": True, "client_id": req.client_id, "profile_status": "created"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Build error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{client_id}")
def get_brand_voice(client_id: str, db: Session = Depends(get_db)):
    """Get brand voice profile"""
    row = (
        db.query(BrandVoiceProfile)
        .filter(BrandVoiceProfile.client_id == client_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Brand voice not found")
    return {
        "client_id": client_id,
        "profile": row.profile,
        "updated_at": row.updated_at,
    }


@router.post("/generate")
def generate_content(req: GenerateRequest, db: Session = Depends(get_db)):
    """Generate content with brand voice + RAG"""
    
    try:
        profile = _ensure_profile(db, req.client_id)
        
        # Get embeddings for RAG
        q_emb = brand_voice_service.embed_texts([req.topic])[0]
        passages = []
        try:
            sql = sat(
                """
                SELECT text
                FROM brand_embeddings
                WHERE client_id = :cid
                ORDER BY embedding <=> :qvec
                LIMIT 8
                """
            )
            res = db.execute(sql, {"cid": req.client_id, "qvec": q_emb}).fetchall()
            passages = [r[0] for r in res]
        except Exception as e:
            logger.warning(f"RAG query failed: {e}")
            passages = []

        prompt = f"""
Role: Senior social media copywriter

Brand Voice: {json.dumps(profile, ensure_ascii=False)}
Few-Shot Examples: {json.dumps(profile.get('few_shots', []), ensure_ascii=False)}
Context Passages: {json.dumps(passages, ensure_ascii=False)}

Task:
Platform: {req.platform}
Content Type: {req.content_type}
Topic: {req.topic}
Goal: {req.goal}

Output (JSON only):
{{"title": "...", "hook": "...", "caption": "...", "hashtags": ["#..."], "cta": "...", "variants": [{{"caption": "..."}}]}}
""".strip()

        output: Dict[str, Any]
        if getattr(brand_voice_service, "openai", None):
            try:
                resp = brand_voice_service.openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a senior social media copywriter. Return JSON only.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.8,
                    response_format={"type": "json_object"},
                )
                output = json.loads(resp.choices[0].message.content)
            except Exception as e:
                logger.error(f"OpenAI generation error: {e}")
                output = {
                    "title": req.topic.title(),
                    "hook": f"{req.topic} için hızlı bir fikir",
                    "caption": f"{req.topic} hakkında marka sesine uygun bir paylaşım taslağı.",
                    "hashtags": ["#brand", "#voice", "#draft"],
                    "cta": "Detaylar için mesaj at!",
                    "variants": [{"caption": "Alternatif kısa varyant."}],
                    "error": f"ai_failed: {e}",
                }
        else:
            output = {
                "title": req.topic.title(),
                "hook": f"{req.topic} için hızlı bir fikir",
                "caption": f"{req.topic} hakkında marka sesine uygun bir paylaşım taslağı.",
                "hashtags": ["#brand", "#voice", "#draft"],
                "cta": "Detaylar için mesaj at!",
                "variants": [{"caption": "Alternatif kısa varyant."}],
                "analysis_method": "no_ai_fallback",
            }

        # Try to save to database
        try:
            db.add(
                GenOutput(
                    client_id=req.client_id,
                    platform=req.platform,
                    content_type=req.content_type,
                    topic=req.topic,
                    goal=req.goal,
                    request_payload={
                        "platform": req.platform,
                        "content_type": req.content_type,
                        "topic": req.topic,
                        "goal": req.goal
                    },
                    output=output,
                )
            )
            db.commit()
            logger.info(f"✅ Content saved to database")
        except Exception as db_error:
            logger.error(f"❌ DB save error: {db_error}")
            db.rollback()
            # Continue without saving

        return output
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Content generation error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/{client_id}")
def get_stats(client_id: str, db: Session = Depends(get_db)):
    """Get statistics"""
    corpus_count = (
        db.query(BrandCorpus).filter(BrandCorpus.client_id == client_id).count()
    )
    embed_count = (
        db.query(BrandEmbedding).filter(BrandEmbedding.client_id == client_id).count()
    )
    outputs = (
        db.query(GenOutput.id).filter(GenOutput.client_id == client_id).count()
    )
    has_profile = (
        db.query(BrandVoiceProfile)
        .filter(BrandVoiceProfile.client_id == client_id)
        .first()
        is not None
    )
    return {
        "client_id": client_id,
        "corpus_items": corpus_count,
        "embeddings": embed_count,
        "generated_outputs": outputs,
        "has_profile": has_profile,
    }


@router.post("/sync-instagram")
async def sync_instagram_profile(
    client_id: str,
    username: str,
    max_posts: int = 50,
    db: Session = Depends(get_db),
):
    """Instagram auto-sync"""
    try:
        from agents.instagram_sync import instagram_sync
    except ImportError:
        from app.agents.instagram_sync import instagram_sync
    
    if instagram_sync is None or not instagram_sync.client:
        raise HTTPException(
            status_code=501,
            detail="instagram_sync service not available - check APIFY_API_TOKEN",
        )

    try:
        posts = await instagram_sync.sync_profile(username, max_posts)
        if not posts:
            raise HTTPException(
                status_code=400, detail="Instagram sync failed or no posts found"
            )

        added = 0
        for post in posts:
            text_val = (post.get("text") or "").strip()
            if not text_val:
                continue
            corpus_item = BrandCorpus(
                client_id=client_id,
                source="instagram_auto",
                text=text_val,
                url=post.get("url"),
                engagement_score=int(post.get("engagement_score") or 0),
            )
            db.add(corpus_item)
            added += 1
        db.commit()

        emb_texts = [p.get("text") for p in posts if (p.get("text") or "").strip()]
        if emb_texts:
            try:
                vecs = brand_voice_service.embed_texts(emb_texts)
                for t, v in zip(emb_texts, vecs):
                    db.add(
                        BrandEmbedding(
                            client_id=client_id, text=t, source="instagram_auto", embedding=v
                        )
                    )
                db.commit()
            except Exception as e:
                logger.error(f"Embedding error: {e}")
                db.rollback()

        profile = brand_voice_service.summarize_brand_voice(emb_texts)

        existing = (
            db.query(BrandVoiceProfile)
            .filter(BrandVoiceProfile.client_id == client_id)
            .first()
        )
        if existing:
            existing.profile = profile
            existing.updated_at = datetime.datetime.utcnow()
        else:
            db.add(BrandVoiceProfile(client_id=client_id, profile=profile))
        db.commit()

        return {
            "success": True,
            "client_id": client_id,
            "posts_synced": added,
            "profile": profile,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Instagram sync error: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
