from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db, Influencer
from services.apify_service import apify_service

router = APIRouter()

class InfluencerSearch(BaseModel):
    usernames: Optional[List[str]] = None
    hashtag: Optional[str] = None
    limit: int = 10

class InfluencerResponse(BaseModel):
    id: str
    username: str
    platform: str
    followers: int
    engagement_rate: float
    data: dict
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[InfluencerResponse])
def get_influencers(db: Session = Depends(get_db)):
    if not db:
        return []
    return db.query(Influencer).all()

@router.post("/search")
async def search_influencers(search: InfluencerSearch, db: Session = Depends(get_db)):
    """Search influencers using Apify"""
    
    if search.hashtag:
        results = await apify_service.search_by_hashtag(
            hashtag=search.hashtag,
            limit=search.limit
        )
    elif search.usernames:
        results = await apify_service.search_instagram_profiles(
            usernames=search.usernames,
            limit=search.limit
        )
    else:
        raise HTTPException(status_code=400, detail="Provide either usernames or hashtag")
    
    # Save to database if available
    if db and results and "error" not in results[0]:
        for result in results:
            # Calculate simple engagement rate
            followers = result.get("followers", 1)
            likes = result.get("likes", 0)
            comments = result.get("comments", 0)
            engagement_rate = ((likes + comments) / followers * 100) if followers > 0 else 0
            
            influencer = Influencer(
                username=result.get("username"),
                platform="instagram",
                followers=followers,
                engagement_rate=round(engagement_rate, 2),
                data=result
            )
            db.add(influencer)
        
        db.commit()
    
    return {
        "results": results,
        "count": len(results),
        "saved_to_db": db is not None
    }

@router.get("/{influencer_id}", response_model=InfluencerResponse)
def get_influencer(influencer_id: str, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    influencer = db.query(Influencer).filter(Influencer.id == influencer_id).first()
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")
    return influencer
