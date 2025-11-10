"""Campaign management endpoints backed by the relational database."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.campaign import Campaign


class CampaignBase(BaseModel):
    name: str
    client_id: str
    campaign_type: str
    sector: str
    status: str = "planning"
    goals: List[str] = Field(default_factory=list)
    budget: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    sales_goal: Optional[str] = None
    awareness_goal: Optional[str] = None


class CampaignCreate(CampaignBase):
    """Payload accepted when creating a campaign."""


class CampaignResponse(CampaignBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


router = APIRouter()


@router.get("/", response_model=List[CampaignResponse])
def list_campaigns(
    client_id: Optional[str] = None,
    db: Session = Depends(get_db),
) -> List[Campaign]:
    """Return campaigns stored in the relational database."""

    query = db.query(Campaign)
    if client_id:
        query = query.filter(Campaign.client_id == client_id)

    return query.order_by(Campaign.created_at.desc()).all()


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)) -> Campaign:
    """Create a campaign persisted in the database."""

    campaign = Campaign(
        name=payload.name,
        client_id=payload.client_id,
        campaign_type=payload.campaign_type,
        sector=payload.sector,
        status=payload.status,
        goals=payload.goals,
        budget=payload.budget,
        start_date=payload.start_date,
        end_date=payload.end_date,
        sales_goal=payload.sales_goal,
        awareness_goal=payload.awareness_goal,
    )

    db.add(campaign)
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Kampanya veritabanına kaydedilemedi.",
        )

    db.refresh(campaign)
    return campaign
