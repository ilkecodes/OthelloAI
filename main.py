from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OthelloAI Marketing Platform")

# ========== CORS - EN BAŞTA ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD"],  # HEAD eklendi
    allow_headers=["*"],
)

@app.get("/")
@app.head("/")  # HEAD method eklendi
def root():
    return {"message": "OthelloAI API", "version": "2.0", "status": "healthy"}

@app.get("/health")
@app.head("/health")  # HEAD method eklendi
def health():
    return {"status": "ok"}

# ========== DATABASE ==========
try:
    from database import engine, Base
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"⚠️ Database error: {e}")

# ========== API ROUTES ==========
try:
    from api import clients, content, trends, campaigns, influencers
    
    app.include_router(clients.router, prefix="/api/clients", tags=["clients"])
    app.include_router(content.router, prefix="/api/content", tags=["content"])
    app.include_router(trends.router, prefix="/api/trends", tags=["trends"])
    app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])
    app.include_router(influencers.router, prefix="/api/influencers", tags=["influencers"])
except Exception as e:
    print(f"⚠️ API error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
