"""OpenAI Service - İçerik Üretimi"""
import os
from typing import Dict, Optional
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate_content(
        self, client_name: str, brand_voice: Dict, platform: str,
        topic: str, tone: Optional[str] = None, goal: Optional[str] = "engagement",
        trend_context: Optional[str] = None
    ) -> Dict:
        brand_voice_str = f"""MARKA SESİ:
- Ton: {brand_voice.get('tone', 'professional')}
- Dil: {brand_voice.get('language_style', 'formal')}
- Emoji: {brand_voice.get('emoji_usage', 'medium')}"""
        
        platform_specs = {
            "instagram": "Max 2200 karakter. İlk 125 karakter kritik.",
            "linkedin": "Max 3000 karakter. Profesyonel ton.",
            "tiktok": "Kısa ve çarpıcı. Max 150 karakter.",
        }.get(platform, "Genel sosyal medya.")
        
        trend_section = f"\nTREND: {trend_context}\n" if trend_context else ""
        
        goal_strategy = {
            "awareness": "Bilinirlik artır. Reach odaklı.",
            "engagement": "Etkileşim iste. Soru sor.",
            "sales": "Satış odaklı. Net CTA ver.",
        }.get(goal, "Engagement odaklı.")
        
        prompt = f"""Sen {client_name} markasının content writer'ısın.

{brand_voice_str}

PLATFORM: {platform}
{platform_specs}

KONU: {topic}
HEDEF: {goal_strategy}
{trend_section}

ÇIKTI FORMATI:
Caption: [metin]
Hashtags: [hashtags]
CTA: [call to action]"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"Sen {client_name} markasının content creator'ısın."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            return self._parse_content(content)
        except Exception as e:
            logger.error(f"Error: {e}")
            return {"caption": f"Hata: {str(e)}", "hashtags": "", "cta": ""}
    
    def _parse_content(self, raw: str) -> Dict:
        lines = raw.split('\n')
        caption = hashtags = cta = ""
        for line in lines:
            line = line.strip()
            if line.startswith("Caption:"):
                caption = line.replace("Caption:", "").strip()
            elif line.startswith("Hashtags:"):
                hashtags = line.replace("Hashtags:", "").strip()
            elif line.startswith("CTA:"):
                cta = line.replace("CTA:", "").strip()
            elif caption and not line.startswith(("Hashtags:", "CTA:")):
                caption += " " + line
        return {"caption": caption or raw, "hashtags": hashtags, "cta": cta}

openai_service = OpenAIService()
