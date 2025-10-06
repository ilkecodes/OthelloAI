from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from ..database import get_db
from ..models.client import Client
from ..hashtags.client_hashtags import CLIENT_HASHTAGS

router = APIRouter()

class ClientCreate(BaseModel):
    name: str
    industry: str
    keywords: str
    instagram_url: Optional[str] = None

class ClientUpdate(BaseModel):
    instagram_url: Optional[str] = None
    industry: Optional[str] = None
    keywords: Optional[str] = None

@router.get("/")
def get_clients(db: Session = Depends(get_db)):
    """Get all clients."""
    clients = db.query(Client).all()
    return clients

@router.post("/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    """Create a new client."""
    
    # Check if client already exists
    existing = db.query(Client).filter(Client.name == client.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Client '{client.name}' already exists")
    
    db_client = Client(
        name=client.name,
        industry=client.industry,
        keywords=client.keywords,
        instagram_url=client.instagram_url
    )
    
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    
    return db_client

@router.patch("/{client_id}")
async def update_client(client_id: int, update: ClientUpdate, db: Session = Depends(get_db)):
    """Update client with Instagram URL and analyze profile."""
    
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Update fields
    if update.instagram_url:
        client.instagram_url = update.instagram_url
        
        # Analyze profile if Instagram URL provided
        try:
            from ..agents.profile_analyzer import ProfileAnalyzer
            from ..agents.apify_scanner import ApifyScanner
            
            analyzer = ProfileAnalyzer()
            scanner = ApifyScanner()
            
            username = analyzer.extract_username(update.instagram_url)
            client.instagram_username = username
            
            # Scan profile posts
            posts = await scanner.scan_instagram_profile(username, max_posts=10)
            
            # Analyze brand voice
            brand_voice = await analyzer.analyze_profile(username, posts)
            client.brand_voice = str(brand_voice)
            
            print(f"✅ Brand voice analyzed for @{username}")
            
        except Exception as e:
            print(f"⚠️ Could not analyze profile: {e}")
    
    if update.industry:
        client.industry = update.industry
    if update.keywords:
        client.keywords = update.keywords
    
    db.commit()
    db.refresh(client)
    
    return client

@router.get("/{client_id}/hashtags")
def get_client_hashtags(client_id: int, db: Session = Depends(get_db)):
    """Get hashtags for a client."""
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    client_key = client.name.lower().replace(" ", "_")
    hashtag_groups = CLIENT_HASHTAGS.get(client_key, {
        "primary": [],
        "secondary": [],
        "longtail": []
    })
    
    formatted_post = "\n".join([
        "Primary: " + " ".join([f"#{h}" for h in hashtag_groups.get("primary", [])]),
        "Secondary: " + " ".join([f"#{h}" for h in hashtag_groups.get("secondary", [])]),
        "Long-tail: " + " ".join([f"#{h}" for h in hashtag_groups.get("longtail", [])])
    ])
    
    return {
        "client_name": client.name,
        "hashtags": hashtag_groups,
        "formatted_post": formatted_post
    }
