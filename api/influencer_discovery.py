from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Influencer, Client
from services.influencer_service import influencer_discovery
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class InfluencerSearchRequest(BaseModel):
    client_id: str
    hashtags: Optional[List[str]] = []
    location: Optional[str] = None
    min_followers: Optional[int] = 1000
    limit: Optional[int] = 30

@router.post("/discover")
async def discover_influencers(request: InfluencerSearchRequest, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    print(f"Searching influencers for {client.name}")
    discovered = []
    
    if request.hashtags:
        hashtag_results = influencer_discovery.search_by_hashtag(request.hashtags, request.limit)
        for inf in hashtag_results[:10]:
            profile = influencer_discovery.analyze_profile(inf["username"])
            if profile and profile["followers"] >= request.min_followers:
                discovered.append(profile)
    
    return {
        "client": client.name,
        "total_found": len(discovered),
        "influencers": discovered
    }
