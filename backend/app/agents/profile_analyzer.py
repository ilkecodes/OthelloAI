import os
import re
from typing import Dict, Any
from openai import OpenAI

class ProfileAnalyzer:
    """Analyze Instagram profiles to create brand voice."""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def extract_username(self, url: str) -> str:
        """Extract username from Instagram URL."""
        # https://instagram.com/username or instagram.com/username
        match = re.search(r'instagram\.com/([^/?]+)', url)
        return match.group(1) if match else url.replace('@', '')
    
    async def analyze_profile(self, username: str, sample_posts: list) -> Dict[str, Any]:
        """Analyze profile and create brand voice based on actual posts."""
        
        # Sample posts'tan caption'ları al
        captions = [post.get('caption', '')[:200] for post in sample_posts[:10]]
        captions_text = "\n---\n".join(captions)
        
        prompt = f"""Instagram kullanıcı adı: @{username}

Aşağıda bu hesabın son paylaşımlarından örnekler var:

{captions_text}

Bu paylaşımları analiz ederek BRAND VOICE PROFILE oluştur:

1. TONE (Ton): (Örnek: profesyonel, samimi, eğlenceli, lüks, minimalist)
2. LANGUAGE STYLE (Dil Stili): (Örnek: formal, günlük konuşma, teknik, duygusal)
3. EMOJI USAGE (Emoji Kullanımı): (Örnek: sık, nadiren, hiç kullanmıyor)
4. CONTENT THEMES (İçerik Temaları): (Örnek: eğitici, eğlendirici, satış odaklı, hikaye anlatımı)
5. BRAND PERSONALITY (Marka Kişiliği): (3-5 kelime)
6. HASHTAG STRATEGY (Hashtag Stratejisi): (Kaç adet kullanıyor, hangi tür)

ÇIKTI JSON formatında olsun:
{{
  "tone": "",
  "language_style": "",
  "emoji_usage": "",
  "content_themes": [],
  "brand_personality": [],
  "hashtag_strategy": "",
  "sample_caption_style": ""
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Sen bir marka analisti ve sosyal medya uzmanısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            import json
            brand_voice = json.loads(response.choices[0].message.content)
            return brand_voice
            
        except Exception as e:
            print(f"Error analyzing profile: {e}")
            return {
                "tone": "professional",
                "language_style": "formal",
                "emoji_usage": "moderate",
                "content_themes": ["general"],
                "brand_personality": ["authentic"],
                "hashtag_strategy": "3-5 relevant hashtags"
            }
