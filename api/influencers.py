from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel
from database import get_db, Influencer
from services.apify_service import apify_service

router = APIRouter()

class InfluencerFilters(BaseModel):
    # Arama yöntemi
    search_type: str  # "hashtag", "username", "niche"
    search_value: str
    
    # Filtreler
    min_followers: Optional[int] = None
    max_followers: Optional[int] = None
    min_engagement: Optional[float] = None
    location: Optional[str] = None
    verified_only: Optional[bool] = False
    business_only: Optional[bool] = False
    
    limit: int = 20

class InfluencerResponse(BaseModel):
    id: str
    username: str
    platform: str
    followers: int
    engagement_rate: float
    bio: Optional[str] = None
    profile_pic: Optional[str] = None
    is_verified: Optional[bool] = False
    is_business: Optional[bool] = False
    posts_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

@router.post("/search")
async def search_influencers(filters: InfluencerFilters, db: Session = Depends(get_db)):
    """Advanced influencer search with filters"""
    
    # Apify'dan veri çek
    if filters.search_type == "hashtag":
        raw_results = await apify_service.search_by_hashtag(
            hashtag=filters.search_value,
            limit=filters.limit * 2  # Filtreleme için fazladan çek
        )
    elif filters.search_type == "username":
        raw_results = await apify_service.search_instagram_profiles(
            usernames=[filters.search_value],
            limit=filters.limit
        )
    else:
        # Niche search - multiple hashtags
        niche_hashtags = {
            "moda": ["fashion", "style", "ootd", "moda"],
            "guzellik": ["beauty", "makeup", "skincare", "guzellik"],
            "yemek": ["food", "foodie", "yemek", "mutfak"],
            "saglik": ["health", "fitness", "wellness", "saglik"],
            "seyahat": ["travel", "wanderlust", "seyahat"]
        }
        hashtag = niche_hashtags.get(filters.search_value.lower(), [filters.search_value])[0]
        raw_results = await apify_service.search_by_hashtag(hashtag=hashtag, limit=filters.limit * 2)
    
    # Filtreleme uygula
    filtered_results = []
    for result in raw_results:
        if "error" in result:
            continue
            
        followers = result.get("followers", 0)
        
        # Takipçi filtresi
        if filters.min_followers and followers < filters.min_followers:
            continue
        if filters.max_followers and followers > filters.max_followers:
            continue
        
        # Engagement hesapla
        likes = result.get("likes", 0)
        comments = result.get("comments", 0)
        engagement_rate = ((likes + comments) / followers * 100) if followers > 0 else 0
        
        # Engagement filtresi
        if filters.min_engagement and engagement_rate < filters.min_engagement:
            continue
        
        # Verified filtresi
        if filters.verified_only and not result.get("is_verified", False):
            continue
        
        # Business filtresi
        if filters.business_only and not result.get("is_business", False):
            continue
        
        result["engagement_rate"] = round(engagement_rate, 2)
        filtered_results.append(result)
    
    # Limit uygula
    filtered_results = filtered_results[:filters.limit]
    
    # Database'e kaydet
    if db and filtered_results:
        for result in filtered_results:
            influencer = Influencer(
                username=result.get("username"),
                platform="instagram",
                followers=result.get("followers", 0),
                engagement_rate=result.get("engagement_rate", 0),
                bio=result.get("biography") or result.get("bio"),
                profile_pic=result.get("profile_pic_url"),
                profile_metadata={
                    "is_verified": result.get("is_verified", False),
                    "is_business": result.get("is_business", False),
                    "posts": result.get("posts", 0),
                    "full_name": result.get("full_name")
                }
            )
            db.merge(influencer)  # merge yerine add kullanırsak duplicate olur
        
        try:
            db.commit()
        except:
            db.rollback()
    
    return {
        "results": filtered_results,
        "count": len(filtered_results),
        "filters_applied": {
            "min_followers": filters.min_followers,
            "max_followers": filters.max_followers,
            "min_engagement": filters.min_engagement
        }
    }

@router.get("/", response_model=List[InfluencerResponse])
def get_all_influencers(db: Session = Depends(get_db)):
    """Get saved influencers from database"""
    if not db:
        return []
    return db.query(Influencer).limit(50).all()

@router.get("/{influencer_id}", response_model=InfluencerResponse)
def get_influencer(influencer_id: str, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    influencer = db.query(Influencer).filter(Influencer.id == influencer_id).first()
    if not influencer:
        raise HTTPException(status_code=404, detail="Influencer not found")
    return influencer
