"""AI ile Dinamik Konum Eşleştirme + KKTC Özel Desteği"""
import os
from openai import OpenAI
import json
import re

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_TOKEN")
openai_client = OpenAI(api_key=api_key) if api_key else None

# KKTC Knowledge Base
CYPRUS_LOCATIONS = {
    "kktc": ["kktc", "trnc", "kuzey kıbrıs", "kuzey kibris", "northern cyprus", "north cyprus", "kibris", "kıbrıs", "cyprus"],
    "lefkoşa": ["lefkoşa", "lefkosa", "nicosia", "nicosie"],
    "girne": ["girne", "kyrenia", "keryneia"],
    "gazimağusa": ["gazimağusa", "gazimagusa", "mağusa", "magusa", "famagusta"],
    "güzelyurt": ["güzelyurt", "guzelyurt", "morphou"],
    "lefke": ["lefke", "lefka"],
    "iskele": ["iskele", "iskele", "trikomo"],
    "karpaz": ["karpaz", "dipkarpaz", "rizokarpaso"],
    "lapta": ["lapta", "lapithos"],
    "alsancak": ["alsancak", "karavas"],
    "çatalköy": ["çatalköy", "catalkoy"],
    "ozanköy": ["ozanköy", "ozankoy"],
}

def normalize_text(text: str) -> str:
    """Metni normalize et (Türkçe karakterler dahil)"""
    return text.lower().strip()

def check_cyprus_location(text: str) -> dict:
    """KKTC lokasyonu kontrolü - Pattern matching"""
    
    text_norm = normalize_text(text)
    
    for location, aliases in CYPRUS_LOCATIONS.items():
        for alias in aliases:
            # Kelime sınırlarıyla ara (hashtag içinde de olabilir)
            pattern = r'\b' + re.escape(alias) + r'\b|#' + re.escape(alias)
            if re.search(pattern, text_norm):
                return {
                    "found": True,
                    "location": location,
                    "matched_term": alias,
                    "confidence": "high"
                }
    
    return {"found": False}

def extract_location_from_bio(biography: str, username: str = "") -> dict:
    """Biography'den konum çıkar"""
    
    if not biography:
        return {"city": None, "country": None, "confidence": "low"}
    
    # 1. KKTC Pattern Check (en hızlı)
    cyprus_check = check_cyprus_location(biography)
    if cyprus_check["found"]:
        return {
            "city": cyprus_check["location"],
            "country": "KKTC",
            "confidence": cyprus_check["confidence"],
            "source": "cyprus_pattern",
            "matched_term": cyprus_check["matched_term"]
        }
    
    # 2. Location emoji check
    if "📍" in biography or "📌" in biography or "🇨🇾" in biography:
        # Emoji yakınında KKTC kelimesi var mı?
        words_near_emoji = biography.split()
        for word in words_near_emoji:
            cyprus_check = check_cyprus_location(word)
            if cyprus_check["found"]:
                return {
                    "city": cyprus_check["location"],
                    "country": "KKTC",
                    "confidence": "high",
                    "source": "emoji_pattern"
                }
    
    # 3. AI ile genel konum çıkarımı
    if not openai_client:
        return {"city": None, "country": None, "confidence": "low"}
    
    try:
        prompt = f"""Extract location from Instagram bio:

Bio: "{biography}"

KKTC locations: Lefkoşa, Girne, Gazimağusa, Güzelyurt, Lefke, İskele, Karpaz, Lapta
Aliases: KKTC = TRNC = Kuzey Kıbrıs = Northern Cyprus

Return JSON:
{{
  "city": "city/region or null",
  "country": "country or null",
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
        return {"city": None, "country": None, "confidence": "low"}

def check_location_match(biography: str, target_location: str) -> dict:
    """Kullanıcının target location'ı ile biography'yi eşleştir"""
    
    if not target_location or not biography:
        return {"match": False, "confidence": "none"}
    
    target_norm = normalize_text(target_location)
    bio_norm = normalize_text(biography)
    
    # 1. KKTC için özel mantık
    target_cyprus = check_cyprus_location(target_location)
    bio_cyprus = check_cyprus_location(biography)
    
    if target_cyprus["found"] and bio_cyprus["found"]:
        # İkisi de KKTC ile ilgili
        target_loc = target_cyprus["location"]
        bio_loc = bio_cyprus["location"]
        
        # Genel KKTC araması → Tüm KKTC şehirlerini kabul et
        if target_loc == "kktc":
            return {
                "match": True,
                "confidence": "high",
                "reasoning": f"Biography contains {bio_cyprus['matched_term']}, matches KKTC search",
                "source": "cyprus_pattern"
            }
        
        # Spesifik şehir araması
        if target_loc == bio_loc:
            return {
                "match": True,
                "confidence": "high",
                "reasoning": f"Exact match: {target_cyprus['matched_term']} = {bio_cyprus['matched_term']}",
                "source": "cyprus_pattern"
            }
        
        # Farklı şehirler
        return {
            "match": False,
            "confidence": "high",
            "reasoning": f"Different cities: {target_loc} != {bio_loc}",
            "source": "cyprus_pattern"
        }
    
    # 2. Basit string match
    if target_norm in bio_norm:
        return {
            "match": True,
            "confidence": "high",
            "reasoning": "Direct string match",
            "source": "string_match"
        }
    
    # 3. AI ile semantik eşleştirme
    if not openai_client:
        return {"match": False, "confidence": "none"}
    
    try:
        prompt = f"""Does this bio match the target location?

Bio: "{biography}"
Target: "{target_location}"

KKTC context:
- KKTC = TRNC = Kuzey Kıbrıs = Northern Cyprus
- Cities: Lefkoşa (Nicosia), Girne (Kyrenia), Gazimağusa (Famagusta), Güzelyurt (Morphou)
- If searching "KKTC", match ANY KKTC city/region
- If searching specific city, match that city only

Return JSON:
{{
  "match": true/false,
  "confidence": "high|medium|low",
  "reasoning": "explain"
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
        return {"match": False, "confidence": "low"}

def filter_by_location(profiles: list, target_location: str) -> list:
    """Konuma göre filtrele"""
    
    if not target_location:
        return profiles
    
    print(f"\n📍 Filtering by: {target_location}")
    
    filtered = []
    
    for profile in profiles:
        bio = profile.get("biography", "")
        username = profile.get("username", "")
        
        match_result = check_location_match(bio, target_location)
        
        if match_result["match"]:
            location_data = extract_location_from_bio(bio, username)
            profile["location_data"] = location_data
            profile["match_confidence"] = match_result["confidence"]
            filtered.append(profile)
            print(f"  ✅ @{username}: {match_result.get('reasoning', 'Match')}")
    
    print(f"\n📊 {len(profiles)} -> {len(filtered)} profiles")
    return filtered

# Test
if __name__ == "__main__":
    test_cases = [
        {"bio": "📍 Lefkoşa, KKTC | Food", "target": "KKTC"},
        {"bio": "📍 Lefkoşa, KKTC | Food", "target": "Lefkoşa"},
        {"bio": "Girne'den selamlar 🇨🇾", "target": "KKTC"},
        {"bio": "Girne'den selamlar 🇨🇾", "target": "Girne"},
        {"bio": "Girne'den selamlar", "target": "Lefkoşa"},
        {"bio": "#kktc #lefkosa #yemek", "target": "Kuzey Kıbrıs"},
        {"bio": "Northern Cyprus blogger", "target": "TRNC"},
        {"bio": "Gazimağusa fitness trainer", "target": "KKTC"},
        {"bio": "İstanbul food blogger", "target": "KKTC"},
    ]
    
    print("🧪 KKTC Location Matching Tests:\n")
    for i, test in enumerate(test_cases, 1):
        result = check_location_match(test["bio"], test["target"])
        status = "✅" if result["match"] else "❌"
        print(f"{i}. {status}")
        print(f"   Bio: {test['bio']}")
        print(f"   Target: {test['target']}")
        print(f"   Result: {result.get('reasoning', 'No match')}")
        print()
