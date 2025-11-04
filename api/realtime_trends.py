"""Real-time Trend Analysis API"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
sys.path.append('..')
from services.realtime_trends import trend_analyzer

router = APIRouter()

class TrendAnalysisRequest(BaseModel):
    keywords: str  # Kullanıcının girdiği anahtar kelimeler
    timeframe: Optional[str] = "today 3-m"  # Google Trends zaman aralığı

@router.post("/analyze")
async def analyze_trends(request: TrendAnalysisRequest):
    """
    🔥 GERÇEK ZAMANLI TREND ANALİZİ
    
    1. Kullanıcı girdisini AI ile analiz et
    2. Google Trends'den gerçek veri çek
    3. TikTok & Instagram trend'lerini kontrol et
    4. AI ile içgörüler ve öneriler oluştur
    """
    
    if not request.keywords:
        raise HTTPException(status_code=400, detail="Anahtar kelime gerekli")
    
    try:
        print(f"\n{'='*60}")
        print(f"🎯 TREND ANALİZİ: {request.keywords}")
        print(f"{'='*60}\n")
        
        # 1. AI Niche Detection
        print("1️⃣ AI ile niş tespiti...")
        niche_info = await trend_analyzer.analyze_keywords(request.keywords)
        print(f"   Niş: {niche_info.get('niche')}")
        print(f"   Alt Niş: {niche_info.get('sub_niche')}")
        
        # 2. Google Trends
        print("\n2️⃣ Google Trends analizi...")
        keywords_to_check = niche_info.get('keywords', [request.keywords])[:5]
        google_trends = trend_analyzer.get_google_trends(
            keywords_to_check,
            timeframe=request.timeframe
        )
        
        # 3. TikTok Trends
        print("\n3️⃣ TikTok trend'leri...")
        tiktok_trends = trend_analyzer.get_tiktok_trends()
        
        # 4. Instagram Hashtag Analysis
        print("\n4️⃣ Instagram hashtag analizi...")
        hashtags = niche_info.get('related_hashtags', [])
        instagram_analysis = trend_analyzer.get_instagram_hashtag_volume(hashtags)
        
        # 5. AI Insights
        print("\n5️⃣ AI içgörü oluşturma...")
        ai_insights = await trend_analyzer.generate_ai_insights(
            request.keywords,
            google_trends,
            niche_info
        )
        
        print(f"\n{'='*60}")
        print("✅ ANALİZ TAMAMLANDI")
        print(f"{'='*60}\n")
        
        return {
            "success": True,
            "user_input": request.keywords,
            "niche_detection": niche_info,
            "google_trends": google_trends,
            "tiktok_trends": tiktok_trends,
            "instagram_analysis": instagram_analysis,
            "ai_insights": ai_insights,
            "timestamp": str(datetime.now())
        }
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trending-now")
async def get_trending_now():
    """Şu anda trend olanlar (genel)"""
    
    try:
        # Genel trend'ler
        google_trends = trend_analyzer.get_google_trends(
            ["viral", "trend", "popüler"],
            timeframe="now 7-d"
        )
        
        tiktok_trends = trend_analyzer.get_tiktok_trends()
        
        return {
            "success": True,
            "google_trends": google_trends,
            "tiktok_trends": tiktok_trends,
            "updated_at": str(datetime.now())
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
