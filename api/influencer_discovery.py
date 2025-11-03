"""Influencer Discovery API"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import sys
sys.path.append('..')
from services.apify_service import search_instagram_profiles

router = APIRouter()

class InfluencerSearchRequest(BaseModel):
    search_query: Optional[str] = None
    location: Optional[str] = None
    usernames: Optional[List[str]] = None
    max_results: Optional[int] = 20

@router.post("/search")
async def search_influencers(request: InfluencerSearchRequest):
    """Influencer arama"""
    
    if not request.search_query and not request.usernames:
        raise HTTPException(status_code=400, detail="Search query veya usernames gerekli")
    
    result = await search_instagram_profiles(
        search_query=request.search_query,
        location=request.location,
        usernames=request.usernames,
        max_results=request.max_results
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=500, detail=result.get("error", "Error"))
    
    return result

@router.get("/locations")
async def get_locations():
    """Popüler konumlar"""
    return {
        "locations": [
            "İstanbul", "Ankara", "İzmir", "Antalya", "Bursa",
            "Turkey", "Dubai", "London", "New York"
        ]
    }
