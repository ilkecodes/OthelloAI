"""AI-Powered Search Strategist"""
import os
from openai import OpenAI
import json
from services.niche_definitions import get_niche_config

client = OpenAI(api_key=os.getenv("OPENAI_API_TOKEN"))

def create_search_strategy(niche_key: str, custom_query: str = None, location: str = None) -> dict:
    """OpenAI ile arama stratejisi oluştur"""
    
    niche_config = get_niche_config(niche_key)
    
    # Custom query varsa OpenAI'a sor
    if niche_key == "custom" and custom_query:
        return ask_openai_strategy(custom_query, location)
    
    # Predefined niş için hazır strateji
    strategy = {
        "search_queries": niche_config["search_templates"],
        "bio_keywords": niche_config["bio_keywords"],
        "location_keywords": [],
        "known_usernames": [],
        "min_followers": niche_config["min_followers"],
        "ideal_engagement": niche_config["ideal_engagement"]
    }
    
    # Lokasyon varsa ekle
    if location:
        strategy["location_keywords"] = [location.lower()]
        # Lokasyonu search query'lere ekle
        strategy["search_queries"] = [
            f"{q} {location}" for q in strategy["search_queries"][:2]  # İlk 2'sine lokasyon ekle
        ]
    
    print(f"📋 Strategy: {len(strategy['search_queries'])} queries, {len(strategy['bio_keywords'])} keywords")
    
    return strategy

def ask_openai_strategy(custom_query: str, location: str = None) -> dict:
    """Custom query için OpenAI'dan strateji al"""
    
    try:
        location_text = f" in {location}" if location else ""
        print(f"🤖 AI analyzing: '{custom_query}'{location_text}")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Sen Instagram influencer arama stratejisti sin. Verilen keyword için:

1. 2-3 tane Instagram search query oluştur (OR operatörü kullan)
2. Bio'da aranacak anahtar kelimeler (5-10 tane, hem İngilizce hem Türkçe)
3. Minimum takipçi sayısı öner
4. İdeal engagement rate öner
5. Bu nişte bildiğin gerçek username'ler varsa ekle (5-10 tane)

JSON format:
{
  "search_queries": ["query1", "query2"],
  "bio_keywords": ["keyword1", "keyword2", ...],
  "location_keywords": ["istanbul", "turkey"],
  "known_usernames": ["user1", "user2", ...],
  "min_followers": 5000,
  "ideal_engagement": 0.02
}"""
                },
                {
                    "role": "user",
                    "content": f"{custom_query}{location_text}"
                }
            ],
            temperature=0.7,
            max_tokens=400,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        strategy = json.loads(content)
        
        print(f"✅ AI strategy: {len(strategy.get('search_queries', []))} queries")
        
        return strategy
        
    except Exception as e:
        print(f"❌ AI strategy error: {e}, using fallback")
        return {
            "search_queries": [custom_query],
            "bio_keywords": custom_query.lower().split(),
            "location_keywords": [location.lower()] if location else [],
            "known_usernames": [],
            "min_followers": 3000,
            "ideal_engagement": 0.02
        }
