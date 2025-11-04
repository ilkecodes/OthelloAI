"""Complete Trend Dashboard Service - Google + TikTok + Content Types"""
import os
from openai import OpenAI
from pytrends.request import TrendReq
import json
from typing import Dict, List, Optional
from datetime import datetime
import sys
sys.path.append('..')
from services.tiktok_scraper import tiktok_scraper
from services.content_type_analyzer import content_analyzer

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_TOKEN"))

class TrendDashboardService:
    def __init__(self):
        self.pytrends = TrendReq(hl='tr-TR', tz=180)
    
    def get_general_dashboard(self) -> Dict:
        """Dashboard için genel trendler"""
        
        print("📊 Fetching general trends for dashboard...")
        
        google_general = self._get_google_realtime_trends()
        tiktok_general = tiktok_scraper.get_trending_hashtags(country="TR", limit=20)
        
        return {
            "google_trends": google_general,
            "tiktok_trends": tiktok_general,
            "last_updated": str(datetime.now())
        }
    
    def _get_google_realtime_trends(self) -> List[Dict]:
        """Google'ın şu an yükselen trendleri"""
        try:
            general_keywords = [
                "viral", "trend", "popüler", "yeni", "haber",
                "teknoloji", "sağlık", "yemek", "moda", "spor"
            ]
            
            self.pytrends.build_payload(
                general_keywords[:5],
                cat=0,
                timeframe='now 7-d',
                geo='TR'
            )
            
            interest_data = self.pytrends.interest_over_time()
            
            trends = []
            for keyword in general_keywords[:5]:
                if keyword in interest_data.columns:
                    current = int(interest_data[keyword].iloc[-1])
                    
                    trends.append({
                        "keyword": keyword,
                        "interest": current,
                        "category": "genel",
                        "trend_emoji": "🔥" if current > 70 else "📈" if current > 40 else "→"
                    })
            
            trends.sort(key=lambda x: x["interest"], reverse=True)
            return trends
            
        except Exception as e:
            print(f"⚠️ Google realtime trends error: {e}")
            return []
    
    async def search_niche_trends(self, user_query: str) -> Dict:
        """Kullanıcı araması için detaylı niş analiz + CONTENT TYPES"""
        
        print(f"\n{'='*60}")
        print(f"�� Niche Trend Search: {user_query}")
        print(f"{'='*60}\n")
        
        # 1. AI ile niş tespit
        print("1️⃣ Detecting niche with AI...")
        niche_info = await self._detect_niche(user_query)
        detected_niche = niche_info.get('niche', 'lifestyle')
        
        # 2. Google Trends
        print(f"2️⃣ Google Trends for niche: {detected_niche}")
        keywords = niche_info.get('keywords', [user_query])[:5]
        google_niche = self._get_google_niche_trends(keywords)
        
        # 3. TikTok Trends
        print(f"3️⃣ TikTok Trends for niche: {detected_niche}")
        tiktok_niche = tiktok_scraper.get_niche_hashtags(detected_niche, limit=15)
        
        # 4. CONTENT TYPE ANALYSIS (YENİ!)
        print(f"4️⃣ Analyzing trending content types...")
        content_types = await content_analyzer.analyze_trending_content_types(
            detected_niche, 
            keywords
        )
        
        # 5. Rank ve skor
        print("5️⃣ Calculating ranks and scores...")
        ranked_results = self._rank_and_score(google_niche, tiktok_niche, user_query)
        
        # 6. AI İçgörüler
        print("6️⃣ Generating AI insights...")
        ai_insights = await self._generate_insights(
            user_query, 
            niche_info, 
            ranked_results,
            content_types  # Content type verisi de eklendi
        )
        
        print(f"{'='*60}")
        print("✅ Search complete!")
        print(f"{'='*60}\n")
        
        return {
            "query": user_query,
            "niche": niche_info,
            "google_analysis": google_niche,
            "tiktok_analysis": tiktok_niche,
            "content_types": content_types,  # YENİ!
            "ranked_trends": ranked_results,
            "ai_insights": ai_insights,
            "timestamp": str(datetime.now())
        }
    
    def _get_google_niche_trends(self, keywords: List[str]) -> List[Dict]:
        """Google Trends nişe özel analiz"""
        try:
            self.pytrends.build_payload(keywords, cat=0, timeframe='today 3-m', geo='TR')
            interest_data = self.pytrends.interest_over_time()
            related_queries = self.pytrends.related_queries()
            
            trends = []
            
            for keyword in keywords:
                if keyword in interest_data.columns:
                    data = interest_data[keyword]
                    current = int(data.iloc[-1]) if not data.empty else 0
                    previous = int(data.iloc[0]) if len(data) > 0 else 0
                    
                    if previous > 0:
                        growth = ((current - previous) / previous) * 100
                    else:
                        growth = 0
                    
                    if growth > 20:
                        direction = "🔥 Hızlı Yükseliş"
                    elif growth > 0:
                        direction = "📈 Yükselişte"
                    elif growth < -20:
                        direction = "📉 Düşüşte"
                    else:
                        direction = "→ Stabil"
                    
                    related = []
                    if keyword in related_queries:
                        top_q = related_queries[keyword].get('top')
                        if top_q is not None and not top_q.empty:
                            related = [
                                {"query": row['query'], "score": int(row['value'])}
                                for _, row in top_q.head(5).iterrows()
                            ]
                    
                    trends.append({
                        "keyword": keyword,
                        "current_interest": current,
                        "growth_percent": round(growth, 1),
                        "direction": direction,
                        "related_searches": related
                    })
            
            return trends
            
        except Exception as e:
            print(f"⚠️ Google niche trends error: {e}")
            return []
    
    def _rank_and_score(self, google_data: List[Dict], tiktok_data: List[Dict], query: str) -> List[Dict]:
        """Google ve TikTok verilerini birleştir ve skorla"""
        
        combined = []
        
        for g in google_data:
            score = self._calculate_trend_score(
                google_interest=g.get("current_interest", 0),
                google_growth=g.get("growth_percent", 0),
                tiktok_views=0,
                is_google=True
            )
            
            combined.append({
                "keyword": g["keyword"],
                "source": "Google Trends",
                "score": score,
                "google_interest": g.get("current_interest", 0),
                "google_growth": g.get("growth_percent", 0),
                "direction": g.get("direction", "→"),
                "related": g.get("related_searches", [])
            })
        
        for t in tiktok_data[:10]:
            views_str = t.get("views", "0")
            if 'B' in views_str:
                views_num = float(views_str.replace('B', '')) * 1_000_000_000
            elif 'M' in views_str:
                views_num = float(views_str.replace('M', '')) * 1_000_000
            elif 'K' in views_str:
                views_num = float(views_str.replace('K', '')) * 1_000
            else:
                views_num = float(views_str)
            
            score = self._calculate_trend_score(
                google_interest=0,
                google_growth=0,
                tiktok_views=views_num,
                is_google=False
            )
            
            combined.append({
                "keyword": f"#{t['hashtag']}",
                "source": "TikTok",
                "score": score,
                "tiktok_views": t.get("views"),
                "tiktok_posts": t.get("posts", 0),
                "growth": t.get("growth", "→"),
                "rank": t.get("rank", 0)
            })
        
        combined.sort(key=lambda x: x["score"], reverse=True)
        
        for idx, item in enumerate(combined, 1):
            item["overall_rank"] = idx
        
        return combined[:20]
    
    def _calculate_trend_score(self, google_interest: int, google_growth: float, 
                               tiktok_views: float, is_google: bool) -> float:
        """Trend skoru hesapla"""
        if is_google:
            interest_score = (google_interest / 100) * 50
            growth_score = min(max(google_growth, -50), 50) * 0.5
            growth_score = (growth_score + 25)
            return interest_score + (growth_score * 0.5)
        else:
            if tiktok_views > 10_000_000_000:
                return 95
            elif tiktok_views > 1_000_000_000:
                return 85
            elif tiktok_views > 100_000_000:
                return 75
            elif tiktok_views > 10_000_000:
                return 65
            else:
                return 50
    
    async def _detect_niche(self, query: str) -> Dict:
        """AI ile niş tespit"""
        prompt = f"""Analyze: "{query}"

Return JSON:
{{
  "niche": "food|fashion|fitness|travel|beauty|tech|lifestyle|business|entertainment",
  "sub_niche": "specific category",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "related_hashtags": ["hashtag1", "hashtag2"],
  "description": "Brief description in Turkish"
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def _generate_insights(self, query: str, niche_info: Dict, 
                                 ranked_results: List[Dict], content_types: Dict) -> Dict:
        """AI ile içgörüler (content type bilgisi dahil)"""
        
        top_trends = "\n".join([
            f"{r['overall_rank']}. {r['keyword']} - Score: {r['score']:.1f}"
            for r in ranked_results[:5]
        ])
        
        content_summary = "\n".join([
            f"- {ct['type']}: %{ct['percentage']} (Avg Engagement: {ct['avg_engagement']}x)"
            for ct in content_types.get('content_types', {}).get('distribution', [])
        ])
        
        prompt = f"""Trend analyst. Turkish insights:

Query: "{query}"
Niche: {niche_info.get('niche')}

Top Trends:
{top_trends}

Trending Content Types:
{content_summary}

JSON:
{{
  "summary": "2-3 cümle",
  "opportunities": ["Fırsat 1", "Fırsat 2", "Fırsat 3"],
  "content_ideas": [
    {{
      "type": "video|carousel|story",
      "title": "Başlık",
      "description": "Açıklama"
    }}
  ],
  "hashtag_recommendations": ["#tag1", "#tag2", "#tag3"],
  "best_time": "morning|afternoon|evening"
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

dashboard_service = TrendDashboardService()
