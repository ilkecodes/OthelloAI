from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, JSON, String

from ..database import Base


def _generate_uuid() -> str:
    return str(uuid4())


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String(36), primary_key=True, default=_generate_uuid)
    client_id = Column(String, nullable=False)
    name = Column(String(200), nullable=False)
    campaign_type = Column(String(50), nullable=False)
    sector = Column(String(100), nullable=False)
    status = Column(String(50), default="planning", nullable=False)
    goals = Column(JSON, default=list)
    budget = Column(Float, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    sales_goal = Column(String(200), nullable=True)
    awareness_goal = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict[str, object | None]:
        """Return a serialisable representation for debugging."""

        return {
            "id": self.id,
            "client_id": self.client_id,
            "name": self.name,
            "campaign_type": self.campaign_type,
            "sector": self.sector,
            "status": self.status,
            "goals": self.goals,
            "budget": self.budget,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "sales_goal": self.sales_goal,
            "awareness_goal": self.awareness_goal,
            "created_at": self.created_at,
        }
