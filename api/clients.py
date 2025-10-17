"""Clients API - Müşteri Yönetimi"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database import get_db, Client
from services import apify_service, brand_analyzer
import uuid

router = APIRouter()

class ClientCreate(BaseModel):
    name: str
    industry: str
    description: Optional[str] = None
    target_audience: Optional[str] = None
    keywords: List[str] = []
    social_platforms: List[str] = []
    instagram_username: Optional[str] = None

class ClientResponse(BaseModel):
    id: str
    name: str
    slug: str
    active: bool
    keywords: Optional[dict] = None
    platforms: Optional[dict] = None
    brand_guidelines: Optional[dict] = None
    brand_voice_learned: bool = False
    created_at: str
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    try:
        clients = db.query(Client).filter(Client.active == True).all()
        return [ClientResponse(
            id=c.id,
            name=c.name,
            slug=c.slug,
            active=c.active,
            keywords=c.keywords,
            platforms=c.platforms,
            brand_guidelines=c.brand_guidelines,
            brand_voice_learned=bool(c.brand_guidelines and c.brand_guidelines.get("brand_voice")),
            created_at=c.created_at.isoformat() if c.created_at else ""
        ) for c in clients]
    except Exception as e:
        print(f"ERROR: {e}")
        return []

@router.post("/", response_model=ClientResponse)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    try:
        # Unique slug oluştur (duplicate hatası olmasın)
        base_slug = client.name.lower().replace(" ", "-").replace(".", "")
        slug = base_slug
        counter = 1
        
        # Slug zaten varsa sonuna sayı ekle
        while db.query(Client).filter(Client.slug == slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        print(f"Creating client: {client.name} with slug: {slug}")
        
        # Brand voice (opsiyonel)
        brand_voice_dict = None
        if client.instagram_username:
            try:
                profile = await apify_service.get_profile_details(client.instagram_username)
                if profile and profile.get("latestPosts"):
                    brand_voice_dict = await brand_analyzer.analyze_instagram_profile(
                        username=client.instagram_username,
                        sample_posts=profile["latestPosts"][:10]
                    )
            except Exception as e:
                print(f"⚠️ Brand voice failed: {e}")
        
        db_client = Client(
            name=client.name,
            slug=slug,  # Unique slug
            keywords={"keywords": client.keywords} if client.keywords else {},
            platforms={"platforms": client.social_platforms} if client.social_platforms else {},
            brand_guidelines={
                "industry": client.industry or "",
                "description": client.description or "",
                "target_audience": client.target_audience or "",
                "brand_voice": brand_voice_dict or {}
            },
            active=True
        )
        
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        
        return ClientResponse(
            id=db_client.id,
            name=db_client.name,
            slug=db_client.slug,
            active=db_client.active,
            keywords=db_client.keywords,
            platforms=db_client.platforms,
            brand_guidelines=db_client.brand_guidelines,
            brand_voice_learned=bool(brand_voice_dict),
            created_at=db_client.created_at.isoformat()
        )
    
    except Exception as e:
        print(f"❌ ERROR: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{client_id}")
def delete_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Not found")
    client.active = False
    db.commit()
    return {"message": "Deleted", "id": client_id}
