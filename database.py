from sqlalchemy import create_engine, Column, String, DateTime, Boolean, JSON, Text, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# PostgreSQL bağlantısı
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    slug = Column(String, unique=True)
    keywords = Column(JSON)
    platforms = Column(JSON)
    brand_guidelines = Column(JSON)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Content(Base):
    __tablename__ = "content"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String)
    platform = Column(String)
    content_type = Column(String)
    text = Column(Text)
    media_url = Column(String)
    scheduled_time = Column(DateTime)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)

class Influencer(Base):
    __tablename__ = "influencers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True)
    platform = Column(String)
    followers = Column(String)
    engagement_rate = Column(String)
    bio = Column(Text)
    profile_pic = Column(String)
    profile_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String)
    name = Column(String)
    campaign_type = Column(String)
    objectives = Column(JSON)
    budget = Column(String)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)

class CampaignInfluencer(Base):
    __tablename__ = "campaign_influencers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String)
    influencer_id = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class Trend(Base):
    __tablename__ = "trends"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String)
    keyword = Column(String)
    platform = Column(String)
    post_count = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0.0)
    trending_score = Column(Float, default=0.0)
    extra_data = Column(JSON)
    scanned_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
