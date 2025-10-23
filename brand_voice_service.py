import os
from typing import List, Dict, Any
from openai import OpenAI
import json

class BrandVoiceService:
    """Marka sesi analizi ve içerik üretimi"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = OpenAI(api_key=api_key)
        else:
            self.openai_client = None
    
    def analyze_brand_voice(self, corpus_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Marka içeriklerini analiz et"""
        
        if not self.openai_client:
            return self._default_voice_profile()
        
        if not corpus_items:
            return self._default_voice_profile()
        
        sample_texts = [item.get('text_content', '')[:300] for item in corpus_items[:20]]
        combined_text = "\n---\n".join(sample_texts)
        
        prompt = f"""Aşağıdaki marka içeriklerini analiz ederek MARKA SESİ PROFİLİ oluştur.

İÇERİKLER:
{combined_text}

GÖREV: Bu içeriklerin ortak özelliklerini çıkar ve SADECE JSON formatında döndür.

Analiz edilecek özellikler:
1. TON: profesyonel/samimi/arkadaşça/otoriter/eğlenceli
2. DİL STİLİ: resmi/konuşma dili/teknik/hikaye anlatımı
3. EMOJİ KULLANIMI: sık/orta/az/hiç
4. İÇERİK TEMALARI: ["eğitici", "eğlendirici", "satış", "topluluk", "ilham"]
5. MARKA KİŞİLİĞİ: ["yenilikçi", "güvenilir", "eğlenceli", "uzman", "samimi"]
6. HASHTAG STRATEJİSİ: "3-5 ilgili hashtag" / "minimal hashtag"
7. SES ÖZETİ: Bu markayı anlatan 2-3 cümlelik Türkçe özet

ÇIKTI (SADECE JSON):
{{
  "tone": "profesyonel",
  "language_style": "samimi",
  "emoji_usage": "orta",
  "content_themes": ["eğitici", "ilham verici"],
  "brand_personality": ["yenilikçi", "güvenilir"],
  "hashtag_strategy": "3-5 ilgili hashtag",
  "voice_summary": "Modern ve samimi bir dille iletişim kuran, müşterilerine değer katan profesyonel bir marka.",
  "confidence_score": 85
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Sen bir marka analisti ve sosyal medya uzmanısın. SADECE Türkçe JSON formatında cevap ver."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            content = response.choices[0].message.content.strip()
            
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            
            voice_profile = json.loads(content)
            voice_profile['sample_size'] = len(corpus_items)
            
            print(f"✅ Marka sesi analizi tamamlandı: {voice_profile.get('tone')}")
            
            return voice_profile
            
        except Exception as e:
            print(f"❌ Marka sesi analiz hatası: {e}")
            return self._default_voice_profile()
    
    def generate_branded_content(
        self,
        voice_profile: Dict[str, Any],
        prompt: str,
        platform: str = "instagram"
    ) -> str:
        """Marka sesine uygun içerik üret"""
        
        if not self.openai_client:
            return "OpenAI API anahtarı yapılandırılmamış."
        
        voice_summary = voice_profile.get('voice_summary', '')
        tone = voice_profile.get('tone', 'profesyonel')
        language_style = voice_profile.get('language_style', 'samimi')
        emoji_usage = voice_profile.get('emoji_usage', 'orta')
        hashtag_strategy = voice_profile.get('hashtag_strategy', '3-5 hashtag')
        
        platform_instructions = {
            "instagram": "Instagram için caption yaz. Görseli destekleyen, dikkat çekici bir metin oluştur.",
            "twitter": "280 karakter sınırına uy. Kısa, öz ve etkileyici ol.",
            "linkedin": "Profesyonel ve bilgilendirici bir ton kullan. İş dünyasına hitap et."
        }
        
        system_prompt = f"""Sen bu markanın içerik yazarısın. Markanın sesine TAM OLARAK sadık kalarak içerik üreteceksin.

MARKA SESİ PROFİLİ:
{voice_summary}

ÖZELLİKLER:
- Ton: {tone}
- Dil Stili: {language_style}
- Emoji Kullanımı: {emoji_usage}
- Hashtag Stratejisi: {hashtag_strategy}

ÖNEMLİ KURALLAR:
1. Bu markanın stilini BIREBIR taklit et
2. Aynı ton, aynı üslup, aynı enerjiyi kullan
3. Markanın karakteristik özellikleri muhakkak yansıt
4. Özgün ve yaratıcı ol, ama marka sesinden sapma
5. MUTLAKA TÜRKÇE yaz"""

        user_prompt = f"""PLATFORM: {platform}
KONU: {prompt}

{platform_instructions.get(platform, '')}

Markanın sesine uygun, etkileyici bir içerik oluştur. SADECE içeriği yaz, başka açıklama ekleme."""

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
            
            generated = response.choices[0].message.content.strip()
            print(f"✅ İçerik üretildi ({len(generated)} karakter)")
            
            return generated
            
        except Exception as e:
            print(f"❌ İçerik üretim hatası: {e}")
            return "İçerik üretilemedi. Lütfen tekrar deneyin."
    
    def _default_voice_profile(self) -> Dict[str, Any]:
        return {
            "tone": "profesyonel",
            "language_style": "samimi",
            "emoji_usage": "orta",
            "content_themes": ["genel"],
            "brand_personality": ["otantik", "güvenilir"],
            "hashtag_strategy": "3-5 ilgili hashtag",
            "voice_summary": "Profesyonel ve samimi bir marka iletişimi.",
            "confidence_score": 50,
            "sample_size": 0
        }

brand_voice_service = BrandVoiceService()
