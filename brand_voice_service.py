import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from sqlalchemy.orm import Session
import json

class BrandVoiceService:
    """Marka sesi analizi ve içerik üretimi"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def analyze_brand_voice(self, corpus_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Marka içeriklerini analiz edip brand voice profili çıkar
        
        Args:
            corpus_items: [{text_content, metadata}, ...]
        
        Returns:
            {
                tone, language_style, emoji_usage,
                content_themes, brand_personality,
                hashtag_strategy, voice_summary, confidence_score
            }
        """
        
        if not corpus_items:
            return self._default_voice_profile()
        
        # İçerikleri hazırla
        sample_texts = [item.get('text_content', '')[:300] for item in corpus_items[:20]]
        combined_text = "\n---\n".join(sample_texts)
        
        prompt = f"""Aşağıdaki marka içeriklerini analiz ederek BRAND VOICE PROFILE oluştur.

İÇERİKLER:
{combined_text}

GÖREV: Bu içeriklerin ortak özelliklerini çıkar ve JSON formatında döndür.

Analiz edilecek özellikler:
1. TONE (Genel Ton): professional/casual/friendly/authoritative/playful
2. LANGUAGE_STYLE: formal/conversational/technical/storytelling
3. EMOJI_USAGE: frequent/moderate/minimal/none
4. CONTENT_THEMES: ["education", "entertainment", "sales", "community", "inspiration"]
5. BRAND_PERSONALITY: ["innovative", "trustworthy", "fun", "expert", "relatable"] (3-5 kelime)
6. HASHTAG_STRATEGY: "3-5 relevant hashtags" / "minimal hashtag use" / etc.
7. VOICE_SUMMARY: Bu markayı anlatan 2-3 cümlelik özet (içerik üretiminde kullanılacak)

ÇIKTI (sadece JSON, başka bir şey yazma):
{{
  "tone": "",
  "language_style": "",
  "emoji_usage": "",
  "content_themes": [],
  "brand_personality": [],
  "hashtag_strategy": "",
  "voice_summary": "",
  "confidence_score": 85
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sen bir marka analisti ve sosyal medya uzmanısın. Sadece JSON formatında cevap ver."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            
            # Markdown code block temizle
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            
            voice_profile = json.loads(content)
            voice_profile['sample_size'] = len(corpus_items)
            
            return voice_profile
            
        except Exception as e:
            print(f"❌ Brand voice analiz hatası: {e}")
            return self._default_voice_profile()
    
    def generate_branded_content(
        self,
        voice_profile: Dict[str, Any],
        prompt: str,
        platform: str = "instagram",
        content_type: str = "post"
    ) -> str:
        """
        Marka sesine uygun içerik üret
        
        Args:
            voice_profile: BrandVoiceProfile'dan gelen profil
            prompt: Kullanıcının isteği (örn: "yeni ürün tanıtımı")
            platform: instagram/twitter/linkedin
            content_type: post/story/reel/tweet
        """
        
        voice_summary = voice_profile.get('voice_summary', '')
        tone = voice_profile.get('tone', 'professional')
        language_style = voice_profile.get('language_style', 'conversational')
        emoji_usage = voice_profile.get('emoji_usage', 'moderate')
        hashtag_strategy = voice_profile.get('hashtag_strategy', '3-5 hashtags')
        
        system_prompt = f"""Sen bir marka içerik üreticisisin. Aşağıdaki marka sesine TAM OLARAK sadık kalarak içerik üreteceksin.

MARKA SESİ PROFİLİ:
{voice_summary}

ÖZELLİKLER:
- Ton: {tone}
- Dil Stili: {language_style}
- Emoji Kullanımı: {emoji_usage}
- Hashtag Stratejisi: {hashtag_strategy}

ÖNEMLİ: Bu markanın stilini BIREBIR taklit et. Aynı ton, aynı üslup, aynı enerji!"""

        platform_instructions = {
            "instagram": "Instagram için caption yaz. Emoji kullanabilirsin. Caption uzun olabilir.",
            "twitter": "280 karakter sınırına uy. Kısa ve çarpıcı ol.",
            "linkedin": "Profesyonel ton kullan. Daha uzun ve detaylı olabilir."
        }
        
        user_prompt = f"""PLATFORM: {platform}
İÇERİK TİPİ: {content_type}
İSTEK: {prompt}

{platform_instructions.get(platform, '')}

Sadece içeriği yaz, başka bir şey ekleme."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.8,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"❌ İçerik üretim hatası: {e}")
            return "İçerik üretilemedi. Lütfen tekrar deneyin."
    
    def _default_voice_profile(self) -> Dict[str, Any]:
        """Varsayılan profil (içerik yoksa)"""
        return {
            "tone": "professional",
            "language_style": "conversational",
            "emoji_usage": "moderate",
            "content_themes": ["general"],
            "brand_personality": ["authentic", "trustworthy"],
            "hashtag_strategy": "3-5 relevant hashtags",
            "voice_summary": "Professional and authentic brand communication with a conversational tone.",
            "confidence_score": 50,
            "sample_size": 0
        }

# Singleton instance
brand_voice_service = BrandVoiceService()
