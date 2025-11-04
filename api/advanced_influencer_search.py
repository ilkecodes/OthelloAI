"""Advanced Influencer Search API"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
sys.path.append('..')
from services.advanced_influencer_search import advanced_influencer_search

router = APIRouter()

class AdvancedSearchRequest(BaseModel):
    search_query: str
    location: Optional[str] = None
    min_quality_score: Optional[int] = 40

@router.post("/advanced-search")
async def search_advanced(request: AdvancedSearchRequest):
    """
    🚀 TAM SİSTEM - Advanced Influencer Search
    
    Features:
    - AI-generated smart hashtags
    - Parallel multi-hashtag search
    - Bio & content analysis with OpenAI
    - Quality scoring (0-100)
    - Authenticity checking
    - Bot detection
    """
    
    if not request.search_query:
        raise HTTPException(status_code=400, detail="Search query required")
    
    result = await advanced_influencer_search(
        search_query=request.search_query,
        location=request.location,
        min_quality_score=request.min_quality_score
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=500, 
            detail=result.get("error", "Search failed")
        )
    
    return result

@router.get("/search-info")
async def get_search_info():
    """Search system bilgisi"""
    return {
        "system": "Advanced AI-Powered Influencer Search",
        "version": "2.0",
        "features": [
            "AI hashtag generation",
            "Parallel multi-hashtag search (5 hashtags)",
            "OpenAI bio analysis",
            "OpenAI content consistency check",
            "Quality scoring (0-100)",
            "Authenticity verification",
            "Bot follower detection",
            "Engagement pod detection"
        ],
        "scoring": {
            "bio_match": 30,
            "content_match": 30,
            "engagement": 20,
            "authenticity": 10,
            "activity": 10,
            "total": 100
        }
    }
