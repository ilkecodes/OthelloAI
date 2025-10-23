from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from database import engine, Base, Client, Trend, Influencer, Content
from database import BrandCorpus, BrandVoiceProfile, GeneratedContent, ContentFeedback

# ESKİ BRAND VOICE TABLOLARINI SİL
print("🗑️  Cleaning old Brand Voice tables...")
from sqlalchemy import text
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS content_feedback CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS generated_contents CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS brand_voice_profiles CASCADE;"))
    conn.execute(text("DROP TABLE IF EXISTS brand_corpus CASCADE;"))
    conn.commit()
print("✅ Old tables dropped")

print("📊 Creating fresh database tables...")
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
from brand_voice_api import router as brand_voice_router

app.include_router(clients_router, prefix="/api/clients", tags=["clients"])
app.include_router(trends_router, prefix="/api/trends", tags=["trends"])
app.include_router(content_router, prefix="/api/content", tags=["content"])
app.include_router(influencers_router, prefix="/api/influencers", tags=["influencers"])
app.include_router(brand_voice_router, prefix="/api/brand-voice", tags=["brand-voice"])

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "OthelloAI Marketing Platform API",
        "version": "2.0.0",
        "features": ["clients", "trends", "content", "influencers", "brand-voice"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
