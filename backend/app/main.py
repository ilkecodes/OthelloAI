from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables FIRST
load_dotenv()

from .database import engine, Base
from .api.clients import router as clients_router
from .api.trends import router as trends_router
from .api.content import router as content_router
from .api.campaigns import router as campaigns_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Marketing Platform API",
    version="1.0.0",
    redirect_slashes=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers with /api prefix
app.include_router(clients_router, prefix="/api/clients", tags=["clients"])
app.include_router(trends_router, prefix="/api/trends", tags=["trends"])
app.include_router(content_router, prefix="/api/content", tags=["content"])
app.include_router(campaigns_router, prefix="/api/campaigns", tags=["campaigns"])

@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "service": "AI Marketing Platform API",
        "apify_configured": bool(os.getenv("APIFY_API_TOKEN")),
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
