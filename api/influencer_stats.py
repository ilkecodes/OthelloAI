"""Influencer Statistics Dashboard"""
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()

saved_influencers = []

class SavedInfluencer(BaseModel):
    username: str
    full_name: str
    followers: int
    engagement_rate: float
    notes: str = ""

@router.post("/save")
async def save_influencer(influencer: SavedInfluencer):
    """Influencer'ı kaydet"""
    
    # Zaten kayıtlı mı kontrol et
    if any(i["username"] == influencer.username for i in saved_influencers):
        return {"success": False, "message": "Zaten kayıtlı"}
    
    saved_influencers.append(influencer.dict())
    return {"success": True, "message": "Kaydedildi"}

@router.get("/saved")
async def get_saved_influencers():
    """Kaydedilen influencer'ları getir"""
    return {
        "success": True,
        "count": len(saved_influencers),
        "influencers": saved_influencers
    }

@router.get("/stats")
async def get_dashboard_stats():
    """Dashboard istatistikleri"""
    if not saved_influencers:
        return {
            "total_influencers": 0,
            "total_reach": 0,
            "avg_engagement": 0
        }
    
    total_followers = sum(i["followers"] for i in saved_influencers)
    avg_engagement = sum(i["engagement_rate"] for i in saved_influencers) / len(saved_influencers)
    
    return {
        "total_influencers": len(saved_influencers),
        "total_reach": total_followers,
        "avg_engagement": round(avg_engagement, 2)
    }

@router.delete("/remove/{username}")
async def remove_influencer(username: str):
    """Influencer'ı sil"""
    global saved_influencers
    saved_influencers = [i for i in saved_influencers if i["username"] != username]
    return {"success": True, "message": "Silindi"}
