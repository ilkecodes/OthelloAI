"""Content Type Analyzer - Optimized"""
import os
from openai import OpenAI
from typing import Dict, List
import json

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_TOKEN"))

class ContentTypeAnalyzer:
    
    async def analyze_trending_content_types(self, niche: str, keywords: List[str]) -> Dict:
        """Niş için en trend content type'ları AI ile tahmin et"""
        
        print(f"🎬 Analyzing content types for: {niche}")
        
        # Instagram scraping yerine AI'dan direkt tahmin alalım (daha hızlı)
        content_analysis = await self._analyze_with_ai(niche, keywords)
        
        return {
            "niche": niche,
            "content_types": content_analysis,
            "top_performing_type": content_analysis["distribution"][0] if content_analysis["distribution"] else None,
            "recommendations": content_analysis.get("best_practices", [])
        }
    
    async def _analyze_with_ai(self, niche: str, keywords: List[str]) -> Dict:
        """AI ile nişe özel content type analizi"""
        
        try:
            prompt = f"""You are a social media content expert. Analyze the "{niche}" niche with keywords: {keywords}.

Based on current Instagram and TikTok trends in this niche, provide content type distribution and insights.

Return JSON:
{{
  "distribution": [
    {{
      "type": "video",
      "percentage": 50,
      "avg_engagement": 5.5,
      "description": "Kısa video içerikler (Reels, TikTok)",
      "emoji": "🎥"
    }},
    {{
      "type": "carousel",
      "percentage": 30,
      "avg_engagement": 4.2,
      "description": "Çoklu görsel postlar",
      "emoji": "��"
    }},
    {{
      "type": "single_image",
      "percentage": 20,
      "avg_engagement": 3.5,
      "description": "Tek görsel postlar",
      "emoji": "🖼️"
    }}
  ],
  "insights": [
    "Insight 1 in Turkish",
    "Insight 2 in Turkish"
  ],
  "best_practices": [
    "Best practice 1 in Turkish",
    "Best practice 2 in Turkish"
  ]
}}

Make sure percentages add up to 100. Base on real 2024-2025 social media trends."""

            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                timeout=15,  # 15 saniye timeout
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            print(f"  ✅ Content types analyzed with AI")
            return result
            
        except Exception as e:
            print(f"  ⚠️ AI analysis error: {e}")
            return self._get_default_analysis(niche)
    
    def _get_default_analysis(self, niche: str) -> Dict:
        """Fallback default values"""
        
        defaults = {
            "food": {
                "distribution": [
                    {"type": "video", "percentage": 55, "avg_engagement": 6.2, "description": "Tarif ve yemek videoları", "emoji": "🎥"},
                    {"type": "carousel", "percentage": 30, "avg_engagement": 4.5, "description": "Adım adım tarifler", "emoji": "📸"},
                    {"type": "single_image", "percentage": 15, "avg_engagement": 3.2, "description": "Yemek sunumları", "emoji": "🖼️"}
                ],
                "insights": ["Video içerikler 2x daha fazla engagement", "Carousel step-by-step için ideal"],
                "best_practices": ["İlk 3 saniye dikkat çekici olmalı", "5-7 adımlık tarifler optimal"]
            },
            "fitness": {
                "distribution": [
                    {"type": "video", "percentage": 60, "avg_engagement": 6.8, "description": "Egzersiz ve workout videoları", "emoji": "🎥"},
                    {"type": "carousel", "percentage": 25, "avg_engagement": 4.2, "description": "Workout planları", "emoji": "📸"},
                    {"type": "story", "percentage": 15, "avg_engagement": 3.8, "description": "Motivasyon içerik", "emoji": "⚡"}
                ],
                "insights": ["Transformation videoları çok viral", "Kısa egzersiz clip'leri popüler"],
                "best_practices": ["15-30 saniyelik hızlı egzersizler", "Before/after karşılaştırmaları"]
            }
        }
        
        return defaults.get(niche, {
            "distribution": [
                {"type": "video", "percentage": 50, "avg_engagement": 5.0, "description": "Video içerikler", "emoji": "🎥"},
                {"type": "carousel", "percentage": 30, "avg_engagement": 4.0, "description": "Çoklu görsel", "emoji": "📸"},
                {"type": "single_image", "percentage": 20, "avg_engagement": 3.0, "description": "Tek görsel", "emoji": "🖼️"}
            ],
            "insights": ["Video içerikler daha fazla engagement", "Carousel detaylı anlatım için uygun"],
            "best_practices": ["Kısa ve öz içerik", "Görsel kalitesi önemli"]
        })

content_analyzer = ContentTypeAnalyzer()
