import os
from typing import List, Dict, Any
from apify_client import ApifyClient
import logging

logger = logging.getLogger(__name__)

class InstagramSync:
    """Instagram profile sync for brand voice"""
    
    def __init__(self):
        self.token = os.getenv("APIFY_API_TOKEN")
        self.client = ApifyClient(self.token) if self.token else None
        logger.info(f"✅ InstagramSync initialized (Token: {bool(self.token)})")
    
    async def sync_profile(self, username: str, max_posts: int = 15) -> List[Dict[str, Any]]:
        """Sync Instagram profile posts"""
        if not self.client:
            logger.warning("❌ No Apify token")
            return []
        
        try:
            logger.info(f"📥 Fetching {max_posts} posts from @{username}...")
            
            # Instagram Profile Scraper (daha basit)
            run_input = {
                "usernames": [username],
                "resultsLimit": 1  # Sadece profil bilgisi
            }
            
            run = self.client.actor("apify/instagram-profile-scraper").call(
                run_input=run_input,
                timeout_secs=120
            )
            
            posts = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                # latestPosts içindeki postları al
                if item.get("latestPosts"):
                    for post in item["latestPosts"][:max_posts]:
                        caption = post.get("caption", "")
                        if not caption or len(caption) < 10:
                            continue
                        
                        likes = post.get("likesCount", 0) or 0
                        comments = post.get("commentsCount", 0) or 0
                        
                        posts.append({
                            "text": caption,
                            "url": post.get("url", ""),
                            "engagement_score": int(likes + (comments * 2))
                        })
            
            logger.info(f"✅ Found {len(posts)} posts from @{username}")
            return posts
            
        except Exception as e:
            logger.error(f"❌ Instagram sync error for @{username}: {str(e)}")
            return []

# Singleton
instagram_sync = InstagramSync()
