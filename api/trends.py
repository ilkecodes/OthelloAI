"""Trends API - Trend Tarama"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from database import get_db, Trend, Client
from services import apify_service

router = APIRouter()

class TrendScanRequest(BaseModel):
    client_id: str
    keywords: List[str]
    limit: Optional[int] = 30

@router.post("/scan")
async def scan_trends(request: TrendScanRequest, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == request.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    print(f"�� Scanning trends for {client.name}")
    
    trends = await apify_service.scan_trending_hashtags(
        keywords=request.keywords,
        limit=request.limit
    )
    
    if not trends:
        return {
            "message": "No trends found",
            "client": client.name,
            "keywords": request.keywords,
            "trends_found": 0,
            "trends": []
        }
    
    saved_trends = []
    for trend in trends:
        score = trend["trending_score"]
        if score >= 0.08:
            rec = f"🔥 SICAK! #{trend['keyword']} viral, HEMEN içerik üret!"
        elif score >= 0.05:
            rec = f"📈 YÜKSELİYOR: #{trend['keyword']} popülerleşiyor!"
        elif score >= 0.03:
            rec = f"📊 STABİL: #{trend['keyword']} güvenilir."
        else:
            rec = f"🌱 GELİŞİYOR: #{trend['keyword']} yeni fırsat."
        
        db_trend = Trend(
            client_id=request.client_id,
            keyword=trend["keyword"],
            platform="instagram",
            post_count=trend["post_count"],
            avg_engagement=trend["avg_engagement"],
            trending_score=trend["trending_score"],
            scanned_at=datetime.now()
        )
        db.add(db_trend)
        db.flush()
        
        saved_trends.append({
            "id": db_trend.id,
            "keyword": trend["keyword"],
            "post_count": trend["post_count"],
            "avg_engagement": trend["avg_engagement"],
            "trending_score": trend["trending_score"],
            "recommendation": rec,
            "scanned_at": db_trend.scanned_at.isoformat()
        })
    
    db.commit()
    
    return {
        "message": f"Found {len(trends)} trends",
        "client": client.name,
        "keywords": request.keywords,
        "trends_found": len(trends),
        "trends": saved_trends
    }

@router.get("/client/{client_id}")
async def get_client_trends(client_id: str, limit: Optional[int] = 50, db: Session = Depends(get_db)):
    trends = db.query(Trend).filter(
        Trend.client_id == client_id
    ).order_by(Trend.scanned_at.desc()).limit(limit).all()
    
    return {
        "client_id": client_id,
        "total_trends": len(trends),
        "trends": [
            {
                "id": t.id,
                "keyword": t.keyword,
                "post_count": t.post_count,
                "avg_engagement": t.avg_engagement,
                "trending_score": t.trending_score,
                "scanned_at": t.scanned_at.isoformat()
            }
            for t in trends
        ]
    }
