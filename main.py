from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OthelloAI Marketing Platform", redirect_slashes=False)

# ========== CORS MIDDLEWARE (ÖNEMLİ!) ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://othello-dashboard-frontend.vercel.app",
        "http://localhost:3000",
        "http://localhost:3001",
        "*"  # Geliştirme için tüm originlere izin
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Import routers
from api import clients, content, trends, campaigns, influencers

# Register routers
app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(trends.router, prefix="/api/trends", tags=["trends"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(influencers.router, prefix="/api/influencers", tags=["influencers"])

@app.get("/")
def root():
    return {
        "message": "OthelloAI Marketing Platform API", 
        "version": "2.0",
        "status": "healthy"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

# OPTIONS endpoint for CORS preflight
@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str):
    return {"message": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
