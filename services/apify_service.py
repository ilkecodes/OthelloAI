"""Apify Instagram Scraper Service"""
from apify_client import ApifyClient
import os

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def search_instagram_by_hashtag(hashtag: str, limit: int = 30):
    """Instagram'da hashtag ile arama - TAM VERİ"""
    
    try:
        print(f"📸 Searching Instagram: #{hashtag}")
        
        # Hashtag scraper kullan
        run = client.actor("apify/instagram-hashtag-scraper").call(
            run_input={
                "hashtags": [hashtag],
                "resultsLimit": limit
            },
            timeout_secs=120
        )
        
        profiles_dict = {}  # Username'e göre dedup için
        
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            username = item.get("ownerUsername", "")
            
            if not username or username in profiles_dict:
                continue
            
            # Profile data'yı çek
            owner_data = item.get("owner", {})
            
            profiles_dict[username] = {
                "username": username,
                "full_name": item.get("ownerFullName") or owner_data.get("full_name", ""),
                "biography": "", # Hashtag scraper'da bio yok
                "followers": owner_data.get("edge_followed_by", {}).get("count", 0),
                "following": owner_data.get("edge_follow", {}).get("count", 0),
                "posts_count": owner_data.get("edge_owner_to_timeline_media", {}).get("count", 0),
                "engagement_rate": calculate_engagement(item),
                "profile_pic": item.get("displayUrl", ""),
                "instagram_url": f"https://instagram.com/{username}",
                "is_verified": owner_data.get("is_verified", False),
                "is_business": owner_data.get("is_business_account", False)
            }
        
        profiles = list(profiles_dict.values())
        print(f"✅ Found {len(profiles)} unique profiles")
        
        return profiles
        
    except Exception as e:
        print(f"❌ Hashtag scraper error: {e}")
        # Fallback: Profile scraper dene
        return search_instagram_profiles_directly(hashtag, limit)

def search_instagram_profiles_directly(query: str, limit: int = 20):
    """Direkt profile scraper kullan - DAHA DETAYLI VERİ"""
    
    try:
        print(f"📸 Using profile scraper for: {query}")
        
        # Query'den username listesi oluştur (basit yaklaşım)
        usernames = [query.replace(' ', '_'), f"{query}_official"]
        
        run = client.actor("apify/instagram-profile-scraper").call(
            run_input={
                "usernames": usernames[:5],
                "resultsLimit": limit
            },
            timeout_secs=120
        )
        
        profiles = []
        
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            profiles.append({
                "username": item.get("username", ""),
                "full_name": item.get("fullName", ""),
                "biography": item.get("biography", ""),
                "followers": item.get("followersCount", 0),
                "following": item.get("followsCount", 0),
                "posts_count": item.get("postsCount", 0),
                "engagement_rate": round(item.get("engagementRate", 0) * 100, 2),
                "profile_pic": item.get("profilePicUrl", ""),
                "instagram_url": f"https://instagram.com/{item.get('username', '')}",
                "is_verified": item.get("verified", False),
                "is_business": item.get("businessCategoryName") is not None
            })
        
        print(f"✅ Found {len(profiles)} profiles with full data")
        return profiles
        
    except Exception as e:
        print(f"❌ Profile scraper error: {e}")
        return []

def calculate_engagement(post_data: dict) -> float:
    """Post verisinden engagement rate hesapla"""
    
    try:
        likes = post_data.get("likesCount", 0)
        comments = post_data.get("commentsCount", 0)
        
        owner = post_data.get("owner", {})
        followers = owner.get("edge_followed_by", {}).get("count", 0)
        
        if followers > 0:
            engagement = ((likes + comments) / followers) * 100
            return round(engagement, 2)
        
        return 0.0
        
    except:
        return 0.0

def get_profile_details(username: str):
    """Tek bir profile için detaylı veri çek"""
    
    try:
        print(f"📸 Getting profile details: @{username}")
        
        run = client.actor("apify/instagram-profile-scraper").call(
            run_input={
                "usernames": [username],
                "resultsLimit": 1
            },
            timeout_secs=60
        )
        
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            return {
                "username": item.get("username", ""),
                "full_name": item.get("fullName", ""),
                "biography": item.get("biography", ""),
                "followers": item.get("followersCount", 0),
                "following": item.get("followsCount", 0),
                "posts_count": item.get("postsCount", 0),
                "engagement_rate": round(item.get("engagementRate", 0) * 100, 2),
                "profile_pic": item.get("profilePicUrl", ""),
                "instagram_url": f"https://instagram.com/{username}",
                "is_verified": item.get("verified", False),
                "is_business": item.get("businessCategoryName") is not None,
                "external_url": item.get("externalUrl", ""),
                "category": item.get("businessCategoryName", "")
            }
        
        return None
        
    except Exception as e:
        print(f"❌ Profile details error: {e}")
        return None
