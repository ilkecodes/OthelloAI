from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine
from datetime import datetime
import uuid
from config import settings

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

# ========== MODELS ==========

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)
    keywords = Column(JSON, nullable=True)
    platforms = Column(JSON, nullable=True)
    brand_guidelines = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Influencer(Base):
    __tablename__ = "influencers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, nullable=False)
    platform = Column(String, default="instagram")
    followers = Column(Integer, nullable=True)
    engagement_rate = Column(Float, nullable=True)
    bio = Column(Text, nullable=True)
    profile_pic = Column(String, nullable=True)
    profile_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    name = Column(String, nullable=False)
    campaign_type = Column(String)
    sector = Column(String)
    objectives = Column(JSON, nullable=True)
    sales_goals = Column(JSON, nullable=True)
    target_audience = Column(JSON, nullable=True)
    budget = Column(Float, nullable=True)
    platforms = Column(JSON, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)

class CampaignInfluencer(Base):
    __tablename__ = "campaign_influencers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    campaign_id = Column(String, ForeignKey("campaigns.id"), nullable=False)
    influencer_id = Column(String, ForeignKey("influencers.id"), nullable=False)
    agreed_price = Column(Float, nullable=True)
    deliverables = Column(JSON, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String, nullable=False)
    keyword = Column(String)
    platform = Column(String, default="instagram")
    post_count = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0.0)
    trending_score = Column(Float, default=0.0)
    scanned_at = Column(DateTime, default=datetime.utcnow)

class Content(Base):
    __tablename__ = "content"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    client_id = Column(String, nullable=False)
    platform = Column(String)
    text = Column(Text)
    status = Column(String, default="draft")
    scheduled_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ========== DATABASE CONNECTION ==========
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
