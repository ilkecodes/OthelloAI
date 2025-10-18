"""Content API - İçerik Üretimi"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from database import get_db, Content, Client, Trend
from services import openai_service

router = APIRouter()

class ContentGenerateRequest(BaseModel):
    client_id: str
    platform: str
    topic: str
    tone: Optional[str] = None
    goal: Optional[str] = "engagement"
    trend_id: Optional[int] = None

@router.post("/generate")
async def generate_content(request: ContentGenerateRequest, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    brand_voice = {}
    if client.brand_guidelines and client.brand_guidelines.get("brand_voice"):
        brand_voice = client.brand_guidelines["brand_voice"]
    else:
        brand_voice = {
            "tone": "professional",
            "emoji_usage": "medium",
            "language_style": "formal",
            "content_themes": ["general"],
            "hashtag_strategy": "3-5 hashtags",
            "brand_personality": ["authentic"]
        }
    
    trend_context = None
    if request.trend_id:
        trend = db.query(Trend).filter(Trend.id == request.trend_id).first()
        if trend:
            trend_context = f"Trend: #{trend.keyword} (Score: {trend.trending_score:.2f})"
    
    print(f"🎨 Generating content for {client.name}")
    
    try:
        result = await openai_service.generate_content(
            client_name=client.name,
            brand_voice=brand_voice,
            platform=request.platform,
            topic=request.topic,
            tone=request.tone,
            goal=request.goal,
            trend_context=trend_context
        )
        
        db_content = Content(
            client_id=request.client_id,
            platform=request.platform,
            text=f"{result['caption']}\n\n{result['hashtags']}\n\n{result['cta']}",
            status="generated"
        )
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        
        return {
            "success": True,
            "content_id": db_content.id,
            "caption": result["caption"],
            "hashtags": result["hashtags"],
            "cta": result["cta"],
            "platform": request.platform,
            "brand_voice_used": bool(client.brand_guidelines and client.brand_guidelines.get("brand_voice"))
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/")
async def get_content(client_id: Optional[str] = None, db: Session = Depends(get_db)):
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
