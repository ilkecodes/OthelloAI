from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from database import get_db, Campaign, CampaignInfluencer

router = APIRouter()

# Schemas
class CampaignObjectives(BaseModel):
    marka_bilinirlik: Optional[List[str]] = []
    sosyal_medya_hesap: Optional[List[str]] = []
    sosyal_medya_gonderi: Optional[List[str]] = []
    lokasyon_bilinirlik: Optional[List[str]] = []
    urun_bilinirlik: Optional[List[str]] = []

class SalesGoals(BaseModel):
    satis_hedefi: Optional[str] = None  # perakende, online, fiziksel, etc.
    alt_satis_hedefi: Optional[str] = None
    onemli_metrikler: Optional[List[str]] = []  # erisim, etkilesim, link tiklama, etc.

class TargetAudience(BaseModel):
    cinsiyet: Optional[str] = None
    yas: Optional[str] = None
    takipci: Optional[str] = None
    platform: Optional[List[str]] = []

class CampaignCreate(BaseModel):
    client_id: str
    name: str
    campaign_type: str  # "awareness" or "sales"
    sector: str
    objectives: Optional[CampaignObjectives] = None
    sales_goals: Optional[SalesGoals] = None
    target_audience: Optional[TargetAudience] = None
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class CampaignResponse(BaseModel):
    id: str
    client_id: str
    name: str
    campaign_type: str
    sector: str
    objectives: Optional[Dict] = None
    sales_goals: Optional[Dict] = None
    target_audience: Optional[Dict] = None
    budget: Optional[float] = None
    platforms: Optional[Dict] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AddInfluencerToCampaign(BaseModel):
    campaign_id: str
    influencer_id: str
    agreed_price: Optional[float] = None
    deliverables: Optional[Dict] = None

# Endpoints
@router.get("/", response_model=List[CampaignResponse])
def get_campaigns(client_id: Optional[str] = None, db: Session = Depends(get_db)):
    if not db:
        return []
    
    query = db.query(Campaign)
    if client_id:
        query = query.filter(Campaign.client_id == client_id)
    
    return query.all()

@router.post("/", response_model=CampaignResponse)
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    db_campaign = Campaign(
        client_id=campaign.client_id,
        name=campaign.name,
        campaign_type=campaign.campaign_type,
        sector=campaign.sector,
        objectives=campaign.objectives.dict() if campaign.objectives else {},
        sales_goals=campaign.sales_goals.dict() if campaign.sales_goals else {},
        target_audience=campaign.target_audience.dict() if campaign.target_audience else {},
        budget=campaign.budget,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        status="draft"
    )
    
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    
    return db_campaign

@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: str, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    return campaign

@router.put("/{campaign_id}/status")
def update_campaign_status(
    campaign_id: str, 
    status: str,
    db: Session = Depends(get_db)
):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign.status = status
    db.commit()
    
    return {"message": f"Campaign status updated to {status}"}

@router.post("/add-influencer")
def add_influencer_to_campaign(data: AddInfluencerToCampaign, db: Session = Depends(get_db)):
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    campaign_influencer = CampaignInfluencer(
        campaign_id=data.campaign_id,
        influencer_id=data.influencer_id,
        agreed_price=data.agreed_price,
        deliverables=data.deliverables or {},
        status="invited"
    )
    
    db.add(campaign_influencer)
    db.commit()
    
    return {"message": "Influencer added to campaign", "id": campaign_influencer.id}

@router.get("/{campaign_id}/influencers")
def get_campaign_influencers(campaign_id: str, db: Session = Depends(get_db)):
    if not db:
        return []
    
    return db.query(CampaignInfluencer).filter(
        CampaignInfluencer.campaign_id == campaign_id
    ).all()
