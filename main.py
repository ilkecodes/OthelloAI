from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

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
    return {"status": "ok"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Database
from database import Base, engine
Base.metadata.create_all(bind=engine)

# API Routes
from api.clients import router as clients_router
from api.trends import router as trends_router
from api.campaigns import router as campaigns_router
from api.content import router as content_router

app.include_router(clients_router, prefix="/api/clients", tags=["clients"])
app.include_router(trends_router, prefix="/api/trends", tags=["trends"])
app.include_router(campaigns_router, prefix="/api/campaigns", tags=["campaigns"])
app.include_router(content_router, prefix="/api/content", tags=["content"])

print("✅ API routes loaded: clients, trends, campaigns")

@app.post("/admin/reset-trends-sequence")
def reset_trends_sequence():
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            # Mevcut max ID'yi bul
            result = conn.execute(text("SELECT COALESCE(MAX(id), 0) FROM trends;"))
            max_id = result.scalar()
            # Sequence'i reset et
            conn.execute(text(f"ALTER SEQUENCE trends_id_seq RESTART WITH {max_id + 1};"))
            conn.commit()
        return {"message": f"Sequence reset to {max_id + 1}"}
    except Exception as e:
        return {"error": str(e)}
@app.post("/admin/recreate-trends")
def recreate_trends():
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS trends CASCADE;"))
            conn.commit()
        Base.metadata.create_all(bind=engine)
        return {"message": "✅ Trends table recreated with correct schema"}
    except Exception as e:
        return {"error": str(e)}

_ENABLE_BRAND_VOICE = os.getenv("ENABLE_BRAND_VOICE", "false").lower() == "true"

if _ENABLE_BRAND_VOICE:
    try:
        from api.brand_voice import router as brand_voice_router
        app.include_router(brand_voice_router, prefix="/api/brand-voice", tags=["brand-voice"])
        print("✅ Brand Voice System: ENABLED")
    except Exception as e:
        print(f"⚠️  Brand Voice System: Failed to load - {e}")
else:
    print("⚠️  Brand Voice System: DISABLED (set ENABLE_BRAND_VOICE=true)")
