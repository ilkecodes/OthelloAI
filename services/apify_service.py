from apify_client import ApifyClient
from config import settings
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class ApifyService:
    def __init__(self):
        if not settings.APIFY_API_TOKEN:
            logger.warning("Apify API token not configured")
            self.client = None
        else:
            self.client = ApifyClient(settings.APIFY_API_TOKEN)
    
    async def search_instagram_profiles(
        self,
        usernames: List[str] = None,
        hashtag: str = None,
        limit: int = 10
    ) -> List[Dict]:
        """Search Instagram profiles using Apify"""
        
        if not self.client:
            return [{
                "error": "Apify not configured",
                "message": "Add APIFY_API_TOKEN to .env"
            }]
        
        try:
            # Instagram Profile Scraper actor
            actor_id = "apify/instagram-profile-scraper"
            
            run_input = {
                "usernames": usernames or [],
                "resultsLimit": limit
            }
            
            # Run the actor
            run = self.client.actor(actor_id).call(run_input=run_input)
            
            # Get results
            results = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append({
                    "username": item.get("username"),
                    "full_name": item.get("fullName"),
                    "followers": item.get("followersCount", 0),
                    "following": item.get("followsCount", 0),
                    "posts": item.get("postsCount", 0),
                    "biography": item.get("biography"),
                    "is_verified": item.get("verified", False),
                    "is_business": item.get("isBusinessAccount", False),
                    "profile_pic_url": item.get("profilePicUrl"),
                    "external_url": item.get("externalUrl")
                })
            
            logger.info(f"Found {len(results)} Instagram profiles")
            return results
            
        except Exception as e:
            logger.error(f"Apify error: {e}")
            return [{"error": str(e)}]
    
    async def search_by_hashtag(
        self,
        hashtag: str,
        limit: int = 20
    ) -> List[Dict]:
        """Search Instagram by hashtag"""
        
        if not self.client:
            return [{"error": "Apify not configured"}]
        
        try:
            actor_id = "apify/instagram-hashtag-scraper"
            
            run_input = {
                "hashtags": [hashtag],
                "resultsLimit": limit
            }
            
            run = self.client.actor(actor_id).call(run_input=run_input)
            
            results = []
            users_seen = set()
            
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                username = item.get("ownerUsername")
                if username and username not in users_seen:
                    users_seen.add(username)
                    results.append({
                        "username": username,
                        "full_name": item.get("ownerFullName"),
                        "likes": item.get("likesCount", 0),
                        "comments": item.get("commentsCount", 0),
                        "is_verified": item.get("isOwnerVerified", False)
                    })
            
            logger.info(f"Found {len(results)} users from #{hashtag}")
            return results
            
        except Exception as e:
            logger.error(f"Hashtag search error: {e}")
            return [{"error": str(e)}]

apify_service = ApifyService()
