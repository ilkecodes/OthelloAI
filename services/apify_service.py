"""Apify Service - With Location Support"""
import os
from apify_client import ApifyClient
from typing import Optional, List, Dict

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

async def search_instagram_profiles(
    search_query: Optional[str] = None,
    location: Optional[str] = None,
    usernames: Optional[List[str]] = None,
    max_results: int = 20
) -> Dict:
    """Instagram arama - konum desteği ile"""
    
    if usernames:
        profiles = await get_profile_details(usernames[:max_results])
        return {
            "success": True,
            "count": len(profiles),
            "profiles": profiles
        }
    
    elif search_query:
        try:
            # Konum varsa query'ye ekle
            if location:
                hashtags = [
                    search_query.replace(" ", ""),
                    f"{search_query.replace(' ', '')}{location.replace(' ', '')}",
                    location.replace(" ", "")
                ]
            else:
                hashtags = [search_query.replace(" ", "")]
            
            print(f"🔍 Searching: {hashtags}")
            
            all_usernames = set()
            
            for hashtag in hashtags[:2]:  # İlk 2 hashtag
                try:
                    run = client.actor("apify/instagram-hashtag-scraper").call(
                        run_input={
                            "hashtags": [hashtag],
                            "resultsLimit": 30
                        },
                        timeout_secs=60
                    )
                    
                    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                        username = item.get("ownerUsername")
                        if username:
                            all_usernames.add(username)
                except Exception as e:
                    print(f"  ⚠️ Hashtag {hashtag} failed: {e}")
                    continue
            
            print(f"✅ Found {len(all_usernames)} unique profiles")
            
            profiles = await get_profile_details(list(all_usernames)[:20])
            
            return {
                "success": True,
                "search_query": search_query,
                "location": location,
                "count": len(profiles),
                "profiles": profiles
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                "success": False,
                "error": str(e),
                "profiles": []
            }
    
    else:
        return {
            "success": False,
            "error": "Search query or usernames required",
            "profiles": []
        }

async def get_profile_details(usernames: List[str]) -> List[Dict]:
    """Profil detaylarını çek"""
    
    if not usernames:
        return []
    
    try:
        print(f"📊 Getting {len(usernames)} profiles...")
        
        run = client.actor("apify/instagram-profile-scraper").call(
            run_input={
                "usernames": usernames,
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
                        "caption": p.get("caption", "")[:100],
                        "likes": p.get("likesCount", 0),
                        "comments": p.get("commentsCount", 0),
                    }
                    for p in latest_posts[:5]
                ]
            })
        
        profiles.sort(key=lambda x: x["engagement_rate"], reverse=True)
        
        return profiles
        
    except Exception as e:
        print(f"❌ Profile error: {e}")
        return []
