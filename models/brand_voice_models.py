from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class BrandCorpus(Base):
    __tablename__ = "brand_corpus"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(String(100), nullable=False, index=True)
    source = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    url = Column(String(500))
    engagement_score = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    embeddings = relationship("BrandEmbedding", back_populates="corpus", cascade="all, delete-orphan")

class BrandVoiceProfile(Base):
    __tablename__ = "brand_voice_profiles"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(String(100), unique=True, nullable=False)
    profile = Column(JSONB, default={})
    created_at = Column(TIMESTAMP, default=datetime.now)
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now)

class BrandEmbedding(Base):
    __tablename__ = "brand_embeddings"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(String(100), nullable=False, index=True)
    corpus_id = Column(Integer, ForeignKey("brand_corpus.id", ondelete="CASCADE"), nullable=True)
    text = Column(Text, nullable=False)
    source = Column(String(50))
    embedding = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    corpus = relationship("BrandCorpus", back_populates="embeddings")

class GenOutput(Base):
    __tablename__ = "gen_outputs"
    
    id = Column(Integer, primary_key=True)
    client_id = Column(String(100), nullable=False, index=True)
    platform = Column(String(50), nullable=False)
    content_type = Column(String(50), nullable=False)
    topic = Column(String(200))
    goal = Column(String(100))
    request_payload = Column(JSONB, default={})
    output = Column(JSONB, default={})
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    feedbacks = relationship("Feedback", back_populates="output", cascade="all, delete-orphan")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True)
    output_id = Column(Integer, ForeignKey("gen_outputs.id", ondelete="CASCADE"), index=True)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.now)
    
    output = relationship("GenOutput", back_populates="feedbacks")
