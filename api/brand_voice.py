"""
Brand Voice API Router - İzole endpoint'ler
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from database import get_db
from models.brand_voice_models import BrandCorpus, BrandVoiceProfile, BrandEmbedding, GenOutput
from services.brand_voice_service import brand_voice_service

router = APIRouter()

# Schemas
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

# Endpoints
@router.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "brand-voice"}

@router.post("/corpus")
def add_to_corpus(data: CorpusAdd, db: Session = Depends(get_db)):
    """Add content to brand corpus"""
    
    added = 0
    for item in data.texts:
        corpus_item = BrandCorpus(
            client_id=data.client_id,
            source=data.source,
            text=item.get("text", ""),
            url=item.get("url"),
            engagement_score=item.get("engagement_score", 0)
        )
        db.add(corpus_item)
        added += 1
    
    db.commit()
    
    return {
        "success": True,
        "client_id": data.client_id,
        "added": added
    }

@router.post("/build")
def build_brand_voice(req: BuildRequest, db: Session = Depends(get_db)):
    """Build brand voice profile from corpus"""
    
    # Get corpus
    corpus_items = db.query(BrandCorpus).filter(
        BrandCorpus.client_id == req.client_id
    ).all()
    
    texts = [item.text for item in corpus_items]
    
    if req.texts:
        texts += req.texts
    
    if not texts:
        raise HTTPException(status_code=400, detail="No corpus data")
    
    # Extract brand voice
    profile = brand_voice_service.summarize_brand_voice(texts)
    
    # Save profile
    existing = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == req.client_id
    ).first()
    
    if existing:
        existing.profile = profile
    else:
        new_profile = BrandVoiceProfile(
            client_id=req.client_id,
            profile=profile
        )
        db.add(new_profile)
    
    db.commit()
    
    # Generate embeddings
    db.query(BrandEmbedding).filter(
        BrandEmbedding.client_id == req.client_id
    ).delete()
    db.commit()
    
    embeddings = brand_voice_service.embed_texts(texts)
    
    for text, vec in zip(texts, embeddings):
        emb = BrandEmbedding(
            client_id=req.client_id,
            text=text[:500],
            vector=vec
        )
        db.add(emb)
    
    db.commit()
    
    return {
        "success": True,
        "client_id": req.client_id,
        "profile": profile,
        "corpus_count": len(texts)
    }

@router.get("/get/{client_id}")
def get_brand_voice(client_id: str, db: Session = Depends(get_db)):
    """Get brand voice profile"""
    
    profile_row = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == client_id
    ).first()
    
    if not profile_row:
        raise HTTPException(status_code=404, detail="Brand voice not found")
    
    return {
        "client_id": client_id,
        "profile": profile_row.profile,
        "updated_at": profile_row.updated_at.isoformat()
    }

@router.post("/generate")
def generate_content(req: GenerateRequest, db: Session = Depends(get_db)):
    """Generate content with brand voice"""
    
    # Get brand voice
    profile_row = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == req.client_id
    ).first()
    
    if not profile_row:
        raise HTTPException(status_code=404, detail="Brand voice not found. Run /build first")
    
    # Mock generation (replace with OpenAI later)
    output = {
        "title": f"{req.topic} ile İlgili İçerik",
        "hook": f"Bu {req.topic} hakkında bilmeniz gerekenler!",
        "caption": f"{req.topic} konusunda harika bir içerik. Sizce ne düşünüyorsunuz?",
        "hashtags": ["#marketing", "#content", "#brand"],
        "cta": "Yorumlarda düşüncelerinizi paylaşın!",
        "variants": [
            {"caption": f"Alternatif 1: {req.topic}"},
            {"caption": f"Alternatif 2: {req.topic}"}
        ]
    }
    
    # Save output
    gen_output = GenOutput(
        client_id=req.client_id,
        request_payload={
            "platform": req.platform,
            "topic": req.topic,
            "goal": req.goal
        },
        output=output
    )
    db.add(gen_output)
    db.commit()
    
    return {
        "success": True,
        "output": output,
        "gen_id": gen_output.id
    }

@router.get("/stats/{client_id}")
def get_corpus_stats(client_id: str, db: Session = Depends(get_db)):
    """Get corpus statistics"""
    
    from sqlalchemy import func
    
    total = db.query(func.count(BrandCorpus.id)).filter(
        BrandCorpus.client_id == client_id
    ).scalar()
    
    avg_engagement = db.query(func.avg(BrandCorpus.engagement_score)).filter(
        BrandCorpus.client_id == client_id
    ).scalar()
    
    return {
        "client_id": client_id,
        "total_items": total or 0,
        "avg_engagement": float(avg_engagement) if avg_engagement else 0
    }
