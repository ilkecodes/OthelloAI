from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from api import clients, content, trends, influencers, campaigns, influencer_discovery, campaign_influencer

# Database tables oluştur
Base.metadata.create_all(bind=engine)
print("✓ Database tables created")

app = FastAPI(
    title="OthelloAI Marketing Platform",
    description="AI-powered marketing automation platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(trends.router, prefix="/api/trends", tags=["trends"])
app.include_router(influencers.router, prefix="/api/influencers", tags=["influencers"])
app.include_router(influencer_discovery.router, prefix="/api/influencer-discovery", tags=["influencer-discovery"])
app.include_router(campaign_influencer.router, prefix="/api/campaign-influencer", tags=["campaign-influencer"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])

@app.get("/")
def read_root():
    return {"message": "OthelloAI Marketing Platform API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Vercel serverless handler
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
