from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Campaign, Client
from services.influencer_service import influencer_discovery
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class CampaignInfluencerSearch(BaseModel):
    campaign_id: str
    sector: str
    goals: List[str]
    age_range: str
    gender: str
    location: str
    min_followers: int
    max_followers: int
    platforms: List[str]
    sales_goal: str
    budget_per_influencer: Optional[float] = None

@router.post("/search-for-campaign")
async def search_influencers_for_campaign(
    request: CampaignInfluencerSearch,
    db: Session = Depends(get_db)
):
    campaign = db.query(Campaign).filter(Campaign.id == request.campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    search_keywords = []
    if request.sector == "Gıda ve İçecek":
        search_keywords = ["food", "restaurant", "cafe", "yemek"]
    elif request.sector == "Moda ve Giyim":
        search_keywords = ["fashion", "style", "outfit", "moda"]
    elif request.sector == "Güzellik ve Kişisel Bakım":
        search_keywords = ["beauty", "skincare", "makeup", "güzellik"]
    elif request.sector == "Sağlık ve Fitness":
        search_keywords = ["fitness", "health", "workout", "yoga"]
    
    if request.location:
        search_keywords.append(request.location)
    
    print(f"Searching influencers for campaign: {campaign.name}")
    print(f"Keywords: {search_keywords}")
    
    discovered = []
    hashtag_results = influencer_discovery.search_by_hashtag(search_keywords[:3], limit=30)
    
    for inf in hashtag_results:
        profile = influencer_discovery.analyze_profile(inf["username"])
        if not profile:
            continue
        
        followers = profile["followers"]
        if followers < request.min_followers or followers > request.max_followers:
            continue
        
        score = 0
        if request.location.lower() in (profile.get("biography") or "").lower():
            score += 20
        if followers >= request.min_followers:
            score += 30
        if profile.get("engagement_rate", 0) > 3:
            score += 30
        
        tier = "A-Tier" if score >= 60 else "B-Tier" if score >= 40 else "C-Tier"
        
        discovered.append({
            "username": profile["username"],
            "followers": followers,
            "engagement_rate": profile.get("engagement_rate", 0),
            "biography": profile.get("biography", ""),
            "score": score,
            "tier": tier,
            "estimated_cost": followers * 0.01 if request.sales_goal == "Satış Odaklı" else followers * 0.005
        })
    
    discovered.sort(key=lambda x: x["score"], reverse=True)
    
    return {
        "campaign_name": campaign.name,
        "search_criteria": {
            "sector": request.sector,
            "location": request.location,
            "follower_range": f"{request.min_followers}-{request.max_followers}",
            "platforms": request.platforms
        },
        "total_found": len(discovered),
        "recommended_influencers": discovered[:15],
        "total_estimated_cost": sum(i["estimated_cost"] for i in discovered[:15])
    }

@router.get("/campaign-suggestions/{campaign_id}")
async def get_campaign_suggestions(campaign_id: str, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return {
        "campaign_types": [
            {
                "name": "Lokasyon Bazlı Kampanya",
                "description": "Fiziksel lokasyon ziyareti gerektiren influencer işbirikleri",
                "suitable_for": ["Restaurant", "Cafe", "Etkileşim"]
            },
            {
                "name": "Ürün Gönderimli Kampanya",
                "description": "Influencerlara ürün gönderimi yaparak tanıtım yapan kampanyalar",
                "suitable_for": ["Product", "Satış"]
            }
        ],
        "metrics": [
            "Erişim Sayısı",
            "Etkileşim Sayısı", 
            "Link Tıklama Sayısı",
            "Yorum Sayısı",
            "Beğeni Sayısı",
            "Paylaşım Sayısı"
        ]
    }
