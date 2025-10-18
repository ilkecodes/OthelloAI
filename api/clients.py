from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from database import get_db, Client

router = APIRouter()

class ClientCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    description: Optional[str] = None
    target_audience: Optional[str] = None
    brand_voice: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    social_platforms: List[str] = Field(default_factory=list)

class ClientResponse(BaseModel):
    id: str
    name: str
    slug: str
    active: bool
    keywords: Optional[Dict[str, Any]] = None
    platforms: Optional[Dict[str, Any]] = None
    brand_guidelines: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).filter(Client.active == True).all()
    return clients

@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    slug = client.name.lower().replace(" ", "-").replace(".", "")
    
    db_client = Client(
        name=client.name,
        slug=slug,
        keywords={"keywords": client.keywords},
        platforms={"platforms": client.social_platforms},
        brand_guidelines={
            "industry": client.industry,
            "description": client.description,
            "target_audience": client.target_audience,
            "brand_voice": client.brand_voice
        },
        active=True
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.delete("/{client_id}")
def delete_client(client_id: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Not found")
    client.active = False
    db.commit()
    return {"message": "Client deleted successfully", "id": client_id}

@router.patch("/{client_id}")
def update_client(
    client_id: str,
    instagram_url: str = None,
    db: Session = Depends(get_db)
):
    """Update client with Instagram URL"""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    if instagram_url:
        client.instagram_url = instagram_url
    
    db.commit()
    db.refresh(client)
    return client
