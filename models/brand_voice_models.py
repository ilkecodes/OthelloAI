"""
Brand Voice Models - İzole, mevcut models'e dokunmaz
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import TypeDecorator
from datetime import datetime
from database import Base

class Vector(TypeDecorator):
    """PostgreSQL vector type for embeddings"""
    impl = Text
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return "[" + ",".join(f"{x:.6f}" for x in value) + "]"
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        s = value.strip("[]")
        return [float(x) for x in s.split(",")] if s else []

class BrandCorpus(Base):
    __tablename__ = "brand_corpus"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String, nullable=False, index=True)
    source = Column(String, default="instagram")
    text = Column(Text, nullable=False)
    url = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)
    engagement_score = Column(Float, default=0.0)

class BrandVoiceProfile(Base):
    __tablename__ = "brand_voice_profiles"
    
    client_id = Column(String, primary_key=True)
    profile = Column(JSONB, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class BrandEmbedding(Base):
    __tablename__ = "brand_embeddings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String, index=True, nullable=False)
    text = Column(Text, nullable=False)
    vector = Column(Vector)

class GenOutput(Base):
    __tablename__ = "gen_outputs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String, index=True, nullable=False)
    request_payload = Column(JSONB, nullable=False)
    output = Column(JSONB, nullable=False)
    scores = Column(JSONB, default={})
    ts = Column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    gen_output_id = Column(Integer, nullable=False)
    field = Column(String)
    action = Column(String, nullable=False)
    comment = Column(Text)
    user_id = Column(String)
    ts = Column(DateTime, default=datetime.utcnow)
