from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables FIRST
load_dotenv()

from database import engine, Base, Client, Trend, Influencer, Content
from database import BrandCorpus, BrandVoiceProfile, GeneratedContent, ContentFeedback

# Import routers
from clients import router as clients_router
from trends import router as trends_router
from content import router as content_router
from influencers import router as influencers_router
from brand_voice_api import router as brand_voice_router

# Create tables
print("📊 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created")

app = FastAPI(
    title="OthelloAI Marketing Platform",
    version="2.0.0",
    description="AI-Powered Marketing Platform with Brand Voice Intelligence",
    redirect_slashes=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(clients_router, prefix="/api/clients", tags=["clients"])
app.include_router(trends_router, prefix="/api/trends", tags=["trends"])
app.include_router(content_router, prefix="/api/content", tags=["content"])
app.include_router(influencers_router, prefix="/api/influencers", tags=["influencers"])
app.include_router(brand_voice_router, prefix="/api/brand-voice", tags=["brand-voice"])

print("✅ API routes loaded")

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "OthelloAI Marketing Platform API",
        "version": "2.0.0",
        "features": [
            "clients",
            "trends", 
            "content",
            "influencers",
            "brand-voice"
        ],
        "apify_configured": bool(os.getenv("APIFY_API_TOKEN")),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_services": "ready"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
