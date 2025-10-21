from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

app = FastAPI(title="OthelloAI Marketing Platform", redirect_slashes=False)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "features": {
            "brand_voice": os.getenv("ENABLE_BRAND_VOICE", "false").lower() == "true"
        }
    }

@app.get("/health")
def health():
    return {"status": "ok"}

# Database
from database import Base, engine
Base.metadata.create_all(bind=engine)

# API Routes
from api.clients import router as clients_router
from api.trends import router as trends_router

app.include_router(clients_router, prefix="/api/clients", tags=["clients"])
app.include_router(trends_router, prefix="/api/trends", tags=["trends"])

# Brand Voice Feature
ENABLE_BRAND_VOICE = os.getenv("ENABLE_BRAND_VOICE", "false").lower() == "true"

if ENABLE_BRAND_VOICE:
    try:
        print("🔍 Loading Brand Voice router...")
        from api.brand_voice import router as brand_voice_router
        app.include_router(brand_voice_router, prefix="/api/brand-voice", tags=["brand-voice"])
        print("✅ Brand Voice feature enabled at /api/brand-voice")
    except Exception as e:
        print(f"❌ Brand Voice load failed: {e}")
        import traceback
        traceback.print_exc()
else:
    print("ℹ️  Brand Voice disabled (set ENABLE_BRAND_VOICE=true)")
