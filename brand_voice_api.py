from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db, Client
from database import BrandCorpus, BrandVoiceProfile, GeneratedContent, ContentFeedback
from brand_voice_service import brand_voice_service

router = APIRouter()

# ============= SCHEMAS =============

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
    content_type: str = "post"

class ContentFeedbackCreate(BaseModel):
    content_id: str
    rating: int
    feedback_type: str
    notes: Optional[str] = None

# ============= ENDPOINTS =============

@router.get("/health")
def health_check():
    """Brand Voice servis sağlık kontrolü"""
    import os
    return {
        "status": "healthy",
        "service": "Brand Voice AI",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@router.post("/corpus")
def add_corpus_item(item: CorpusItemCreate, db: Session = Depends(get_db)):
    """Marka içeriği ekle"""
    
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
    
    return {
        "message": "Corpus item added",
        "id": corpus_item.id,
        "client": client.name
    }

@router.post("/build")
async def build_brand_voice(request: BuildVoiceRequest, db: Session = Depends(get_db)):
    """Marka sesini analiz et ve profil oluştur"""
    
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    existing_profile = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == request.client_id
    ).first()
    
    if existing_profile and not request.force_rebuild:
        return {
            "message": "Brand voice profile already exists",
            "profile_id": existing_profile.id,
            "use_force_rebuild": True
        }
    
    corpus_items = db.query(BrandCorpus).filter(
        BrandCorpus.client_id == request.client_id
    ).all()
    
    if not corpus_items:
        raise HTTPException(
            status_code=400, 
            detail="No corpus items found. Add content first using /corpus endpoint"
        )
    
    print(f"🔍 Analyzing brand voice for {client.name} with {len(corpus_items)} items...")
    
    corpus_data = [
        {
            "text_content": item.text_content,
            "post_metadata": item.post_metadata
        }
        for item in corpus_items
    ]
    
    voice_data = brand_voice_service.analyze_brand_voice(corpus_data)
    
    if existing_profile:
        existing_profile.tone = voice_data.get('tone')
        existing_profile.language_style = voice_data.get('language_style')
        existing_profile.emoji_usage = voice_data.get('emoji_usage')
        existing_profile.content_themes = voice_data.get('content_themes')
        existing_profile.brand_personality = voice_data.get('brand_personality')
        existing_profile.hashtag_strategy = voice_data.get('hashtag_strategy')
        existing_profile.voice_summary = voice_data.get('voice_summary')
        existing_profile.sample_size = voice_data.get('sample_size', len(corpus_items))
        existing_profile.confidence_score = voice_data.get('confidence_score', 0)
        existing_profile.updated_at = datetime.now()
        
        profile = existing_profile
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
            sample_size=voice_data.get('sample_size', len(corpus_items)),
            confidence_score=voice_data.get('confidence_score', 0)
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    
    print(f"✅ Brand voice profile created for {client.name}")
    
    return {
        "message": "Brand voice profile created successfully",
        "profile_id": profile.id,
        "client_name": client.name,
        "voice_profile": {
            "tone": profile.tone,
            "language_style": profile.language_style,
            "emoji_usage": profile.emoji_usage,
            "content_themes": profile.content_themes,
            "brand_personality": profile.brand_personality,
            "voice_summary": profile.voice_summary,
            "confidence_score": profile.confidence_score,
            "sample_size": profile.sample_size
        }
    }

@router.get("/get/{client_id}")
def get_brand_voice(client_id: str, db: Session = Depends(get_db)):
    """Marka sesi profilini getir"""
    
    profile = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == client_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=404, 
            detail="Brand voice profile not found. Build it first using /build endpoint"
        )
    
    return {
        "profile_id": profile.id,
        "client_id": profile.client_id,
        "tone": profile.tone,
        "language_style": profile.language_style,
        "emoji_usage": profile.emoji_usage,
        "content_themes": profile.content_themes,
        "brand_personality": profile.brand_personality,
        "hashtag_strategy": profile.hashtag_strategy,
        "voice_summary": profile.voice_summary,
        "confidence_score": profile.confidence_score,
        "sample_size": profile.sample_size,
        "created_at": profile.created_at,
        "updated_at": profile.updated_at
    }

@router.post("/generate")
async def generate_content(request: GenerateContentRequest, db: Session = Depends(get_db)):
    """Marka sesine uygun içerik üret"""
    
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    profile = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == request.client_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Brand voice profile not found. Build it first using /build endpoint"
        )
    
    voice_profile = {
        "tone": profile.tone,
        "language_style": profile.language_style,
        "emoji_usage": profile.emoji_usage,
        "content_themes": profile.content_themes,
        "brand_personality": profile.brand_personality,
        "hashtag_strategy": profile.hashtag_strategy,
        "voice_summary": profile.voice_summary
    }
    
    print(f"🎨 Generating content for {client.name}...")
    
    generated_text = brand_voice_service.generate_branded_content(
        voice_profile=voice_profile,
        prompt=request.prompt,
        platform=request.platform,
        content_type=request.content_type
    )
    
    content = GeneratedContent(
        client_id=request.client_id,
        profile_id=profile.id,
        platform=request.platform,
        content_text=generated_text,
        prompt_used=request.prompt,
        is_approved="pending"
    )
    
    db.add(content)
    db.commit()
    db.refresh(content)
    
    print(f"✅ Content generated and saved")
    
    return {
        "content_id": content.id,
        "text": generated_text,
        "platform": request.platform,
        "client_name": client.name,
        "voice_tone": profile.tone
    }

@router.get("/stats/{client_id}")
def get_stats(client_id: str, db: Session = Depends(get_db)):
    """Marka sesi istatistikleri"""
    
    corpus_count = db.query(BrandCorpus).filter(
        BrandCorpus.client_id == client_id
    ).count()
    
    generated_count = db.query(GeneratedContent).filter(
        GeneratedContent.client_id == client_id
    ).count()
    
    profile = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == client_id
    ).first()
    
    return {
        "client_id": client_id,
        "corpus_items": corpus_count,
        "generated_contents": generated_count,
        "has_profile": profile is not None,
        "confidence_score": profile.confidence_score if profile else 0
    }

@router.post("/feedback")
def add_feedback(feedback: ContentFeedbackCreate, db: Session = Depends(get_db)):
    """İçerik feedback'i ekle"""
    
    content = db.query(GeneratedContent).filter(
        GeneratedContent.id == feedback.content_id
    ).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    content.user_rating = feedback.rating
    if feedback.rating >= 4:
        content.is_approved = "approved"
    elif feedback.rating <= 2:
        content.is_approved = "rejected"
    
    feedback_record = ContentFeedback(
        content_id=feedback.content_id,
        client_id=content.client_id,
        rating=feedback.rating,
        feedback_type=feedback.feedback_type,
        notes=feedback.notes
    )
    
    db.add(feedback_record)
    db.commit()
    
    return {
        "message": "Feedback recorded",
        "content_status": content.is_approved
    }
