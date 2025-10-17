from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return {"status": "ok", "cors": "enabled"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Sonra database ve API'ler yüklenecek
try:
    from database import Base, engine
    Base.metadata.create_all(bind=engine)
    
    from api import clients, content, trends, campaigns, influencers
    app.include_router(clients.router, prefix="/api/clients")
    app.include_router(content.router, prefix="/api/content")
    app.include_router(trends.router, prefix="/api/trends")
    app.include_router(campaigns.router, prefix="/api/campaigns")
    app.include_router(influencers.router, prefix="/api/influencers")
    print("✅ All loaded")
except Exception as e:
    print(f"⚠️ Error: {e}")
