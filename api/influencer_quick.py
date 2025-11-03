"""Quick Influencer Discovery API"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from services.influencer_service import InfluencerDiscovery

router = APIRouter()
discovery = InfluencerDiscovery()

# ---------- Schemas ----------
class HashtagDiscoverRequest(BaseModel):
    hashtags: List[str] = Field(..., description="örn: ['ivf','kadindogum','izmir']")
    min_followers: Optional[int] = 10000
    max_followers: Optional[int] = 500000
    limit: Optional[int] = 10

class BioDiscoverRequest(BaseModel):
    query: str = Field(..., description="örn: 'ivf doctor izmir' / 'bio: fizyoterapi'")
    min_followers: Optional[int] = 5000
    max_followers: Optional[int] = 1000000
    limit: Optional[int] = 20

class LocationDiscoverRequest(BaseModel):
    location_query: str = Field(..., description="örn: 'Izmir', 'Nisantasi', 'Etiler'")
    min_followers: Optional[int] = 2000
    max_followers: Optional[int] = 1000000
    limit: Optional[int] = 20

class AnalyzeRequest(BaseModel):
    username: str

# ---------- Endpoints ----------
@router.post("/quick-discover/hashtags")
async def quick_discover_by_hashtags(req: HashtagDiscoverRequest):
    try:
        data = await discovery.find_niche_influencers(
            hashtags=req.hashtags,
            min_followers=req.min_followers,
            max_followers=req.max_followers,
            limit=req.limit
        )
        if not data:
            raise HTTPException(status_code=404, detail="Uygun influencer bulunamadı.")
        return {"success": True, "count": len(data), "influencers": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quick-discover/bio")
async def quick_discover_by_bio(req: BioDiscoverRequest):
    try:
        data = await discovery.find_influencers_by_bio(
            query=req.query,
            min_followers=req.min_followers,
            max_followers=req.max_followers,
            limit=req.limit
        )
        if not data:
            raise HTTPException(status_code=404, detail="Eşleşen influencer bulunamadı.")
        return {"success": True, "count": len(data), "influencers": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quick-discover/location")
async def quick_discover_by_location(req: LocationDiscoverRequest):
    try:
        data = await discovery.find_influencers_by_location(
            location_query=req.location_query,
            min_followers=req.min_followers,
            max_followers=req.max_followers,
            limit=req.limit
        )
        if not data:
            raise HTTPException(status_code=404, detail="Konuma göre uygun influencer bulunamadı.")
        return {"success": True, "count": len(data), "influencers": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_influencer(req: AnalyzeRequest):
    try:
        result = await discovery.analyze_influencer_content(req.username)
        if not result:
            raise HTTPException(status_code=404, detail="Analiz yapılamadı.")
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
