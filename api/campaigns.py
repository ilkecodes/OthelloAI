"""Campaigns API - Basit CRUD"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from database import get_db, Campaign

router = APIRouter()

class CampaignCreate(BaseModel):
    client_id: str
    name: str
    campaign_type: str
    sector: str
    budget: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@router.get("/")
def get_campaigns(client_id: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        query = db.query(Campaign)
        if client_id:
            query = query.filter(Campaign.client_id == client_id)
        campaigns = query.all()
        return {
            "count": len(campaigns),
            "data": [
                {
                    "id": c.id,
                    "client_id": c.client_id,
                    "name": c.name,
                    "campaign_type": c.campaign_type,
                    "sector": c.sector,
                    "budget": c.budget,
                    "status": c.status,
                    "created_at": c.created_at.isoformat() if c.created_at else None
                }
                for c in campaigns
            ]
        }
    except Exception as e:
        print(f"ERROR: {e}")
        return {"count": 0, "data": []}

@router.post("/")
def create_campaign(campaign: CampaignCreate, db: Session = Depends(get_db)):
    try:
        db_campaign = Campaign(
            client_id=campaign.client_id,
            name=campaign.name,
            campaign_type=campaign.campaign_type,
            sector=campaign.sector,
            budget=campaign.budget,
            status="draft"
        )
        db.add(db_campaign)
        db.commit()
        db.refresh(db_campaign)
        return {
            "success": True,
            "id": db_campaign.id,
            "message": "Campaign created"
        }
    except Exception as e:
        print(f"ERROR: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
