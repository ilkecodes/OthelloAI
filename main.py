from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from database import engine, Base

# Basit modeller - sadece eskiler
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

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

print("📊 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created")

app = FastAPI(
    title="OthelloAI Marketing Platform",
    version="2.0.0",
    redirect_slashes=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from api.clients import router as clients_router
from api.trends import router as trends_router
from api.content import router as content_router
from api.influencers import router as influencers_router

app.include_router(clients_router, prefix="/api/clients", tags=["clients"])
app.include_router(trends_router, prefix="/api/trends", tags=["trends"])
app.include_router(content_router, prefix="/api/content", tags=["content"])
app.include_router(influencers_router, prefix="/api/influencers", tags=["influencers"])

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "OthelloAI Marketing Platform API",
        "version": "2.0.0",
        "features": ["clients", "trends", "content", "influencers"],
        "apify_configured": bool(os.getenv("APIFY_API_TOKEN")),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
