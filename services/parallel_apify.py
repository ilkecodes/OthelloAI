"""Parallel Apify Search - FAST"""
import os
from apify_client import ApifyClient
from typing import List, Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.append('..')
from services.influencer_scorer import calculate_niche_score

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def search_single_query(query: str, max_results: int = 30) -> List[str]:
    """Tek bir query ile arama yap - usernames döndür"""
    try:
        print(f"  🔍 Searching: {query[:50]}...")
        
        # Instagram search API kullan (daha hızlı)
        run = client.actor("apify/instagram-hashtag-scraper").call(
            run_input={
                "hashtags": [query.replace(" OR ", "").split()[0]],  # İlk kelimeyi al
                "resultsLimit": max_results
            },
            timeout_secs=60
        )
        
        usernames = set()
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            username = item.get("ownerUsername")
            if username:
                usernames.add(username)
        
        print(f"    ✓ Found {len(usernames)} profiles")
        return list(usernames)
        
    except Exception as e:
        print(f"    ✗ Error: {str(e)[:50]}")
        return []

def get_profile_details(usernames: List[str]) -> List[Dict]:
    """Username'lerden profil detaylarını çek"""
    
    if not usernames:
        return []
    
    try:
        print(f"📊 Getting details for {len(usernames)} profiles...")
        
        run = client.actor("apify/instagram-profile-scraper").call(
            run_input={
                "usernames": usernames[:50],  # Max 50
                "resultsLimit": len(usernames),
                "addParentData": True
            },
            timeout_secs=180
        )
        
        profiles = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            latest_posts = item.get("latestPosts", [])[:12]
            if not latest_posts:
                continue
            
            total_likes = sum(p.get("likesCount", 0) for p in latest_posts)
            total_comments = sum(p.get("commentsCount", 0) for p in latest_posts)
            followers = item.get("followersCount", 0)
            
            if followers == 0:
                continue
            
            avg_likes = total_likes / len(latest_posts)
            avg_comments = total_comments / len(latest_posts)
            engagement_rate = ((avg_likes + avg_comments) / followers * 100)
            
            profiles.append({
                "username": item.get("username"),
                "full_name": item.get("fullName"),
                "biography": item.get("biography"),
                "followers": followers,
                "following": item.get("followsCount", 0),
                "posts_count": item.get("postsCount", 0),
                "engagement_rate": round(engagement_rate, 2),
                "avg_likes": int(avg_likes),
                "avg_comments": int(avg_comments),
                "is_verified": item.get("verified", False),
                "is_business": item.get("businessCategoryName") is not None,
                "business_category": item.get("businessCategoryName"),
                "profile_pic": item.get("profilePicUrl"),
                "external_url": item.get("externalUrl"),
                "instagram_url": f"https://instagram.com/{item.get('username')}",
                "latest_posts": [
                    {
                        "url": p.get("url"),
                        "caption": p.get("caption", "")[:100],
                        "likes": p.get("likesCount", 0),
                        "comments": p.get("commentsCount", 0),
                    }
                    for p in latest_posts[:5]
                ]
            })
        
        print(f"✅ Got {len(profiles)} valid profiles")
        return profiles
        
    except Exception as e:
        print(f"❌ Profile details error: {e}")
        return []

async def parallel_search(strategy: dict) -> dict:
    """Paralel arama yap"""
    
    print(f"🚀 Starting parallel search...")
    
    search_queries = strategy.get("search_queries", [])[:3]  # Max 3 query
    known_usernames = strategy.get("known_usernames", [])
    
    # Paralel arama
    all_usernames = set(known_usernames)
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(search_single_query, query, 30)
            for query in search_queries
        ]
        
        for future in futures:
            try:
                usernames = future.result(timeout=90)
                all_usernames.update(usernames)
            except Exception as e:
                print(f"⚠️ Thread error: {e}")
    
    print(f"📦 Total unique profiles: {len(all_usernames)}")
    
    # Profil detaylarını çek
    profiles = get_profile_details(list(all_usernames))
    
    # Skorlama yap
    for profile in profiles:
        score_data = calculate_niche_score(profile, strategy)
        profile["score"] = score_data["total_score"]
        profile["score_breakdown"] = score_data["breakdown"]
        profile["match_reasons"] = score_data["reasons"]
        profile["badge"] = score_data["badge"]
    
    # Skora göre sırala ve filtrele
    profiles.sort(key=lambda x: x["score"], reverse=True)
    qualified_profiles = [p for p in profiles if p["score"] >= 40]  # Min 40 skor
    
    print(f"✅ {len(qualified_profiles)} qualified influencers (score >= 40)")
    
    return {
        "success": True,
        "strategy": strategy,
        "total_searched": len(all_usernames),
        "qualified_count": len(qualified_profiles),
        "profiles": qualified_profiles[:20]  # Top 20
    }

async def search_instagram_influencers(
    niche_key: str,
    custom_query: str = None,
    location: str = None
) -> dict:
    """Ana arama fonksiyonu"""
    
    from services.ai_strategist import create_search_strategy
    
    # Strateji oluştur
    strategy = create_search_strategy(niche_key, custom_query, location)
    
    # Paralel arama
    result = await parallel_search(strategy)
    
    return result
