"""OpenAI Service - Turkish Format with Customer Requirements"""
import os
import json
from typing import Dict, Optional
from openai import OpenAI
import logging
from .platform_specs import get_platform_spec
from .brand_profiles import get_brand_profile

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def _build_brand_context(self, brand_profile: Optional[Dict]) -> str:
        if not brand_profile:
            return ""
        
        colors = brand_profile.get("colors", {})
        style = brand_profile.get("style", {})
        
        return f"""Marka: {brand_profile.get("name")}
Renkler: {", ".join([f"{v}" for v in colors.values()])}
Stil: {style.get("visual_style", "")}
Mockup Tercihleri: {", ".join(style.get("mockup_preferences", []))}"""
    
    async def generate_content(
        self, client_name: str, brand_voice: Dict, platform: str,
        content_type: str, topic: str, tone: Optional[str] = None,
        goal: Optional[str] = "engagement", trend_context: Optional[str] = None
    ) -> Dict:
        
        print(f"📍 OpenAI Service - Generating {content_type}")
        
        brand_profile = get_brand_profile(client_name)
        spec = get_platform_spec(platform, content_type)
        
        if not spec:
            raise ValueError(f"Unsupported: {platform}/{content_type}")
        
        if content_type == "carousel":
            print("🎠 Calling carousel generator...")
            return await self._generate_carousel(client_name, brand_profile, topic, goal)
        elif content_type == "reel":
            print("🎬 Calling reel generator...")
            return await self._generate_reel(client_name, brand_profile, topic, goal)
        elif content_type == "thread":
            print("🧵 Calling thread generator...")
            return await self._generate_thread(client_name, brand_profile, topic, goal)
        else:
            print("📝 Calling post generator...")
            return await self._generate_post(client_name, brand_profile, platform, topic, goal)
    
    async def _generate_carousel(
        self, client_name: str, brand_profile: Optional[Dict], topic: str, goal: str
    ) -> Dict:
        """Generate Instagram Carousel - Turkish Format"""
        
        brand_context = self._build_brand_context(brand_profile)
        
        prompt = f"""Sen Othello Dijital ajansının content creator'ısın ve {client_name} için içerik üretiyorsun.

{brand_context}

GÖREV: "{topic}" konusunda Instagram carousel içeriği oluştur. Hedef: {goal}

ÇOK ÖNEMLİ: Sadece geçerli JSON formatında yanıt ver. Başka hiçbir metin ekleme.

ÖRNEK FORMAT (AYNEN BU YAPIYI KULLAN):

{{
  "slides": [
    {{
      "slide_number": 1,
      "type": "Kapak",
      "title": "Ana Başlık",
      "subtitle": "Alt başlık veya kısa açıklama",
      "visual_description": "Logo mockup + web & sosyal medya ikonları"
    }},
    {{
      "slide_number": 2,
      "type": "Logo Tasarımı",
      "title": "Adım 1: [Başlık]",
      "text": "Detaylı açıklama metni",
      "visual_description": "Logo mockup (kartvizit, tabelada, dijitalde)"
    }},
    {{
      "slide_number": 3,
      "type": "Sosyal Medya",
      "title": "Adım 2: [Başlık]",
      "text": "Detaylı açıklama metni",
      "visual_description": "Instagram profil sayfası mockup + Facebook kapak"
    }},
    {{
      "slide_number": 4,
      "type": "Web Sitesi",
      "title": "Adım 3: [Başlık]",
      "text": "Detaylı açıklama metni",
      "visual_description": "Web site hero bölümünde logo mockup"
    }},
    {{
      "slide_number": 5,
      "type": "Sonuç",
      "title": "Sonuç: [Özet Başlık]",
      "text": "Süreç özeti ve sonuç. Örnek: Logo → Sosyal Medya → Web Sitesi. Güçlü, profesyonel marka imajı.",
      "visual_description": "3 ekran (mobil sosyal medya, web sitesi, kartvizit)"
    }}
  ],
  "post_content": {{
    "title": "Tek Post İçerik Fikri",
    "text": "Othello Dijital olarak, {client_name} için [proje açıklaması]. [Sonuç ve etki].",
    "cta": "Markanız için biz de [hizmet] tasarlayalım. 👉 Markanızı birlikte büyütelim."
  }},
  "visual_brief": {{
    "title": "Görsel Brief",
    "colors": "Othello Dijital paleti + {client_name} kurumsal renkleri",
    "mockups": [
      "Kartvizit & antetli kağıt üzerinde logo",
      "Instagram & Facebook profil mockup",
      "Web site ekranında logo"
    ],
    "style": "Modern, minimal, [sektöre uygun] güven veren",
    "mood": "Profesyonel, güvenilir"
  }},
  "hashtags": "#MarkaKimliği #LogoTasarım #Dijital #OthelloDijital",
  "platform_notes": "Instagram carousel için optimize edilmiş, her slayt bağımsız okunabilir"
}}

Şimdi "{topic}" konusunda yukarıdaki formatta carousel içeriği üret. Sadece JSON döndür, başka metin yok."""

        try:
            print("🔄 Calling OpenAI API...")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Sen Othello Dijital'in uzman content creator'ısın. Sadece geçerli JSON formatında yanıt verirsin."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content.strip()
            print(f"📄 OpenAI returned {len(content)} chars")
            
            data = json.loads(content)
            print(f"✅ JSON parsed successfully")
            
            data["content_type"] = "carousel"
            
            if brand_profile:
                data["brand_colors"] = brand_profile.get("colors", {})
                data["brand_fonts"] = brand_profile.get("fonts", {})
                print(f"✅ Added brand identity")
            
            print(f"✅ Carousel has {len(data.get('slides', []))} slides")
            return data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            print(traceback.format_exc())
            raise
    
    async def _generate_reel(
        self, client_name: str, brand_profile: Optional[Dict], topic: str, goal: str
    ) -> Dict:
        """Generate Instagram Reel - Turkish Format"""
        
        brand_context = self._build_brand_context(brand_profile)
        
        prompt = f"""Sen Othello Dijital ajansının video creator'ısın ve {client_name} için içerik üretiyorsun.

{brand_context}

GÖREV: "{topic}" konusunda 60 saniyelik Instagram Reel scripti oluştur.

Sadece geçerli JSON formatında yanıt ver:

{{
  "scenes": [
    {{
      "scene_number": 1,
      "timing": "0-3 saniye",
      "type": "Hook",
      "text": "Dikkat çekici açılış",
      "visual": "Ne gösterilecek",
      "voiceover": "Sesli anlatım metni"
    }},
    {{
      "scene_number": 2,
      "timing": "3-15 saniye",
      "type": "Giriş",
      "text": "İlk mesaj",
      "visual": "Sahne açıklaması",
      "voiceover": "Sesli anlatım"
    }},
    {{
      "scene_number": 3,
      "timing": "15-30 saniye",
      "type": "Gelişme",
      "text": "Ana nokta",
      "visual": "Sahne açıklaması",
      "voiceover": "Sesli anlatım"
    }},
    {{
      "scene_number": 4,
      "timing": "30-45 saniye",
      "type": "Doruk",
      "text": "Önemli mesaj",
      "visual": "Sahne açıklaması",
      "voiceover": "Sesli anlatım"
    }},
    {{
      "scene_number": 5,
      "timing": "45-60 saniye",
      "type": "Sonuç & CTA",
      "text": "Harekete geçirme",
      "visual": "Kapanış görseli",
      "voiceover": "Son mesaj"
    }}
  ],
  "caption": "Video açıklaması",
  "hashtags": "#Reel #Video #OthelloDijital",
  "music_suggestion": "Müzik önerisi (örn: Upbeat trending sound)",
  "filming_tips": [
    "Çekim ipucu 1",
    "Çekim ipucu 2",
    "Çekim ipucu 3"
  ]
}}

"{topic}" için video scripti üret. Sadece JSON döndür."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Sen Othello Dijital'in video uzmanısın. Sadece JSON yanıt verirsin."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content.strip()
            data = json.loads(content)
            data["content_type"] = "video"
            
            if brand_profile:
                data["brand_colors"] = brand_profile.get("colors", {})
                data["brand_fonts"] = brand_profile.get("fonts", {})
            
            print(f"✅ Reel has {len(data.get('scenes', []))} scenes")
            return data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
    
    async def _generate_thread(
        self, client_name: str, brand_profile: Optional[Dict], topic: str, goal: str
    ) -> Dict:
        """Generate Twitter Thread - Turkish Format"""
        
        prompt = f"""Sen Othello Dijital ajansının Twitter uzmanısın.

GÖREV: {client_name} için "{topic}" konusunda Twitter thread oluştur.

Sadece geçerli JSON:

{{
  "tweets": [
    "Tweet 1: Hook - dikkat çeken açılış (max 280 karakter)",
    "Tweet 2: İlk nokta (max 280 karakter)",
    "Tweet 3: İkinci nokta (max 280 karakter)",
    "Tweet 4: Üçüncü nokta (max 280 karakter)",
    "Tweet 5: Sonuç & CTA (max 280 karakter)"
  ]
}}

"{topic}" için thread üret. Sadece JSON döndür."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Sen Othello Dijital'in Twitter uzmanısın. Sadece JSON yanıt verirsin."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content.strip()
            data = json.loads(content)
            data["content_type"] = "thread"
            
            if brand_profile:
                data["brand_colors"] = brand_profile.get("colors", {})
                data["brand_fonts"] = brand_profile.get("fonts", {})
            
            print(f"✅ Thread has {len(data.get('tweets', []))} tweets")
            return data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise
    
    async def _generate_post(
        self, client_name: str, brand_profile: Optional[Dict], platform: str, topic: str, goal: str
    ) -> Dict:
        """Generate Standard Post - Turkish Format"""
        
        prompt = f"""Sen Othello Dijital ajansının content writer'ısın.

GÖREV: {client_name} için {platform} platformunda "{topic}" konusunda post oluştur.

Sadece geçerli JSON:

{{
  "caption": "Post metni - ilk cümle hook olmalı",
  "hashtags": "#İlgili #Hashtagler #OthelloDijital",
  "cta": "Harekete geçirme mesajı",
  "visual_suggestion": "Görsel önerisi"
}}

"{topic}" için post üret. Sadece JSON döndür."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Sen Othello Dijital'in content writer'ısın. Sadece JSON yanıt verirsin."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content.strip()
            data = json.loads(content)
            
            if brand_profile:
                data["brand_colors"] = brand_profile.get("colors", {})
                data["brand_fonts"] = brand_profile.get("fonts", {})
            
            return data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise

openai_service = OpenAIService()
