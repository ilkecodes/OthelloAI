from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
import os
import json
from ..database import get_db
from ..models.trend import Trend
from ..models.client import Client
from ..hashtags.client_hashtags import CLIENT_HASHTAGS

router = APIRouter()

def get_brand_voice(client: Client) -> str:
    """Get brand voice based on industry."""
    voices = {
        "Healthcare": "Professional, empathetic, trustworthy. Focus on patient care and medical expertise.",
        "Food & Beverage": "Warm, inviting, appetizing. Emphasize quality ingredients and culinary experience.",
        "Handmade Products": "Authentic, artisanal, personal. Highlight craftsmanship and uniqueness.",
        "Desserts": "Delightful, indulgent, joyful. Create desire and celebrate special moments.",
        "Entertainment": "Energetic, fun, engaging. Build excitement and FOMO.",
        "Digital Marketing": "Strategic, innovative, results-driven. Showcase expertise and value.",
        "E-commerce": "Convenient, quality-focused, customer-centric. Highlight benefits and ease.",
        "Interior Design": "Sophisticated, creative, transformative. Inspire and visualize possibilities."
    }
    return voices.get(client.industry, "Professional, engaging, authentic.")

@router.post("/generate")
async def generate_content(
    trend_id: int,
    platform: str = "instagram",
    db: Session = Depends(get_db)
):
    """Generate branded content from a trend using winning patterns."""
    
    # Get trend and client
    trend = db.query(Trend).filter(Trend.id == trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    
    client = db.query(Client).filter(Client.id == trend.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Get client hashtags
    client_key = client.name.lower().replace(" ", "_")
    hashtag_groups = CLIENT_HASHTAGS.get(client_key, {})
    brand_hashtags = hashtag_groups.get("primary", [])[:3]
    
    # Load winning patterns from client
    winning_patterns = {}
    if client.winning_patterns:
        try:
            winning_patterns = json.loads(client.winning_patterns)
        except Exception as e:
            print(f"⚠️ Could not parse winning patterns: {e}")
    
    # Parse brand voice data
    brand_voice_data = {}
    if client.brand_voice:
        try:
            # Single quotes'u double quotes'a çevir
            brand_voice_str = client.brand_voice.replace("'", '"')
            brand_voice_data = json.loads(brand_voice_str)
        except Exception as e:
            print(f"⚠️ Could not parse brand voice: {e}")
            # Fallback to industry-based brand voice
            brand_voice_data = {
                "tone": get_brand_voice(client),
                "language_style": "profesyonel",
                "emoji_usage": "orta düzey",
                "brand_personality": ["otantik"],
                "hashtag_strategy": "3-5 hashtag"
            }
    else:
        # No brand voice data, use industry defaults
        brand_voice_data = {
            "tone": get_brand_voice(client),
            "language_style": "profesyonel",
            "emoji_usage": "orta düzey",
            "brand_personality": ["otantik"],
            "hashtag_strategy": "3-5 hashtag"
        }
    
    # Build enhanced prompt with winning patterns
    winning_formula = ""
    if winning_patterns:
        winning_formula = f"""
KAZANAN FORMÜL (Bu niche'de yüksek engagement alan içerikler):
- Hook Tipi: {winning_patterns.get('best_hook_type', 'Bilinmiyor')}
- İçerik Yapısı: {winning_patterns.get('best_structure', 'Bilinmiyor')}
- CTA Stratejisi: {winning_patterns.get('cta_strategy', 'Bilinmiyor')}
- Optimal Hashtag Sayısı: {winning_patterns.get('hashtag_count', '3-5')}
- İdeal Uzunluk: {winning_patterns.get('optimal_length', 'Orta')}
- Emoji Kullanımı: {winning_patterns.get('emoji_pattern', 'Orta düzey')}

⚠️ ÖNEMLİ: Bu formüle sadık kal! Bu niche'de en iyi performans gösteren yapı bu.
"""
    
    prompt = f"""Sen {client.name} için içerik üretiyorsun.

MARKA KİMLİĞİ (Instagram profilinden analiz edildi):
- Ton: {brand_voice_data.get('tone', 'profesyonel')}
- Dil Stili: {brand_voice_data.get('language_style', 'samimi')}
- Emoji Kullanımı: {brand_voice_data.get('emoji_usage', 'orta düzey')}
- Marka Kişiliği: {', '.join(brand_voice_data.get('brand_personality', ['otantik']))}
- Hashtag Stratejisi: {brand_voice_data.get('hashtag_strategy', '3-5 hashtag')}

MARKA BİLGİLERİ:
- İsim: {client.name}
- Sektör: {client.industry}
- Anahtar Kelimeler: {client.keywords}
{winning_formula}
TREND BİLGİSİ:
Hashtag: #{trend.hashtag}
İçerik: {trend.content[:200]}
Engagement: {trend.volume}

GÖREV:
1. Bu markanın TAM OLARAK AYNI ÜSLUBUNDAyazmalısın
2. Yukarıdaki marka kimliğine %100 sadık kal
3. {'KAZANAN FORMÜL stratejisini kullan - bu niche için kanıtlanmış strateji!' if winning_patterns else 'Trend\'den ilham al'}
4. Eğer marka emoji kullanmıyorsa sen de kullanma
5. Eğer marka samimi konuşuyorsa sen de samimi yaz
6. Eğer marka profesyonel ise sen de profesyonel ol
7. Trend'den ilham al ama KOPYALAMA, özgün içerik üret
8. Türkçe olsun, doğal ve akıcı
9. Call-to-action ekle (DM, link, profil ziyareti vb.)

PLATFORM: {platform}
{f"Karakter limiti: 280" if platform == "twitter" else ""}
{f"Caption uzun olabilir, hikaye anlat" if platform == "instagram" else ""}
{f"Profesyonel ton kullan" if platform == "linkedin" else ""}

ÇIKTI FORMATI:
Caption: [içerik metni]
Hashtags: [hashtag'ler - {brand_voice_data.get('hashtag_strategy', '3-5 hashtag')}]
CTA: [call to action]
"""

    try:
        from openai import OpenAI
        client_openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client_openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Sen {client.name} markasının social media content creator'ısın. Bu markanın tonunu ve üslubunu mükemmel bir şekilde taklit ediyorsun."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        generated_content = response.choices[0].message.content
        
        # Parse the response
        lines = generated_content.split('\n')
        caption = ""
        hashtags = ""
        cta = ""
        
        for line in lines:
            if line.startswith("Caption:"):
                caption = line.replace("Caption:", "").strip()
            elif line.startswith("Hashtags:"):
                hashtags = line.replace("Hashtags:", "").strip()
            elif line.startswith("CTA:"):
                cta = line.replace("CTA:", "").strip()
        
        # Add brand hashtags if available
        if brand_hashtags and not any(tag in hashtags for tag in brand_hashtags):
            brand_tags = " ".join([f"#{tag}" for tag in brand_hashtags])
            hashtags = f"{hashtags} {brand_tags}".strip()
        
        return {
            "success": True,
            "content": {
                "caption": caption or generated_content,
                "hashtags": hashtags,
                "cta": cta,
                "platform": platform,
                "client_name": client.name,
                "inspired_by": f"#{trend.hashtag}",
                "brand_voice_used": brand_voice_data.get('tone', 'default'),
                "used_winning_patterns": bool(winning_patterns),
                "winning_formula": winning_patterns if winning_patterns else None
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")