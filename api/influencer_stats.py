"""Influencer Statistics Dashboard"""
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Basit in-memory storage (production'da database kullan)
saved_influencers = []

class SavedInfluencer(BaseModel):
    username: str
    full_name: str
    followers: int
    engagement_rate: float
    category: str = "uncategorized"
    notes: str = ""

@router.post("/save")
async def save_influencer(influencer: SavedInfluencer):
    """Influencer'ı kaydet"""
    saved_influencers.append(influencer.dict())
    return {"success": True, "message": "Influencer kaydedildi"}

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
            "avg_engagement": 0,
            "top_categories": []
        }
    
    total_followers = sum(i["followers"] for i in saved_influencers)
    avg_engagement = sum(i["engagement_rate"] for i in saved_influencers) / len(saved_influencers)
    
    # Kategori bazlı gruplandırma
    categories = {}
    for inf in saved_influencers:
        cat = inf.get("category", "uncategorized")
        categories[cat] = categories.get(cat, 0) + 1
    
    return {
        "total_influencers": len(saved_influencers),
        "total_reach": total_followers,
        "avg_engagement": round(avg_engagement, 2),
        "top_categories": [{"name": k, "count": v} for k, v in categories.items()]
    }

@router.delete("/clear")
async def clear_saved_influencers():
    """Tüm kayıtları temizle"""
    saved_influencers.clear()
    return {"success": True, "message": "Tüm kayıtlar silindi"}
