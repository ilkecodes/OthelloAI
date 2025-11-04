"""Influencer Discovery API - Konum Filtreli"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
sys.path.append('..')
from services.apify_service import search_instagram_by_hashtag
from services.location_extractor import filter_by_location
import os
from openai import OpenAI

router = APIRouter()

api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_TOKEN")
openai_client = OpenAI(api_key=api_key)

class InfluencerSearchRequest(BaseModel):
    search_query: str
    location: Optional[str] = None

@router.post("/search")
async def search_influencers(request: InfluencerSearchRequest):
    """
    Influencer ara - KONUM FİLTRELİ
    """
    
    print(f"\n{'='*60}")
    print(f"🔍 Search: {request.search_query}")
    if request.location:
        print(f"📍 Location: {request.location}")
    print(f"{'='*60}\n")
    
    try:
        # 1. Hashtag üret
        print("1️⃣ Generating hashtags...")
        hashtags = generate_hashtags(request.search_query)
        print(f"   Generated: {hashtags[:3]}")
        
        # 2. Instagram'dan profil çek
        print(f"\n2️⃣ Searching Instagram with #{hashtags[0]}...")
        profiles = search_instagram_by_hashtag(hashtags[0])
        print(f"   Found: {len(profiles)} profiles")
        
        # 3. KONUM FİLTRESİ
        if request.location:
            print(f"\n3️⃣ Applying location filter: {request.location}")
            profiles = filter_by_location(profiles, request.location)
            print(f"   After filter: {len(profiles)} profiles")
        
        print(f"\n{'='*60}")
        print(f"✅ Returning {len(profiles)} profiles")
        print(f"{'='*60}\n")
        
        return {
            "success": True,
            "profiles": profiles[:20],
            "total": len(profiles),
            "hashtags_used": hashtags[:3]
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

def generate_hashtags(query: str) -> list:
    """AI ile hashtag üret"""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"Generate 5 Instagram hashtags for: {query}\nReturn as comma-separated list."
            }],
            temperature=0.5
        )
        
        hashtags_text = response.choices[0].message.content
        hashtags = [h.strip().replace('#', '') for h in hashtags_text.split(',')]
        return hashtags[:5]
        
    except Exception as e:
        print(f"⚠️ Hashtag generation error: {e}")
        return [query.replace(' ', '')]
