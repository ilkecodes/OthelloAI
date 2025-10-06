from apify_client import ApifyClient
from typing import List, Dict, Any
import logging
from datetime import datetime
from app.hashtags import get_all_hashtags_for_client

logger = logging.getLogger(__name__)

class ApifyScanner:
    """Async wrapper for Apify Instagram scanning with hashtag support"""
    
    def __init__(self, api_token: str = None):
        import os
        self.api_token = api_token or os.environ.get("APIFY_API_TOKEN")
        if not self.api_token:
            logger.warning("APIFY_API_TOKEN not set, using mock data")
        self.client = ApifyClient(self.api_token) if self.api_token else None
    
    async def scan_instagram_hashtag(self, hashtag: str, limit: int = 20) -> List[Dict]:
        """Scan Instagram for a single hashtag"""
        if not self.client:
            logger.warning(f"No Apify token, returning mock data for #{hashtag}")
            return self._mock_posts(hashtag, limit)
        
        try:
            logger.info(f"Scanning Instagram #{hashtag} with Apify...")
            
            run = self.client.actor('apify/instagram-hashtag-scraper').call(
                run_input={
                    "hashtags": [hashtag],
                    "resultsLimit": limit,
                    "addParentData": False
                }
            )
            
            posts = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                posts.append({
                    'id': item.get('id'),
                    'caption': item.get('caption', ''),
                    'likes': item.get('likesCount', 0),
                    'comments': item.get('commentsCount', 0),
                    'engagement': item.get('likesCount', 0) + item.get('commentsCount', 0),
                    'timestamp': item.get('timestamp'),
                    'url': item.get('url'),
                    'owner': item.get('ownerUsername'),
                    'hashtag': hashtag
                })
            
            logger.info(f"Found {len(posts)} posts for #{hashtag}")
            return posts
            
        except Exception as e:
            logger.error(f"Error scanning #{hashtag}: {e}")
            return []
    
    async def scan_instagram_for_client(self, client_id: int, db_session) -> List[Dict]:
        """Scan Instagram using client's niche hashtags"""
        from app.models.client import Client
        
        client = db_session.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise ValueError(f"Client {client_id} not found")
        
        # Get niche hashtags
        hashtags = get_all_hashtags_for_client(client.name, include_longtail=False)
        
        if not hashtags:
            logger.warning(f"No hashtags for {client.name}, using keywords")
            hashtags = [kw.strip() for kw in client.keywords.split(",") if kw.strip()]
        
        # Use top 3 hashtags
        target_hashtags = hashtags[:3]
        logger.info(f"Scanning for {client.name} with hashtags: {target_hashtags}")
        
        all_posts = []
        for hashtag in target_hashtags:
            posts = await self.scan_instagram_hashtag(hashtag, limit=15)
            all_posts.extend(posts)
        
        return all_posts
    
    def _mock_posts(self, hashtag: str, limit: int) -> List[Dict]:
        """Generate mock posts for testing without Apify token"""
        import random
        return [
            {
                'id': f'mock_{i}',
                'caption': f'Sample post about #{hashtag}',
                'likes': random.randint(50, 500),
                'comments': random.randint(5, 50),
                'engagement': random.randint(55, 550),
                'timestamp': datetime.now().isoformat(),
                'url': f'https://instagram.com/p/mock_{i}',
                'owner': f'user_{i}',
                'hashtag': hashtag
            }
            for i in range(min(limit, 10))
        ]
async def scan_instagram_profile(self, username: str, max_posts: int = 10) -> List[Dict[str, Any]]:
    """Scan an Instagram profile's recent posts."""
    
    if not self.apify_token:
        print(f"No Apify token, returning mock data for @{username}")
        return self._generate_mock_posts(username)
    
    try:
        print(f"Scanning Instagram profile: @{username}")
        
        run_input = {
            "username": [username],
            "resultsLimit": max_posts
        }
        
        run = self.client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
        
        posts = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            if item.get('latestPosts'):
                for post in item['latestPosts'][:max_posts]:
                    posts.append({
                        'caption': post.get('caption', ''),
                        'likesCount': post.get('likesCount', 0),
                        'commentsCount': post.get('commentsCount', 0),
                        'url': post.get('url', ''),
                        'timestamp': post.get('timestamp', '')
                    })
        
        print(f"✅ Found {len(posts)} posts from @{username}")
        return posts
        
    except Exception as e:
        print(f"Error scanning profile: {e}")
        return self._generate_mock_posts(username)
