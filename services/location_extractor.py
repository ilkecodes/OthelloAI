"""AI ile Biography'den Konum Çıkarma"""
import os
from openai import OpenAI
import json

# OPENAI_API_KEY veya OPENAI_API_TOKEN - ikisini de dene
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_TOKEN")
openai_client = OpenAI(api_key=api_key) if api_key else None

def extract_location_from_bio(biography: str, username: str = "") -> dict:
    """Biography'den konum çıkar"""
    
    if not biography:
        return {"city": None, "country": "Turkey", "confidence": "low"}
    
    # Türkiye şehirleri
    turkish_cities = [
        "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Adana",
        "Konya", "Gaziantep", "Mersin", "Kayseri", "Eskişehir"
    ]
    
    # 1. Direkt arama
    bio_lower = biography.lower()
    for city in turkish_cities:
        if city.lower() in bio_lower:
            return {
                "city": city,
                "country": "Turkey",
                "confidence": "high",
                "source": "direct_match"
            }
    
    # 2. Emoji ve pattern check
    if "📍" in biography or "📌" in biography:
        # Emoji'den sonraki kelimeyi al
        words = biography.split()
        for i, word in enumerate(words):
            if "📍" in word or "📌" in word:
                if i + 1 < len(words):
                    next_word = words[i + 1].strip(".,!?")
                    for city in turkish_cities:
                        if city.lower() in next_word.lower():
                            return {
                                "city": city,
                                "country": "Turkey",
                                "confidence": "high",
                                "source": "emoji_pattern"
                            }
    
    # 3. AI kullan (eğer varsa)
    if openai_client:
        try:
            prompt = f"""Extract location from this Instagram bio:

Bio: "{biography}"

Turkish cities: İstanbul, Ankara, İzmir, Bursa, Antalya

Return JSON:
{{
  "city": "city name or null",
  "country": "Turkey or other",
  "confidence": "high|medium|low"
}}"""

            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"},
                timeout=10
            )
            
            result = json.loads(response.choices[0].message.content)
            result["source"] = "ai"
            return result
            
        except Exception as e:
            print(f"⚠️ AI error: {e}")
    
    # 4. Default
    return {
        "city": None,
        "country": "Turkey",
        "confidence": "low",
        "source": "default"
    }

def filter_by_location(profiles: list, target_location: str) -> list:
    """Konuma göre filtrele"""
    
    if not target_location:
        return profiles
    
    target_lower = target_location.lower().strip()
    filtered = []
    
    for profile in profiles:
        bio = profile.get("biography", "")
        
        # Basit string match (en hızlı)
        if target_lower in bio.lower():
            filtered.append(profile)
            continue
        
        # Location extraction
        location_data = extract_location_from_bio(bio, profile.get("username", ""))
        profile["location_data"] = location_data
        
        if location_data["city"]:
            if target_lower in location_data["city"].lower():
                filtered.append(profile)
    
    print(f"📍 Location filter: {len(profiles)} -> {len(filtered)} profiles")
    return filtered

# Test
if __name__ == "__main__":
    test_bios = [
        "📍 İstanbul | Food Blogger 🍕",
        "Fitness coach | Ankara 💪",
        "Travel | Antalya 🌍",
        "Fashion blogger",
        "#istanbul #foodie"
    ]
    
    print("🧪 Testing location extraction:\n")
    for bio in test_bios:
        result = extract_location_from_bio(bio)
        print(f"Bio: {bio}")
        print(f"→ {result}\n")
