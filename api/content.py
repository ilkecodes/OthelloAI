"""Content API - Gelişmiş İçerik Üretimi"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from database import get_db, Content, Client, Trend
from services import openai_service
from services.platform_specs import get_platform_spec, PLATFORM_CONTENT_TYPES

router = APIRouter()

class ContentGenerateRequest(BaseModel):
    client_id: str
    platform: str
    content_type: str  # ZORUNLU!
    topic: str
    tone: Optional[str] = None
    goal: Optional[str] = "engagement"
    trend_id: Optional[int] = None

@router.post("/generate")
async def generate_content(request: ContentGenerateRequest, db: Session = Depends(get_db)):
    """İçerik üret - platform ve content type'a göre"""
    
    # DEBUG
    print("=" * 80)
    print(f"🔥 REQUEST RECEIVED:")
    print(f"   Platform: {request.platform}")
    print(f"   Content Type: {request.content_type}")
    print(f"   Topic: {request.topic}")
    print("=" * 80)
    
    # Validation
    spec = get_platform_spec(request.platform, request.content_type)
    if not spec:
        raise HTTPException(
            status_code=400, 
            detail=f"Platform '{request.platform}' için '{request.content_type}' desteklenmiyor"
        )
    
    print(f"✅ Spec found: {spec.get('name')}")
    
    # Client kontrol
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    print(f"✅ Client found: {client.name}")
    
    # Brand voice
    brand_voice = {}
    if client.brand_guidelines and client.brand_guidelines.get("brand_voice"):
        brand_voice = client.brand_guidelines["brand_voice"]
    else:
        brand_voice = {
            "tone": "professional",
            "emoji_usage": "medium",
            "language_style": "formal"
        }
    
    # Trend context
    trend_context = None
    if request.trend_id:
        trend = db.query(Trend).filter(Trend.id == request.trend_id).first()
        if trend:
            trend_context = f"Trend: #{trend.keyword} (Score: {trend.trending_score:.2f})"
    
    print(f"🎨 Calling openai_service.generate_content with content_type={request.content_type}")
    
    try:
        result = await openai_service.generate_content(
            client_name=client.name,
            brand_voice=brand_voice,
            platform=request.platform,
            content_type=request.content_type,  # BURASI ÇOK ÖNEMLİ!
            topic=request.topic,
            tone=request.tone,
            goal=request.goal,
            trend_context=trend_context
        )
        
        print(f"✅ Result received, content_type in result: {result.get('content_type', 'NOT FOUND')}")
        print(f"   Keys in result: {list(result.keys())}")
        
        # DB'ye kaydet
        full_text = result.get("caption", "")
        if result.get("content_type") == "carousel":
            full_text = f"CAROUSEL ({len(result.get('slides', []))} slayt)\n\n{result.get('caption', '')}"
            print(f"✅ Carousel detected with {len(result.get('slides', []))} slides")
        elif result.get("content_type") == "thread":
            full_text = "\n\n".join(result.get("tweets", []))
        
        db_content = Content(
            client_id=request.client_id,
            platform=f"{request.platform}_{request.content_type}",
            text=full_text,
            status="generated"
        )
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        
        return {
            "success": True,
            "content_id": db_content.id,
            "platform": request.platform,
            "content_type": request.content_type,
            **result
        }
    
    except Exception as e:
        import traceback
        print("❌ ERROR OCCURRED:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
async def get_content(client_id: Optional[str] = None, db: Session = Depends(get_db)):
    """İçerikleri listele"""
    query = db.query(Content)
    if client_id:
        query = query.filter(Content.client_id == client_id)
    contents = query.order_by(Content.created_at.desc()).limit(50).all()
    return {
        "count": len(contents),
        "content": [
            {
                "id": c.id,
                "client_id": c.client_id,
                "platform": c.platform,
                "text": c.text,
                "status": c.status,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in contents
        ]
    }
