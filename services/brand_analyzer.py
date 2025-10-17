"""Brand Analyzer - Müşterinin brand voice'unu öğren"""
import os
from typing import Dict, List, Optional
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class BrandAnalyzer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def analyze_instagram_profile(self, username: str, sample_posts: List[Dict]) -> Dict:
        if not sample_posts:
            return self._default_brand_voice()
        
        captions = [post.get("caption", "")[:300] for post in sample_posts[:10] if post.get("caption")]
        if not captions:
            return self._default_brand_voice()
        
        try:
            prompt = f"""Instagram @{username} için brand voice analizi.

PAYLAŞIMLAR:
{chr(10).join([f"{i+1}. {c}" for i, c in enumerate(captions)])}

JSON çıktı ver:
{{
  "tone": "professional/casual/friendly",
  "emoji_usage": "high/medium/low/none",
  "language_style": "formal/informal",
  "content_themes": ["tema1", "tema2"],
  "hashtag_strategy": "açıklama",
  "brand_personality": ["kelime1", "kelime2"],
  "sample_caption_style": "örnek başlangıç"
}}"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sen bir marka analisti ve sosyal medya uzmanısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content.strip()
            import json
            if result.startswith("```"):
                result = result.split("```")[1]
                if result.startswith("json"):
                    result = result[4:]
            
            brand_voice = json.loads(result)
            logger.info(f"✅ Brand voice analyzed for @{username}")
            return brand_voice
        except Exception as e:
            logger.error(f"Error analyzing brand voice: {e}")
            return self._default_brand_voice()
    
    def _default_brand_voice(self) -> Dict:
        return {
            "tone": "professional",
            "emoji_usage": "medium",
            "language_style": "formal",
            "content_themes": ["general"],
            "hashtag_strategy": "3-5 relevant hashtags",
            "brand_personality": ["authentic", "trustworthy"],
            "sample_caption_style": "Professional and informative."
        }

brand_analyzer = BrandAnalyzer()
