from apify_client import ApifyClient
from datetime import datetime
from sqlalchemy.orm import Session
from database import Trend
from config import settings
import json

class TrendScanner:
    def __init__(self):
        self.client = ApifyClient(settings.APIFY_API_TOKEN)
    
    async def scan_hashtag_trends(self, keywords: list[str], limit: int = 30):
        """Instagram hashtag trendlerini tara"""
        trends = []
        
        for keyword in keywords:
            try:
                print(f"🔍 Scanning trends for: #{keyword}")
                
                # Apify Instagram Hashtag Scraper
                run = self.client.actor("apify/instagram-hashtag-scraper").call(
                    run_input={
                        "hashtags": [keyword],
                        "resultsLimit": limit
                    }
                )
                
                # Sonuçları işle
                items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
                
                if items:
                    avg_likes = sum(item.get("likesCount", 0) for item in items) / len(items)
                    avg_comments = sum(item.get("commentsCount", 0) for item in items) / len(items)
                    
                    trend_data = {
                        "keyword": keyword,
                        "platform": "instagram",
                        "post_count": len(items),
                        "avg_engagement": avg_likes + avg_comments,
                        "avg_likes": avg_likes,
                        "avg_comments": avg_comments,
                        "trending_score": (avg_likes + avg_comments * 3) / 100,  # Custom score
                        "sample_posts": [item.get("url") for item in items[:5]],
                        "scanned_at": datetime.now()
                    }
                    
                    trends.append(trend_data)
                    print(f"✅ Found {len(items)} posts for #{keyword}")
                    print(f"   Avg Engagement: {trend_data['avg_engagement']:.0f}")
                
            except Exception as e:
                print(f"❌ Error scanning #{keyword}: {str(e)}")
        
        return trends
    
    def save_trends(self, client_id: int, trends: list, db: Session):
        """Trendleri database'e kaydet"""
        saved = []
        
        for trend in trends:
            db_trend = Trend(
                client_id=client_id,
                keyword=trend["keyword"],
                platform=trend["platform"],
                post_count=trend["post_count"],
                avg_engagement=trend["avg_engagement"],
                trending_score=trend["trending_score"],
                extra_data=json.dumps({
                    "avg_likes": trend["avg_likes"],
                    "avg_comments": trend["avg_comments"],
                    "sample_posts": trend["sample_posts"]
                }),
                scanned_at=trend["scanned_at"]
            )
            db.add(db_trend)
            saved.append(db_trend)
        
        db.commit()
        return saved

trend_scanner = TrendScanner()
