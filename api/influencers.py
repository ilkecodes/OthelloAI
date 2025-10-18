"""Influencers API - Influencer Keşfi"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from database import get_db, Influencer, Client
from services import apify_service

router = APIRouter()

class InfluencerSearchRequest(BaseModel):
    search_type: str
    client_id: Optional[str] = None
    niche_keywords: List[str] = []
    min_followers: Optional[int] = 10000
    max_followers: Optional[int] = 500000
    min_engagement: Optional[float] = 2.0
    limit: Optional[int] = 20

@router.post("/search")
async def search_influencers(request: InfluencerSearchRequest, db: Session = Depends(get_db)):
    if request.search_type == "client_based":
        if not request.client_id:
            raise HTTPException(status_code=400, detail="client_id required")
        
        client = db.query(Client).filter(Client.id == request.client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")
        
        print(f"🔍 Searching for: {client.name}")
        
        client_keywords = []
        if client.keywords and client.keywords.get("keywords"):
            client_keywords = client.keywords["keywords"]
        
        if client.brand_guidelines and client.brand_guidelines.get("industry"):
            industry = client.brand_guidelines["industry"]
            industry_map = {
                "Healthcare": ["health", "wellness", "medical"],
                "Food & Beverage": ["food", "foodie", "restaurant"],
                "Fashion": ["fashion", "style", "ootd"],
                "Beauty": ["beauty", "makeup", "skincare"],
            }
            client_keywords.extend(industry_map.get(industry, []))
        
        search_keywords = list(set(client_keywords + request.niche_keywords))[:5]
    else:
        if not request.niche_keywords:
            raise HTTPException(status_code=400, detail="niche_keywords required")
        search_keywords = request.niche_keywords
    
    print(f"📌 Keywords: {search_keywords}")
    
    influencers = await apify_service.search_influencers_by_niche(
        niche_keywords=search_keywords,
        min_followers=request.min_followers or 10000,
        max_followers=request.max_followers or 500000,
        limit=request.limit or 20
    )
    
    if not influencers:
        return {
            "message": "No influencers found",
            "search_type": request.search_type,
            "keywords": search_keywords,
            "results": []
        }
    
    if request.min_engagement:
        influencers = [inf for inf in influencers if inf["engagement_rate"] >= request.min_engagement]
    
    results = []
    for inf in influencers:
        tier = inf["tier"]
        engagement = inf["engagement_rate"]
        
        if tier == "A-Tier":
            rec = f"⭐ YÜKSEK KALİTE! {engagement:.1f}% engagement."
        elif tier == "B-Tier":
            rec = f"✅ İYİ SEÇENEK: {engagement:.1f}% engagement."
        else:
            rec = f"⚠️ DİKKATLİ: {engagement:.1f}% düşük."
        
        results.append({
            "username": inf["username"],
            "followers": inf["followers"],
            "engagement_rate": inf["engagement_rate"],
            "tier": inf["tier"],
            "niche": inf["niche"],
            "profile_url": inf["profile_url"],
            "recommendation": rec
        })
    
    print(f"✅ Found {len(results)} influencers")
    
    return {
        "message": f"Found {len(results)} influencers",
        "search_type": request.search_type,
        "keywords": search_keywords,
        "results": results
    }

@router.get("/")
async def get_saved_influencers(db: Session = Depends(get_db)):
    influencers = db.query(Influencer).order_by(Influencer.followers.desc()).limit(50).all()
    return {
        "count": len(influencers),
        "influencers": [
            {
                "id": inf.id,
                "username": inf.username,
                "followers": inf.followers,
                "engagement_rate": inf.engagement_rate,
                "profile_url": f"https://instagram.com/{inf.username}"
            }
            for inf in influencers
        ]
    }
