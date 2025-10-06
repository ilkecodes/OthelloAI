from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid
from config import settings


Base = declarative_base()

try:
    engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("✓ Database engine created")
except Exception as e:
    print(f"⚠ Database connection failed: {e}")
    engine = None
    SessionLocal = None

class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    active = Column(Boolean, default=True)
    trends = relationship("Trend", back_populates="client")
    keywords = Column(JSON)
    platforms = Column(JSON)
    brand_guidelines = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Content(Base):
    __tablename__ = "content"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    text = Column(Text)
    status = Column(String, default="draft")
    scheduled_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Influencer(Base):
    __tablename__ = "influencers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    followers = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    if SessionLocal:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None

def init_db():
    if engine:
        try:
            Base.metadata.create_all(bind=engine)
            print("✓ Database tables created")
        except Exception as e:
            print(f"⚠ Could not create tables: {e}")
    else:
        print("⚠ Database not configured")

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    campaign_type = Column(String, nullable=False)  # awareness, sales
    sector = Column(String)
    objectives = Column(JSON)  # bilinirlik hedefleri
    sales_goals = Column(JSON)  # satış hedefleri
    target_audience = Column(JSON)
    budget = Column(Float)
    metrics = Column(JSON)  # erişim, etkileşim, link tıklama, vb.
    platforms = Column(JSON)  # instagram, tiktok
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String, default="draft")  # draft, active, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CampaignInfluencer(Base):
    __tablename__ = "campaign_influencers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    campaign_id = Column(String, nullable=False)
    influencer_id = Column(String, nullable=False)
    status = Column(String, default="invited")  # invited, accepted, rejected, completed
    agreed_price = Column(Float)
    deliverables = Column(JSON)  # post count, story count, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, ForeignKey("clients.id"))
    keyword = Column(String, index=True)
    platform = Column(String)  # instagram, facebook, tiktok
    post_count = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0.0)
    trending_score = Column(Float, default=0.0)
    extra_data = Column(Text)  # JSON: sample posts, hashtags, etc
    scanned_at = Column(DateTime, default=datetime.utcnow)
    
    client = relationship("Client", back_populates="trends")

# Client model'e relationship ekle (Client class'ının içine)
# trends = relationship("Trend", back_populates="client")
