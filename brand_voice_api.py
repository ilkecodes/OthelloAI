from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db, Client, BrandCorpus, BrandVoiceProfile, GeneratedContent
from brand_voice_service import brand_voice_service

router = APIRouter()

class CorpusItemCreate(BaseModel):
    client_id: str
    platform: str
    content_type: Optional[str] = "post"
    text_content: str
    post_metadata: Optional[dict] = {}

class BuildVoiceRequest(BaseModel):
    client_id: str
    force_rebuild: Optional[bool] = False

class GenerateContentRequest(BaseModel):
    client_id: str
    prompt: str
    platform: str = "instagram"

@router.get("/health")
def health_check():
    import os
    return {
        "status": "healthy",
        "service": "Brand Voice AI",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@router.post("/corpus")
def add_corpus_item(item: CorpusItemCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == item.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    corpus_item = BrandCorpus(
        client_id=item.client_id,
        platform=item.platform,
        content_type=item.content_type,
        text_content=item.text_content,
        post_metadata=item.post_metadata
    )
    
    db.add(corpus_item)
    db.commit()
    db.refresh(corpus_item)
    
    return {"message": "Content added", "id": corpus_item.id}

@router.post("/build")
def build_brand_voice(request: BuildVoiceRequest, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    corpus_items = db.query(BrandCorpus).filter(
        BrandCorpus.client_id == request.client_id
    ).all()
    
    if not corpus_items:
        raise HTTPException(status_code=400, detail="No content found. Add content first.")
    
    corpus_data = [{"text_content": item.text_content} for item in corpus_items]
    voice_data = brand_voice_service.analyze_brand_voice(corpus_data)
    
    existing = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == request.client_id
    ).first()
    
    if existing:
        existing.tone = voice_data.get('tone')
        existing.language_style = voice_data.get('language_style')
        existing.voice_summary = voice_data.get('voice_summary')
        existing.confidence_score = voice_data.get('confidence_score', 0)
        existing.updated_at = datetime.now()
        profile = existing
    else:
        profile = BrandVoiceProfile(
            client_id=request.client_id,
            tone=voice_data.get('tone'),
            language_style=voice_data.get('language_style'),
            emoji_usage=voice_data.get('emoji_usage'),
            content_themes=voice_data.get('content_themes'),
            brand_personality=voice_data.get('brand_personality'),
            hashtag_strategy=voice_data.get('hashtag_strategy'),
            voice_summary=voice_data.get('voice_summary'),
            sample_size=len(corpus_items),
            confidence_score=voice_data.get('confidence_score', 0)
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    
    return {
        "message": "Brand voice created",
        "profile_id": profile.id,
        "tone": profile.tone,
        "confidence_score": profile.confidence_score
    }

@router.get("/get/{client_id}")
def get_brand_voice(client_id: str, db: Session = Depends(get_db)):
    profile = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == client_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Brand voice not found")
    
    return {
        "profile_id": profile.id,
        "tone": profile.tone,
        "voice_summary": profile.voice_summary,
        "confidence_score": profile.confidence_score
    }

@router.post("/generate")
def generate_content(request: GenerateContentRequest, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    profile = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == request.client_id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Brand voice not found. Build it first.")
    
    voice_profile = {
        "tone": profile.tone,
        "voice_summary": profile.voice_summary
    }
    
    generated_text = brand_voice_service.generate_branded_content(
        voice_profile=voice_profile,
        prompt=request.prompt,
        platform=request.platform
    )
    
    content = GeneratedContent(
        client_id=request.client_id,
        profile_id=profile.id,
        platform=request.platform,
        content_text=generated_text,
        prompt_used=request.prompt
    )
    
    db.add(content)
    db.commit()
    
    return {
        "content_id": content.id,
        "text": generated_text,
        "platform": request.platform
    }

# ============= INSTAGRAM AUTO-SYNC =============

@router.post("/sync-instagram")
async def sync_instagram(
    client_id: str,
    instagram_username: str,
    max_posts: int = 15,
    db: Session = Depends(get_db)
):
    """Instagram profilinden otomatik içerik çek ve corpus'a ekle"""
    
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    try:
        # Apify ile Instagram profil scrape
        from apify_scanner import ApifyScanner
        scanner = ApifyScanner()
        
        print(f"📸 Syncing Instagram @{instagram_username}...")
        
        posts = await scanner.scan_instagram_profile(instagram_username, max_posts=max_posts)
        
        if not posts:
            raise HTTPException(status_code=400, detail="No posts found. Check username or API quota.")
        
        # Corpus'a ekle
        added = 0
        for post in posts:
            caption = post.get('caption', '')
            if not caption or len(caption) < 20:
                continue
            
            corpus_item = BrandCorpus(
                client_id=client_id,
                platform="instagram",
                content_type="post",
                text_content=caption,
                post_metadata={
                    "likes": post.get('likesCount', 0),
                    "comments": post.get('commentsCount', 0),
                    "url": post.get('url', ''),
                    "timestamp": post.get('timestamp', '')
                }
            )
            db.add(corpus_item)
            added += 1
        
        db.commit()
        
        print(f"✅ Added {added} Instagram posts to corpus")
        
        return {
            "message": f"Synced {added} posts from @{instagram_username}",
            "instagram_username": instagram_username,
            "posts_added": added,
            "total_posts_found": len(posts)
        }
        
    except Exception as e:
        print(f"❌ Instagram sync error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
