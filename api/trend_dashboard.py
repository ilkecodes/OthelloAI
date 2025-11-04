"""Trend Dashboard API - Google + TikTok"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sys
sys.path.append('..')
from services.trend_dashboard_service import dashboard_service

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """
    📊 ANA DASHBOARD
    
    Genel trendleri gösterir:
    - Google Trends: Popüler aramalar
    - TikTok: Top trending hashtags
    """
    
    try:
        data = dashboard_service.get_general_dashboard()
        
        return {
            "success": True,
            "data": data
        }
        
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

class TrendSearchRequest(BaseModel):
    query: str

@router.post("/search")
async def search_trends(request: TrendSearchRequest):
    """
    🔍 DETAYLI NİŞ ARAMA
    
    Kullanıcı araması için:
    - AI niş tespiti
    - Google Trends analizi (nişe özel)
    - TikTok analizi (nişe özel)
    - Kombine ranking ve skorlama
    - AI içgörüler ve öneriler
    """
    
    if not request.query:
        raise HTTPException(status_code=400, detail="Arama sorgusu gerekli")
    
    try:
        result = await dashboard_service.search_niche_trends(request.query)
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
