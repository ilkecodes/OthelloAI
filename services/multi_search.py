"""Multi-Hashtag Parallel Search"""
import os
from apify_client import ApifyClient
from typing import List, Dict, Set
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
sys.path.append('..')

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def search_single_hashtag(hashtag: str, max_posts: int = 30) -> Set[str]:
    """Tek hashtag'de arama - usernames döndür"""
    try:
        print(f"  🔍 Searching #{hashtag}...")
        
        run = client.actor("apify/instagram-hashtag-scraper").call(
            run_input={
                "hashtags": [hashtag],
                "resultsLimit": max_posts
            },
            timeout_secs=60
        )
        
        usernames = set()
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            username = item.get("ownerUsername")
            if username:
                usernames.add(username)
        
        print(f"    ✓ Found {len(usernames)} profiles")
        return usernames
        
    except Exception as e:
        print(f"    ✗ Failed: {str(e)[:50]}")
        return set()

def parallel_hashtag_search(hashtags: List[str], max_posts_per_hashtag: int = 30) -> Set[str]:
    """Paralel hashtag araması"""
    
    print(f"🚀 Starting parallel search on {len(hashtags)} hashtags...")
    
    all_usernames = set()
    
    # ThreadPoolExecutor ile paralel arama
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Her hashtag için future oluştur
        future_to_hashtag = {
            executor.submit(search_single_hashtag, hashtag, max_posts_per_hashtag): hashtag
            for hashtag in hashtags
        }
        
        # Sonuçları topla
        for future in as_completed(future_to_hashtag):
            hashtag = future_to_hashtag[future]
            try:
                usernames = future.result(timeout=90)
                all_usernames.update(usernames)
            except Exception as e:
                print(f"  ⚠️ #{hashtag} thread failed: {e}")
    
    print(f"✅ Total unique profiles found: {len(all_usernames)}")
    return all_usernames

def get_detailed_profiles(usernames: List[str]) -> List[Dict]:
    """Profil detaylarını çek"""
    
    if not usernames:
        return []
    
    try:
        print(f"📊 Getting detailed profiles for {len(usernames)} users...")
        
        run = client.actor("apify/instagram-profile-scraper").call(
            run_input={
                "usernames": usernames[:30],  # Max 30 profil
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
                "profile_pic": item.get("profilePicUrl"),
                "instagram_url": f"https://instagram.com/{item.get('username')}",
                "latest_posts": [
                    {
                        "caption": p.get("caption", "")[:200],
                        "likes": p.get("likesCount", 0),
                        "comments": p.get("commentsCount", 0),
                    }
                    for p in latest_posts[:10]
                ]
            })
        
        print(f"✅ Got {len(profiles)} valid profiles with engagement data")
        return profiles
        
    except Exception as e:
        print(f"❌ Profile details error: {e}")
        return []
