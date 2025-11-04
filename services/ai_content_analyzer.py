"""AI-Powered Content Analysis"""
import os
from openai import OpenAI
import json
from typing import Dict, List

client = OpenAI(api_key=os.getenv("OPENAI_API_TOKEN"))

def analyze_bio_match(bio: str, search_query: str, location: str = None) -> Dict:
    """Bio'nun arama ile uyumunu analiz et"""
    
    if not bio:
        return {"score": 0, "keywords": [], "relevance": "none"}
    
    try:
        location_text = f" in {location}" if location else ""
        
        prompt = f"""Analyze if this Instagram bio matches the search query.

Search Query: "{search_query}{location_text}"
Bio: "{bio}"

Rate the match from 0-100 and extract relevant keywords.
Return JSON:
{{
  "score": 85,
  "keywords": ["food", "blogger", "istanbul"],
  "relevance": "high|medium|low|none",
  "reason": "Bio mentions food blogging and Istanbul location"
}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"⚠️ Bio analysis error: {e}")
        # Fallback: simple keyword matching
        bio_lower = bio.lower()
        query_words = search_query.lower().split()
        matched = sum(1 for word in query_words if word in bio_lower)
        score = (matched / len(query_words)) * 100 if query_words else 0
        
        return {
            "score": min(score, 100),
            "keywords": [w for w in query_words if w in bio_lower],
            "relevance": "medium" if score > 50 else "low",
            "reason": "Keyword matching"
        }

def analyze_content_consistency(posts: List[Dict], search_query: str) -> Dict:
    """Son postların tutarlılığını analiz et"""
    
    if not posts or len(posts) < 3:
        return {"score": 0, "consistency": 0, "reason": "Not enough posts"}
    
    try:
        # Son 10 postun caption'larını topla
        captions = [p.get("caption", "")[:200] for p in posts[:10]]
        captions_text = "\n---\n".join([f"Post {i+1}: {c}" for i, c in enumerate(captions) if c])
        
        if not captions_text:
            return {"score": 0, "consistency": 0, "reason": "No captions"}
        
        prompt = f"""Analyze if these Instagram post captions are consistent with the topic: "{search_query}"

Posts:
{captions_text}

Rate consistency from 0-100. Return JSON:
{{
  "score": 85,
  "consistency": 90,
  "matching_posts": 9,
  "total_posts": 10,
  "reason": "9 out of 10 posts are about food and restaurants"
}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"⚠️ Content consistency error: {e}")
        return {"score": 50, "consistency": 50, "reason": "Analysis failed"}

def generate_smart_hashtags(search_query: str, location: str = None) -> List[str]:
    """Akıllı hashtag üret"""
    
    try:
        location_text = f" in {location}" if location else ""
        
        prompt = f"""Generate 5 highly relevant Instagram hashtags for finding influencers about: "{search_query}{location_text}"

Rules:
1. Mix of popular and niche hashtags
2. Include location if provided
3. Both English and Turkish variants
4. No spaces, no # symbol

Return JSON array of 5 hashtags:
{{"hashtags": ["foodblogger", "istanbulfood", "yemek", "foodie", "gastronomy"]}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        hashtags = result.get("hashtags", [])
        
        # Temizle
        hashtags = [h.strip().lower().replace("#", "").replace(" ", "") for h in hashtags]
        
        print(f"🏷️  Generated hashtags: {hashtags}")
        return hashtags[:5]
        
    except Exception as e:
        print(f"⚠️ Hashtag generation error: {e}")
        # Fallback
        base = search_query.replace(" ", "").lower()
        fallback = [base]
        if location:
            fallback.append(location.replace(" ", "").lower())
        return fallback
