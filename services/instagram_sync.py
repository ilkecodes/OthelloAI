"""
Instagram Sync - Apify ile otomatik corpus toplama
"""
import os
from typing import List, Dict
from apify_client import ApifyClient

class InstagramSync:
    
    def __init__(self):
        api_token = os.getenv("APIFY_API_TOKEN")
        self.client = ApifyClient(api_token) if api_token else None
    
    async def sync_profile(self, username: str, max_posts: int = 50) -> List[Dict]:
        """Instagram profilinden son postları çek"""
        
        if not self.client:
            return []
        
        try:
            # Apify Instagram Profile Scraper
            run = self.client.actor("apify/instagram-profile-scraper").call(
                run_input={
                    "username": [username],
                    "resultsLimit": max_posts
                }
            )
            
            posts = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                if item.get('latestPosts'):
                    for post in item['latestPosts'][:max_posts]:
                        caption = post.get('caption', '')
                        if caption and len(caption) > 10:
                            posts.append({
                                "text": caption,
                                "url": post.get('url', ''),
                                "engagement_score": (
                                    post.get('likesCount', 0) + 
                                    post.get('commentsCount', 0) * 2
                                )
                            })
            
            return posts
            
        except Exception as e:
            print(f"Instagram sync failed: {e}")
            return []

# Singleton
instagram_sync = InstagramSync()
