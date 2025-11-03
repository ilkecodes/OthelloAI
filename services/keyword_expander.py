"""Keyword Expansion with OpenAI - Location Support"""
import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_TOKEN"))

def expand_keywords(query: str, location: str = None) -> list[str]:
    """OpenAI ile keyword'leri çeşitlendir - konum desteği ile"""
    
    try:
        # Konum varsa query'ye ekle
        full_query = f"{query} {location}" if location else query
        
        print(f"🤖 OpenAI expanding: '{full_query}'")
        
        location_instruction = ""
        if location:
            location_instruction = f"\nKonum: {location} - Bu konuma özel hashtag'ler de ekle (örn: istanbul, turkey, ankara vb.)"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""Sen Instagram hashtag uzmanısın. Verilen keyword için:
1. İlgili Instagram hashtag'leri üret (boşluksuz, küçük harf)
2. Hem Türkçe hem İngilizce varyasyonlar ekle
3. Popüler ve niş hashtag'leri dengele
4. En fazla 12 hashtag döndür
5. Sadece JSON array döndür, başka açıklama yok{location_instruction}

Örnek input: "food blogger" + konum: "istanbul"
Örnek output: ["foodblogger", "istanbulfood", "foodie", "yemekblog", "istanbulrestaurant", "foodphotography", "istanbuleats", "turkishfood", "gastronomi", "lezzet", "foodstagram", "istanbul"]"""
                },
                {
                    "role": "user",
                    "content": full_query
                }
            ],
            temperature=0.7,
            max_tokens=250,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        
        try:
            data = json.loads(content)
            if isinstance(data, dict):
                hashtags = data.get("hashtags", list(data.values())[0] if data else [])
            else:
                hashtags = data
            
            if not isinstance(hashtags, list):
                hashtags = [hashtags]
            
            clean_hashtags = []
            for h in hashtags:
                if isinstance(h, str):
                    h = h.strip().lower().replace("#", "").replace(" ", "")
                    if len(h) > 2 and len(h) < 30:
                        clean_hashtags.append(h)
            
            print(f"✅ Expanded to {len(clean_hashtags)} hashtags: {clean_hashtags[:5]}...")
            
            return clean_hashtags[:12]
            
        except json.JSONDecodeError:
            print(f"⚠️ JSON parse failed, using basic expansion")
            return basic_expand(query, location)
    
    except Exception as e:
        print(f"❌ OpenAI error: {e}, falling back to basic")
        return basic_expand(query, location)

def basic_expand(query: str, location: str = None) -> list[str]:
    """Fallback: basit expansion"""
    query = query.lower().strip()
    no_space = query.replace(" ", "")
    words = query.split()
    
    hashtags = [no_space]
    hashtags.extend(words)
    
    if len(words) >= 2:
        hashtags.append(words[0] + words[1])
    
    # Konum varsa ekle
    if location:
        loc_clean = location.lower().replace(" ", "")
        hashtags.append(loc_clean)
        hashtags.append(f"{no_space}{loc_clean}")
    
    return list(set(hashtags))[:8]
