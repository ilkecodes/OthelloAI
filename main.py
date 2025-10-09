from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OthelloAI Marketing Platform")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers - FORCE RELOAD
import importlib
import sys
if 'api.clients' in sys.modules:
    importlib.reload(sys.modules['api.clients'])
if 'api.content' in sys.modules:
    importlib.reload(sys.modules['api.content'])
if 'api.trends' in sys.modules:
    importlib.reload(sys.modules['api.trends'])
if 'api.influencers' in sys.modules:
    importlib.reload(sys.modules['api.influencers'])
if 'api.campaigns' in sys.modules:
    importlib.reload(sys.modules['api.campaigns'])

from api import clients, content, trends, influencers, campaigns

app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(trends.router, prefix="/api/trends", tags=["trends"])
app.include_router(influencers.router, prefix="/api/influencers", tags=["influencers"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])

@app.get("/")
def root():
    return {"message": "OthelloAI Marketing Platform API", "version": "1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
