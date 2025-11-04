"""Real-time Trend Analysis Service"""
import os
from openai import OpenAI
from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_TOKEN"))

class RealtimeTrendAnalyzer:
    def __init__(self):
        self.pytrends = TrendReq(hl='tr-TR', tz=180)  # Türkiye
    
    async def analyze_keywords(self, user_input: str) -> Dict:
        """
        Kullanıcı girdisini analiz et ve nişi bul
        """
        prompt = f"""Analyze this marketing keyword/phrase and extract insights:

Input: "{user_input}"

Return JSON:
{{
  "niche": "food|fashion|fitness|travel|beauty|tech|lifestyle|business",
  "sub_niche": "specific category",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "related_hashtags": ["#hashtag1", "#hashtag2"],
  "target_audience": "audience description",
  "content_ideas": ["idea1", "idea2", "idea3"]
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def get_google_trends(self, keywords: List[str], timeframe: str = 'today 3-m') -> Dict:
        """
        Google Trends'den gerçek zamanlı veri
        """
        try:
            print(f"🔍 Google Trends: {keywords}")
            
            self.pytrends.build_payload(
                keywords,
                cat=0,
                timeframe=timeframe,
                geo='TR'  # Türkiye
            )
            
            # Zaman içinde ilgi
            interest_over_time = self.pytrends.interest_over_time()
            
            # İlgili sorgular
            related_queries = self.pytrends.related_queries()
            
            # İlgili konular
            related_topics = self.pytrends.related_topics()
            
            results = {
                "keywords": keywords,
                "trends": [],
                "related_queries": {},
                "related_topics": {}
            }
            
            # Her keyword için trend skoru
            for keyword in keywords:
                if keyword in interest_over_time.columns:
                    data = interest_over_time[keyword]
                    current_value = int(data.iloc[-1]) if not data.empty else 0
                    previous_value = int(data.iloc[0]) if len(data) > 0 else 0
                    
                    # Trend yönü
                    if current_value > previous_value * 1.2:
                        trend_direction = "🔥 Yükselişte"
                        growth = ((current_value - previous_value) / previous_value * 100) if previous_value > 0 else 0
                    elif current_value < previous_value * 0.8:
                        trend_direction = "📉 Düşüşte"
                        growth = ((current_value - previous_value) / previous_value * 100) if previous_value > 0 else 0
                    else:
                        trend_direction = "→ Stabil"
                        growth = 0
                    
                    results["trends"].append({
                        "keyword": keyword,
                        "current_interest": current_value,
                        "trend_direction": trend_direction,
                        "growth_percent": round(growth, 1),
                        "popularity_score": current_value
                    })
                
                # İlgili sorgular
                if keyword in related_queries:
                    top_queries = related_queries[keyword].get('top')
                    if top_queries is not None and not top_queries.empty:
                        results["related_queries"][keyword] = [
                            {
                                "query": row['query'],
                                "value": int(row['value'])
                            }
                            for _, row in top_queries.head(5).iterrows()
                        ]
            
            return results
            
        except Exception as e:
            print(f"⚠️ Google Trends error: {e}")
            return {"keywords": keywords, "trends": [], "error": str(e)}
    
    def get_tiktok_trends(self) -> List[Dict]:
        """
        TikTok Creative Center'dan trending hashtags
        """
        try:
            # TikTok Creative Center - Public API (örnek)
            url = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/tr"
            
            # Not: Gerçek implementasyon için TikTok API key gerekir
            # Şimdilik mock data
            
            mock_trends = [
                {"hashtag": "keşfet", "views": "125M", "growth": "🔥", "category": "genel"},
                {"hashtag": "fyp", "views": "89M", "growth": "🔥", "category": "genel"},
                {"hashtag": "tiktoktr", "views": "45M", "growth": "📈", "category": "genel"},
                {"hashtag": "viral", "views": "78M", "growth": "🔥", "category": "genel"},
            ]
            
            return mock_trends
            
        except Exception as e:
            print(f"⚠️ TikTok trends error: {e}")
            return []
    
    def get_instagram_hashtag_volume(self, hashtags: List[str]) -> List[Dict]:
        """
        Instagram hashtag popülerliğini tahmin et
        """
        results = []
        
        for hashtag in hashtags:
            # Instagram'da hashtag volume tahmini
            # Gerçek implementasyon için Instagram Graph API gerekir
            
            # Mock data ile simüle et
            volume = hash(hashtag) % 1000000  # Basit hash-based simülasyon
            
            if volume > 500000:
                popularity = "🔥 Çok Popüler"
                recommendation = "Rekabet yüksek, daha niche hashtag'ler de ekle"
            elif volume > 100000:
                popularity = "📈 Popüler"
                recommendation = "İyi bir hashtag, kullan"
            elif volume > 10000:
                popularity = "→ Orta"
                recommendation = "Niche için iyi, engagement potansiyeli var"
            else:
                popularity = "💡 Niche"
                recommendation = "Az rekabet, hedefli kitle için mükemmel"
            
            results.append({
                "hashtag": hashtag,
                "estimated_posts": volume,
                "popularity": popularity,
                "recommendation": recommendation
            })
        
        return results
    
    async def generate_ai_insights(self, 
                                   user_input: str,
                                   google_trends: Dict,
                                   niche_info: Dict) -> Dict:
        """
        Tüm verileri AI ile analiz et ve öneriler oluştur
        """
        
        prompt = f"""You are a marketing trend analyst. Analyze this data and provide insights:

User Input: "{user_input}"
Niche: {niche_info.get('niche')}
Sub-niche: {niche_info.get('sub_niche')}

Google Trends Data:
{json.dumps(google_trends.get('trends', []), indent=2)}

Related Queries:
{json.dumps(google_trends.get('related_queries', {}), indent=2)}

Provide Turkish insights in JSON:
{{
  "trend_analysis": "Ana trend analizi (2-3 cümle)",
  "opportunities": [
    "Fırsat 1",
    "Fırsat 2",
    "Fırsat 3"
  ],
  "content_recommendations": [
    {{
      "content_type": "video|carousel|reels|story",
      "topic": "Konu",
      "hook": "Dikkat çekici başlık",
      "why": "Neden işe yarar"
    }}
  ],
  "hashtag_strategy": [
    "Hashtag stratejisi 1",
    "Hashtag stratejisi 2"
  ],
  "best_posting_times": ["morning|afternoon|evening"],
  "competitor_insights": "Rakip analizi"
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)

# Global instance
trend_analyzer = RealtimeTrendAnalyzer()
