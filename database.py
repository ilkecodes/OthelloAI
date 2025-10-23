from sqlalchemy import create_engine, Column, String, Text, Integer, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/othelloai")
db_url = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")

engine = create_engine(db_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MODELS
class Client(Base):
    __tablename__ = "clients"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), unique=True)
    active = Column(Boolean, default=True)
    keywords = Column(JSON)
    platforms = Column(JSON)
    brand_guidelines = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)

class Trend(Base):
    __tablename__ = "trends"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, ForeignKey("clients.id"))
    platform = Column(String(50))
    keyword = Column(String(100))
    post_count = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0.0)
    trending_score = Column(Float, default=0.0)
    scanned_at = Column(DateTime, default=datetime.now)
    client = relationship("Client", backref="trends")

class Influencer(Base):
    __tablename__ = "influencers"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(100), unique=True, nullable=False)
    platform = Column(String(50), nullable=False)
    followers = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    bio = Column(Text)
    profile_pic = Column(String(500))
    profile_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)

class Content(Base):
    __tablename__ = "contents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"))
    platform = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    status = Column(String(20), default="draft")
    scheduled_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    client = relationship("Client", backref="contents")
