"""Clients API - Müşteri Yönetimi"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database import get_db, Client
from services import apify_service, brand_analyzer

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
    clients = db.query(Client).filter(Client.active == True).all()
    result = []
    for client in clients:
        result.append(ClientResponse(
            id=client.id,
            name=client.name,
            slug=client.slug,
            active=client.active,
            keywords=client.keywords,
            platforms=client.platforms,
            brand_guidelines=client.brand_guidelines,
            brand_voice_learned=bool(client.brand_guidelines and client.brand_guidelines.get("brand_voice")),
            created_at=client.created_at.isoformat() if client.created_at else ""
        ))
    return result

@router.post("/", response_model=ClientResponse)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    slug = client.name.lower().replace(" ", "-").replace(".", "")
    
    brand_voice_dict = None
    if client.instagram_username:
        try:
            profile = await apify_service.get_profile_details(client.instagram_username)
            if profile and profile.get("latestPosts"):
                brand_voice_dict = await brand_analyzer.analyze_instagram_profile(
                    username=client.instagram_username,
                    sample_posts=profile["latestPosts"][:10]
                )
                print(f"✅ Brand voice learned for {client.name}")
        except Exception as e:
            print(f"⚠️ Could not analyze: {e}")
    
    db_client = Client(
        name=client.name,
        slug=slug,
        keywords={"keywords": client.keywords},
        platforms={"platforms": client.social_platforms},
        brand_guidelines={
            "industry": client.industry,
            "description": client.description,
            "target_audience": client.target_audience,
            "brand_voice": brand_voice_dict if brand_voice_dict else {}
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

@router.delete("/{client_id}")
def delete_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    client.active = False
    db.commit()
    return {"message": "Client deleted", "id": client_id}
