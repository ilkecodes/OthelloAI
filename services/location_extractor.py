"""AI ile Dinamik Konum Eşleştirme + KKTC Kapsamlı Destek"""
import os
from openai import OpenAI
import json
import re

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_TOKEN")
openai_client = OpenAI(api_key=api_key) if api_key else None

# KKTC Kapsamlı Knowledge Base
CYPRUS_LOCATIONS = {
    "kktc": [
        # Resmi isimler
        "kktc", "trnc", "kuzey kıbrıs", "kuzey kibris", "northern cyprus", "north cyprus",
        # Genel Kıbrıs
        "kibris", "kıbrıs", "cyprus", "cypre",
        # Kıbrıslı deyimleri
        "cypriot", "kıbrıslı", "kibrisli", "cypriot",
        # Hashtag varyasyonları
        "northcyprus", "kuzeykibris", "kuzeykıbrıs"
    ],
    "lefkoşa": ["lefkoşa", "lefkosa", "nicosia", "nicosie", "lefkosya"],
    "girne": ["girne", "kyrenia", "keryneia"],
    "gazimağusa": ["gazimağusa", "gazimagusa", "mağusa", "magusa", "famagusta", "ammochostos"],
    "güzelyurt": ["güzelyurt", "guzelyurt", "morphou"],
    "lefke": ["lefke", "lefka"],
    "iskele": ["iskele", "trikomo"],
    "karpaz": ["karpaz", "dipkarpaz", "rizokarpaso", "karpasia"],
    "lapta": ["lapta", "lapithos", "lapethos"],
    "alsancak": ["alsancak", "karavas"],
    "çatalköy": ["çatalköy", "catalkoy"],
    "ozanköy": ["ozanköy", "ozankoy"],
}

def normalize_text(text: str) -> str:
    """Metni normalize et"""
    return text.lower().strip()

def check_cyprus_location(text: str) -> dict:
    """KKTC lokasyonu kontrolü - Esnek pattern matching"""
    
    text_norm = normalize_text(text)
    
    for location, aliases in CYPRUS_LOCATIONS.items():
        for alias in aliases:
            # Kelime sınırlarıyla ara (hashtag içinde de)
            patterns = [
                r'\b' + re.escape(alias) + r'\b',  # Kelime sınırı
                r'#' + re.escape(alias),           # Hashtag
                r'@' + re.escape(alias),           # Mention'da
                alias                              # Substring (son çare)
            ]
            
            for pattern in patterns:
                if re.search(pattern, text_norm, re.IGNORECASE):
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
    
    # Username'de de kontrol et (urban_cypriot gibi)
    full_text = f"{biography} {username}"
    
    # 1. KKTC Pattern Check
    cyprus_check = check_cyprus_location(full_text)
    if cyprus_check["found"]:
        return {
            "city": cyprus_check["location"],
            "country": "KKTC",
            "confidence": cyprus_check["confidence"],
            "source": "cyprus_pattern",
            "matched_term": cyprus_check["matched_term"]
        }
    
    # 2. Emoji check
    if any(emoji in biography for emoji in ["📍", "📌", "🇨��", "🌍"]):
        words = biography.split()
        for word in words:
            cyprus_check = check_cyprus_location(word)
            if cyprus_check["found"]:
                return {
                    "city": cyprus_check["location"],
                    "country": "KKTC",
                    "confidence": "high",
                    "source": "emoji_pattern"
                }
    
    # 3. AI ile genel konum
    if not openai_client:
        return {"city": None, "country": None, "confidence": "low"}
    
    try:
        prompt = f"""Extract location from Instagram:

Bio: "{biography}"
Username: "{username}"

KKTC keywords: cypriot, kıbrıslı, cyprus, kıbrıs, KKTC, TRNC, Northern Cyprus
Cities: Lefkoşa, Girne, Gazimağusa, Güzelyurt

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

def check_location_match(biography: str, target_location: str, username: str = "") -> dict:
    """Target location ile eşleştir"""
    
    if not target_location or not biography:
        return {"match": False, "confidence": "none"}
    
    target_norm = normalize_text(target_location)
    
    # Username + bio birlikte kontrol et
    full_text = f"{biography} {username}"
    
    # 1. KKTC için özel mantık
    target_cyprus = check_cyprus_location(target_location)
    bio_cyprus = check_cyprus_location(full_text)
    
    if target_cyprus["found"] and bio_cyprus["found"]:
        target_loc = target_cyprus["location"]
        bio_loc = bio_cyprus["location"]
        
        # Genel KKTC/Cyprus araması → Tüm KKTC/Cypriot içeriği
        if target_loc == "kktc":
            return {
                "match": True,
                "confidence": "high",
                "reasoning": f"Cyprus content detected: {bio_cyprus['matched_term']}",
                "source": "cyprus_pattern"
            }
        
        # Spesifik şehir
        if target_loc == bio_loc:
            return {
                "match": True,
                "confidence": "high",
                "reasoning": f"City match: {target_cyprus['matched_term']} = {bio_cyprus['matched_term']}",
                "source": "cyprus_pattern"
            }
        
        # Farklı şehirler (ama ikisi de KKTC)
        if target_loc == "kktc" or bio_loc == "kktc":
            # Genel KKTC araması herşeyi yakalar
            return {
                "match": True,
                "confidence": "medium",
                "reasoning": f"General Cyprus search matches {bio_loc}",
                "source": "cyprus_pattern"
            }
        
        return {
            "match": False,
            "confidence": "high",
            "reasoning": f"Different cities: {target_loc} != {bio_loc}",
            "source": "cyprus_pattern"
        }
    
    # 2. Basit string match
    if target_norm in normalize_text(full_text):
        return {
            "match": True,
            "confidence": "high",
            "reasoning": "Direct text match",
            "source": "string_match"
        }
    
    # 3. AI fallback
    if not openai_client:
        return {"match": False, "confidence": "none"}
    
    try:
        prompt = f"""Match location?

Bio: "{biography}"
Username: "{username}"
Target: "{target_location}"

KKTC context:
- Keywords: cypriot, kıbrıslı, cyprus, kıbrıs = KKTC content
- KKTC = TRNC = Northern Cyprus = Kuzey Kıbrıs
- Cities: Lefkoşa, Girne, Gazimağusa, Güzelyurt
- Username can contain location hints (urban_cypriot = cypriot)

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
        
        match_result = check_location_match(bio, target_location, username)
        
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
        {"bio": "Urban ⚡️", "username": "urban_cypriot", "target": "KKTC"},
        {"bio": "Cyprus lifestyle blogger", "username": "cypriot_life", "target": "Kıbrıs"},
        {"bio": "Kıbrıslı yemek bloggerı 🍕", "username": "foodie", "target": "KKTC"},
        {"bio": "📍 Lefkoşa", "username": "lefkosa_daily", "target": "Lefkoşa"},
        {"bio": "#cyprus #cypriot #girne", "username": "travel", "target": "KKTC"},
        {"bio": "İstanbul food", "username": "istanbul_food", "target": "KKTC"},
    ]
    
    print("🧪 KKTC Location Tests (including username):\n")
    for i, test in enumerate(test_cases, 1):
        result = check_location_match(test["bio"], test["target"], test["username"])
        status = "✅" if result["match"] else "❌"
        print(f"{i}. {status}")
        print(f"   Username: @{test['username']}")
        print(f"   Bio: {test['bio']}")
        print(f"   Target: {test['target']}")
        print(f"   Result: {result.get('reasoning', 'No match')}")
        print()
