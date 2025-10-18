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

app.include_router(clients_router, prefix="/api/clients", tags=["clients"])
app.include_router(trends_router, prefix="/api/trends", tags=["trends"])
app.include_router(campaigns_router, prefix="/api/campaigns", tags=["campaigns"])

print("✅ API routes loaded: clients, trends, campaigns")
