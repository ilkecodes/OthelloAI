from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

from database import engine, Base

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

# ROUTER'LAR
from api.clients import router as clients_router
from api.trends import router as trends_router
from api.content import router as content_router
from api.influencers import router as influencers_router
from brand_voice_api import router as brand_voice_router
from api.simple_content import router as simple_content_router
from api.influencer_discovery import router as influencer_discovery_router
from api.influencer_stats import router as influencer_stats_router
from api.advanced_influencer_search import router as advanced_search_router
from api.trend_dashboard import router as trend_dashboard_router

# ROUTER'LARI EKLE
app.include_router(clients_router, prefix="/api/clients", tags=["clients"])
app.include_router(trends_router, prefix="/api/trends-old", tags=["trends-old"])
app.include_router(content_router, prefix="/api/content", tags=["content"])
app.include_router(influencers_router, prefix="/api/influencers", tags=["influencers"])
app.include_router(brand_voice_router, prefix="/api/brand-voice", tags=["brand-voice"])
app.include_router(simple_content_router, prefix="/api/content", tags=["simple-content"])
app.include_router(influencer_discovery_router, prefix="/api/influencer-discovery", tags=["influencer-discovery"])
app.include_router(influencer_stats_router, prefix="/api/influencer-stats", tags=["influencer-stats"])
app.include_router(advanced_search_router, prefix="/api/advanced-search", tags=["advanced-search"])
app.include_router(trend_dashboard_router, prefix="/api/trends", tags=["trend-dashboard"])

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "OthelloAI Marketing Platform API",
        "version": "2.0.0",
        "features": ["clients", "trends", "content", "influencers", "brand-voice", "influencer-discovery", "advanced-search"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
