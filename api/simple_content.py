"""Simple Content Generator - Görsel Brief Dahil"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI
import sys
sys.path.append('..')
from services.brand_profiles import get_brand_profile

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SimpleContentRequest(BaseModel):
    client_name: str
    platform: str
    content_type: str
    topic: str
    goal: str

def build_visual_brief(brand_profile):
    """Brand profile'dan görsel brief oluştur"""
    if not brand_profile:
        return ""
    
    colors = brand_profile.get("colors", {})
    fonts = brand_profile.get("fonts", {})
    style = brand_profile.get("style", {})
    
    color_palette = ", ".join([f"{name}: {code}" for name, code in colors.items()])
    font_list = ", ".join([f"{role}: {font}" for role, font in fonts.items()])
    
    return f"""
═══════════════════════════════════════
🎨 MARKA KİMLİĞİ & GÖRSEL BRIEF
═══════════════════════════════════════

📐 RENK PALETİ
{color_palette}

✍️ FONT KULLANIMI
{font_list}

🎭 GÖRSEL STİL
{style.get('visual_style', 'Belirtilmemiş')}

💭 MOOD & ATMOSFER
{style.get('mood', 'Belirtilmemiş')}

📸 MOCKUP TERCİHLERİ
{', '.join(style.get('mockup_preferences', []))}

🎯 TASARIM BRIEF
{style.get('design_brief', 'Belirtilmemiş')}

═══════════════════════════════════════
"""

@router.post("/simple-generate")
async def simple_generate(request: SimpleContentRequest):
    print(f"🎯 Request: {request.client_name} - {request.content_type}")
    
    # Brand profile al
    brand_profile = get_brand_profile(request.client_name)
    visual_brief = build_visual_brief(brand_profile)
    
    # REEL için detaylı format
    if request.content_type == "reel":
        prompt = f"""Sen Othello Dijital ajansının Reels uzmanısın.

MÜŞTERİ: {request.client_name}
KONU: {request.topic}
HEDEF: {request.goal}

{visual_brief}

GÖREV: Yukarıdaki MARKA KİMLİĞİ'ni dikkate alarak "REELS ÜRETİM ŞABLONU"nu TAMAMEN doldur.

ÖNEMLİ: Görsel tasarım önerilerinde:
- Yukarıdaki renk paletini kullan
- Belirtilen fontları öner
- Mockup tercihlerini göz önünde bulundur
- Design brief'teki tonu koru

═══════════════════════════════════════

🧭 1. STRATEJİK BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Amaç: [Bilinçlendirme / Güven / Satış / Duygusal bağ]
Ana Mesaj: [Reel sonunda izleyicinin aklında kalacak TEK cümle]
Hedef Kitle: [Demografi + psikografik]
Duygu Tonu: [İlham verici / samimi / profesyonel]
Platform: {request.platform}

🧩 2. YAPISAL ZAMANLAMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[0-3sn] HOOK: [Şaşırtıcı açılış]
Görsel: [İlk karede ne - MARKA RENKLERİNİ KULLAN]
Müzik: [Enerji, tempo]

[3-10sn] EMPATİ: [Problem yansıtma]
Görsel: [Sahne - BRAND STİLİNE UYGUN]
Ses: [Ton]

[10-35sn] BİLGİ: [Adım adım]
Görsel: [MOCKUP TERCİHLERİNİ KULLAN]
Ses: [Tempo]

[35-50sn] VİZYON: [Çözüm]
Görsel: [MARKA MOOD'UNA UYGUN]
Ses: [Umut dolu]

[50-60sn] CTA: [Harekete geçirme]
Görsel: [Logo, profil]
Ses: [Final]

🎨 3. GÖRSEL TASARIM REHBERİ (TASARIMCIYA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Renk Kullanımı:
[Hangi sahnede hangi marka rengi kullanılacak - detaylı]

Font Kullanımı:
[Altyazılarda, başlıklarda hangi fontlar - detaylı]

Çekim Stili:
[Işık, açı, kompozisyon - brand'e özel]

Geçiş Efektleri:
[Brand mood'una uygun geçişler]

Mockup & Görsel Öğeler:
[Hangi sahnede hangi mockup/görsel]

🗣️ 4. KOMPLE SCRIPT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Zaman damgalı script]

📋 5. TASARIMCI CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Marka renkleri doğru kullanıldı mı?
✅ Fontlar marka kimliğine uygun mu?
✅ Mockup'lar uygun mu?
✅ Mood/atmosfer korunuyor mu?
✅ Logo yerleşimi doğru mu?

═══════════════════════════════════════

Şimdi "{request.topic}" için TAMAMEN doldur ve özellikle GÖRSEL TASARIM bölümünü detaylandır!"""

    # CAROUSEL için
    elif request.content_type == "carousel":
        prompt = f"""Sen Othello Dijital ajansının content strategist'isin.

MÜŞTERİ: {request.client_name}
KONU: {request.topic}
HEDEF: {request.goal}

{visual_brief}

GÖREV: Yukarıdaki MARKA KİMLİĞİ'ni kullanarak Carousel üret.

✍️ İÇERİK TASLAĞI

Slayt 1 – Kapak
Başlık: [Başlık]
Alt: [Alt başlık]
Görsel: [Marka renklerini kullan - detaylı açıklama]
Tasarım Notu: [Font, renk, layout önerisi]
⸻
Slayt 2–5: [Her slayt için ayrı görsel tasarım notu ekle]

🎨 GÖRSEL TASARIM PAKETİ (TASARIMCIYA)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Her Slayt İçin:
- Renk kullanımı: [Hangi marka rengi nerede]
- Font hierarşisi: [Başlık/metin için fontlar]
- Layout: [Kompozisyon önerisi]
- Görsel öğeler: [Mockup/fotoğraf tipleri]

"{request.topic}" için üret!"""

    # POST için
    else:
        prompt = f"""Sen Othello Dijital ajansının content writer'ısın.

MÜŞTERİ: {request.client_name}
KONU: {request.topic}

{visual_brief}

Post + Görsel Brief üret."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Sen Othello Dijital'in strategist'isin. Marka kimliğini her detayda korursun. Tasarımcılar için net brief'ler verirsin."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        return {
            "success": True,
            "content": response.choices[0].message.content
        }
    
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
