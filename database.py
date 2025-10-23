from sqlalchemy import create_engine, Column, String, Text, Integer, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid
import os

# Database URL
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

# ============= MODELS =============

class Client(Base):
    """Müşteriler"""
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
    """Trendler"""
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
    """Influencer'lar"""
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
    """Üretilen içerikler"""
    __tablename__ = "contents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"))
    platform = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    status = Column(String(20), default="draft")
    scheduled_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    
    client = relationship("Client", backref="contents")

# ============= BRAND VOICE MODELS =============

class BrandCorpus(Base):
    """Marka içerikleri - Instagram, Twitter, blog posts vb."""
    __tablename__ = "brand_corpus"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    content_type = Column(String(50))
    text_content = Column(Text, nullable=False)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    
    client = relationship("Client", backref="corpus_items")

class BrandVoiceProfile(Base):
    """AI tarafından çıkarılan marka sesi profili"""
    __tablename__ = "brand_voice_profiles"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False, unique=True)
    
    tone = Column(String(100))
    language_style = Column(String(100))
    emoji_usage = Column(String(50))
    content_themes = Column(JSON)
    brand_personality = Column(JSON)
    hashtag_strategy = Column(String(200))
    
    sample_size = Column(Integer, default=0)
    confidence_score = Column(Float, default=0.0)
    voice_summary = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    client = relationship("Client", backref="brand_voice")

class GeneratedContent(Base):
    """Üretilen içerikler ve performansları"""
    __tablename__ = "generated_contents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id = Column(String, ForeignKey("clients.id"), nullable=False)
    profile_id = Column(String, ForeignKey("brand_voice_profiles.id"))
    
    platform = Column(String(50), nullable=False)
    content_text = Column(Text, nullable=False)
    prompt_used = Column(Text)
    
    user_rating = Column(Integer)
    is_approved = Column(String(20), default="pending")
    feedback_notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)
    
    client = relationship("Client", backref="generated_contents")
    profile = relationship("BrandVoiceProfile", backref="generated_contents")

class ContentFeedback(Base):
    """İçerik feedback sistemi"""
    __tablename__ = "content_feedback"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content_id = Column(String, ForeignKey("generated_contents.id"))
    client_id = Column(String, ForeignKey("clients.id"))
    
    rating = Column(Integer)
    feedback_type = Column(String(50))
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)
    
    content = relationship("GeneratedContent", backref="feedback_items")
    client = relationship("Client", backref="feedback_items")
