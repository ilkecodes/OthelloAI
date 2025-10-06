from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Trend, Client
from services.trend_service import trend_scanner
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class TrendScanRequest(BaseModel):
    client_id: str
    keywords: List[str]
    limit: Optional[int] = 30

class TrendResponse(BaseModel):
    id: int
    client_id: str
    keyword: str
    platform: str
    post_count: int
    avg_engagement: float
    trending_score: float
    scanned_at: str
    
    class Config:
        from_attributes = True

@router.post("/scan")
async def scan_trends(request: TrendScanRequest, db: Session = Depends(get_db)):
    """Belirli bir müşteri için trend taraması yap"""
    
    # Client kontrolü
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    print(f"🔍 Starting trend scan for {client.name}")
    print(f"📌 Keywords: {', '.join(request.keywords)}")
    
    # Trendleri tara
    trends = await trend_scanner.scan_hashtag_trends(request.keywords, request.limit)
    
    # Database'e kaydet
    saved_trends = trend_scanner.save_trends(request.client_id, trends, db)
    
    return {
        "message": f"Scanned {len(trends)} trends for {client.name}",
        "client": client.name,
        "keywords": request.keywords,
        "trends_found": len(trends),
        "trends": [
            {
                "keyword": t.keyword,
                "post_count": t.post_count,
                "avg_engagement": t.avg_engagement,
                "trending_score": t.trending_score
            } for t in saved_trends
        ]
    }

@router.get("/client/{client_id}")
async def get_client_trends(
    client_id: str, 
    limit: Optional[int] = 50,
    db: Session = Depends(get_db)
):
    """Bir müşterinin tüm trendlerini getir"""
    
    trends = db.query(Trend).filter(
        Trend.client_id == client_id
    ).order_by(Trend.scanned_at.desc()).limit(limit).all()
    
    return {
        "client_id": client_id,
        "total_trends": len(trends),
        "trends": trends
    }

@router.get("/top/{client_id}")
async def get_top_trends(
    client_id: str,
    limit: Optional[int] = 10,
    db: Session = Depends(get_db)
):
    """En popüler trendleri getir"""
    
    trends = db.query(Trend).filter(
        Trend.client_id == client_id
    ).order_by(Trend.trending_score.desc()).limit(limit).all()
    
    return {
        "client_id": client_id,
        "top_trends": [
            {
                "keyword": t.keyword,
                "trending_score": round(t.trending_score, 2),
                "avg_engagement": round(t.avg_engagement, 2),
                "post_count": t.post_count,
                "scanned_at": t.scanned_at.isoformat()
            } for t in trends
        ]
    }

@router.delete("/{trend_id}")
async def delete_trend(trend_id: int, db: Session = Depends(get_db)):
    """Bir trendi sil"""
    
    trend = db.query(Trend).filter(Trend.id == trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    
    db.delete(trend)
    db.commit()
    
    return {"message": "Trend deleted successfully"}
