from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db, Content
from services.openai_service import openai_service

router = APIRouter()

class ContentCreate(BaseModel):
    client_id: str
    platform: str
    text: str
    scheduled_time: Optional[datetime] = None

class ContentGenerate(BaseModel):
    client_id: str
    platform: str
    prompt: str
    tone: str = "professional"

class ContentResponse(BaseModel):
    id: str
    client_id: str
    platform: str
    text: str
    status: str
    scheduled_time: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ContentResponse])
def get_content(client_id: Optional[str] = None, db: Session = Depends(get_db)):
    if not db:
        return []
    query = db.query(Content)
    if client_id:
        query = query.filter(Content.client_id == client_id)
    return query.all()

@router.post("/", response_model=ContentResponse)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    db_content = Content(
        client_id=content.client_id,
        platform=content.platform,
        text=content.text,
        scheduled_time=content.scheduled_time,
        status="draft"
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

@router.post("/generate")
def generate_content(request: ContentGenerate, db: Session = Depends(get_db)):
    """Generate content using OpenAI"""
    
    generated_text = openai_service.generate_content(
        prompt=request.prompt,
        platform=request.platform,
        tone=request.tone
    )
    
    if not db:
        return {
            "text": generated_text,
            "message": "Content generated but not saved (database unavailable)"
        }
    
    # Save to database
    db_content = Content(
        client_id=request.client_id,
        platform=request.platform,
        text=generated_text,
        status="generated"
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    
    return {
        "id": db_content.id,
        "text": generated_text,
        "message": "Content generated and saved"
    }

@router.get("/{content_id}", response_model=ContentResponse)
def get_content_item(content_id: str, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content
