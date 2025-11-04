"""Influencer Stats API"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class SaveInfluencerRequest(BaseModel):
    username: str
    full_name: Optional[str] = None
    followers: Optional[int] = 0
    engagement_rate: Optional[float] = 0.0

@router.get("/saved")
async def get_saved_influencers():
    """Kaydedilen influencer'ları getir (şimdilik boş)"""
    return {
        "success": True,
        "influencers": []
    }

@router.post("/save")
async def save_influencer(request: SaveInfluencerRequest):
    """Influencer'ı kaydet (şimdilik mock)"""
    return {
        "success": True,
        "message": "Influencer saved"
    }

@router.get("/stats")
async def get_stats():
    """İstatistikler (şimdilik mock)"""
    return {
        "success": True,
        "stats": {
            "total_saved": 0,
            "total_campaigns": 0,
            "avg_engagement": 0
        }
    }
