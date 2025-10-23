from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
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
        "status": "sağlıklı",
        "service": "Marka Sesi AI",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@router.post("/corpus")
def add_corpus_item(item: CorpusItemCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == item.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    
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
        "message": "İçerik eklendi",
        "id": corpus_item.id,
        "client": client.name
    }

@router.post("/build")
def build_brand_voice(request: BuildVoiceRequest, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    
    corpus_items = db.query(BrandCorpus).filter(
        BrandCorpus.client_id == request.client_id
    ).all()
    
    if not corpus_items:
        raise HTTPException(
            status_code=400, 
            detail="İçerik bulunamadı. Önce /corpus endpoint'i ile içerik ekleyin."
        )
    
    print(f"🔍 {client.name} için marka sesi analiz ediliyor ({len(corpus_items)} içerik)...")
    
    corpus_data = [{"text_content": item.text_content} for item in corpus_items]
    voice_data = brand_voice_service.analyze_brand_voice(corpus_data)
    
    existing = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == request.client_id
    ).first()
    
    if existing:
        existing.tone = voice_data.get('tone')
        existing.language_style = voice_data.get('language_style')
        existing.emoji_usage = voice_data.get('emoji_usage')
        existing.content_themes = voice_data.get('content_themes')
        existing.brand_personality = voice_data.get('brand_personality')
        existing.hashtag_strategy = voice_data.get('hashtag_strategy')
        existing.voice_summary = voice_data.get('voice_summary')
        existing.confidence_score = voice_data.get('confidence_score', 0)
        existing.sample_size = len(corpus_items)
        existing.updated_at = datetime.now()
        profile = existing
        print(f"♻️  Mevcut profil güncellendi")
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
        print(f"✨ Yeni profil oluşturuldu")
    
    db.commit()
    db.refresh(profile)
    
    print(f"✅ {client.name} için marka sesi oluşturuldu!")
    
    return {
        "message": "Marka sesi başarıyla oluşturuldu",
        "profile_id": profile.id,
        "client_name": client.name,
        "tone": profile.tone,
        "voice_summary": profile.voice_summary,
        "confidence_score": profile.confidence_score,
        "sample_size": profile.sample_size
    }

@router.get("/get/{client_id}")
def get_brand_voice(client_id: str, db: Session = Depends(get_db)):
    profile = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == client_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=404, 
            detail="Marka sesi bulunamadı. Önce /build endpoint'i ile oluşturun."
        )
    
    return {
        "profile_id": profile.id,
        "tone": profile.tone,
        "language_style": profile.language_style,
        "emoji_usage": profile.emoji_usage,
        "content_themes": profile.content_themes,
        "brand_personality": profile.brand_personality,
        "hashtag_strategy": profile.hashtag_strategy,
        "voice_summary": profile.voice_summary,
        "confidence_score": profile.confidence_score,
        "sample_size": profile.sample_size
    }

@router.post("/generate")
def generate_content(request: GenerateContentRequest, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    
    profile = db.query(BrandVoiceProfile).filter(
        BrandVoiceProfile.client_id == request.client_id
    ).first()
    
    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Marka sesi bulunamadı. Önce /build ile marka sesi oluşturun."
        )
    
    voice_profile = {
        "tone": profile.tone,
        "language_style": profile.language_style,
        "emoji_usage": profile.emoji_usage,
        "voice_summary": profile.voice_summary,
        "hashtag_strategy": profile.hashtag_strategy
    }
    
    print(f"🎨 {client.name} için içerik üretiliyor...")
    
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
    
    print(f"✅ İçerik üretildi ve kaydedildi!")
    
    return {
        "content_id": content.id,
        "text": generated_text,
        "platform": request.platform,
        "client_name": client.name,
        "voice_tone": profile.tone
    }

@router.get("/stats/{client_id}")
def get_stats(client_id: str, db: Session = Depends(get_db)):
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

# ============= INSTAGRAM OTOMATİK SENKRONIZASYON =============

@router.post("/sync-instagram")
async def sync_instagram(
    client_id: str,
    instagram_username: str,
    max_posts: int = 15,
    db: Session = Depends(get_db)
):
    """Instagram profilinden otomatik içerik çek"""
    
    # URL'den username'i temizle
    username = instagram_username.replace('https://www.instagram.com/', '').replace('/', '').strip()
    
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Müşteri bulunamadı")
    
    try:
        print(f"📸 @{username} Instagram profili senkronize ediliyor...")
        
        # Apify import
        import os
        from apify_client import ApifyClient
        
        apify_token = os.getenv("APIFY_API_TOKEN")
        if not apify_token:
            raise HTTPException(status_code=400, detail="Apify API anahtarı yapılandırılmamış")
        
        apify_client = ApifyClient(apify_token)
        
        # Instagram profile scraper
        run_input = {
            "usernames": [username],
            "resultsLimit": max_posts
        }
        
        print(f"🔄 Apify ile Instagram taranıyor...")
        run = apify_client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
        
        posts = []
        for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            if item.get('latestPosts'):
                posts = item['latestPosts'][:max_posts]
                break
        
        if not posts:
            raise HTTPException(status_code=400, detail="Post bulunamadı. Kullanıcı adını kontrol edin.")
        
        print(f"📝 {len(posts)} post bulundu, corpus'a ekleniyor...")
        
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
        
        print(f"✅ {added} Instagram postu eklendi!")
        
        return {
            "success": True,
            "message": f"@{username} profilinden {added} post eklendi",
            "instagram_username": username,
            "posts_added": added,
            "total_posts_found": len(posts),
            "client_name": client.name
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Instagram senkronizasyon hatası: {e}")
        raise HTTPException(status_code=500, detail=f"Hata: {str(e)}")
