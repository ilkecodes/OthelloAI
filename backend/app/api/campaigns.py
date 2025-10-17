"""Temporary in-memory campaigns API for the dashboard."""

from __future__ import annotations

from datetime import datetime
from threading import Lock
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field


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


class Campaign(CampaignBase):
    id: str
    created_at: datetime


class CampaignCreate(CampaignBase):
    """Payload accepted when creating a campaign."""


router = APIRouter()

_campaigns_lock = Lock()
_campaigns: List[Campaign] = [
    Campaign(
        id=str(uuid4()),
        name="Lansman Kampanyası",
        client_id="demo-client",
        campaign_type="awareness",
        sector="Teknoloji",
        status="active",
        goals=["Erişim Sayısı", "Etkileşim Sayısı"],
        budget=12500.0,
        start_date=datetime(2024, 1, 15),
        end_date=datetime(2024, 2, 15),
        sales_goal=None,
        awareness_goal="Marka bilinirliğini %20 artır",
        created_at=datetime(2024, 1, 10, 8, 30),
    ),
    Campaign(
        id=str(uuid4()),
        name="Bahar İndirimi",
        client_id="demo-client",
        campaign_type="sales",
        sector="Giyim",
        status="planning",
        goals=["Online Satış"],
        budget=9800.0,
        start_date=datetime(2024, 3, 1),
        end_date=datetime(2024, 3, 31),
        sales_goal="Online Satış",
        awareness_goal=None,
        created_at=datetime(2024, 2, 20, 9, 15),
    ),
]


@router.get("/", response_model=List[Campaign])
async def list_campaigns(client_id: Optional[str] = None) -> List[Campaign]:
    """Return the in-memory campaigns list, optionally filtered by client."""

    with _campaigns_lock:
        campaigns = list(_campaigns)

    if client_id:
        campaigns = [campaign for campaign in campaigns if campaign.client_id == client_id]

    return campaigns


@router.post("/", response_model=Campaign, status_code=201)
async def create_campaign(payload: CampaignCreate) -> Campaign:
    """Create a campaign in the in-memory store."""

    new_campaign = Campaign(
        id=str(uuid4()),
        created_at=datetime.utcnow(),
        **payload.model_dump(),
    )

    with _campaigns_lock:
        _campaigns.append(new_campaign)

    return new_campaign
