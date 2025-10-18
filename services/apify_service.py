"""
Apify Service - Instagram Trend ve Influencer Keşfi
"""
import os
from typing import List, Dict, Any, Optional
from apify_client import ApifyClient
import logging

logger = logging.getLogger(__name__)

class ApifyService:
    def __init__(self):
        self.api_token = os.getenv("APIFY_API_TOKEN")
        self.client = ApifyClient(self.api_token) if self.api_token else None
        
    def _is_available(self) -> bool:
        if not self.client:
            logger.warning("Apify API token not configured")
            return False
        return True
    
    async def scan_trending_hashtags(self, keywords: List[str], limit: int = 30) -> List[Dict]:
        """Business: Keyword bazlı trendleri erkenden yakala"""
        if not self._is_available():
            return self._mock_trends(keywords)
        
        all_trends = []
        for keyword in keywords[:5]:
            try:
                logger.info(f"🔍 Scanning hashtag: #{keyword}")
                run = self.client.actor("apify/instagram-hashtag-scraper").call(
                    run_input={"hashtags": [keyword], "resultsLimit": limit, "addParentData": False}
                )
                posts = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
                if not posts:
                    continue
                
                total_engagement = sum(p.get("likesCount", 0) + p.get("commentsCount", 0) * 2 for p in posts)
                avg_engagement = total_engagement / len(posts) if posts else 0
                trending_score = self._calculate_trending_score(posts)
                
                all_trends.append({
                    "keyword": keyword,
                    "post_count": len(posts),
                    "avg_engagement": round(avg_engagement, 2),
                    "trending_score": round(trending_score, 3),
                    "sample_posts": posts[:5]
                })
            except Exception as e:
                logger.error(f"Error scanning #{keyword}: {e}")
                continue
        
        all_trends.sort(key=lambda x: x["trending_score"], reverse=True)
        return all_trends
    
    def _calculate_trending_score(self, posts: List[Dict]) -> float:
        if not posts:
            return 0.0
        total_score = 0
        for post in posts:
            likes = post.get("likesCount", 0)
            comments = post.get("commentsCount", 0)
            engagement = likes + (comments * 2)
            comment_ratio = comments / likes if likes > 0 else 0
            score = (engagement * 0.7) + (comment_ratio * 1000 * 0.3)
            total_score += score
        avg_score = total_score / len(posts)
        return min(avg_score / 10000, 1.0)
    
    async def search_influencers_by_niche(
        self, niche_keywords: List[str], min_followers: int = 10000,
        max_followers: int = 500000, limit: int = 20
    ) -> List[Dict]:
        """Business: Nişe uygun micro/mid-tier influencer bul"""
        if not self._is_available():
            return self._mock_influencers(niche_keywords)
        
        all_influencers = []
        for keyword in niche_keywords[:3]:
            try:
                logger.info(f"🔍 Searching influencers in #{keyword}")
                run = self.client.actor("apify/instagram-hashtag-scraper").call(
                    run_input={"hashtags": [keyword], "resultsLimit": limit * 2, "addParentData": True}
                )
                posts = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
                seen_usernames = set()
                
                for post in posts:
                    username = post.get("ownerUsername")
                    if not username or username in seen_usernames:
                        continue
                    followers = post.get("ownerFollowersCount", 0)
                    if followers < min_followers or followers > max_followers:
                        continue
                    
                    likes = post.get("likesCount", 0)
                    comments = post.get("commentsCount", 0)
                    engagement_rate = ((likes + comments) / followers * 100) if followers > 0 else 0
                    tier = self._calculate_influencer_tier(followers, engagement_rate)
                    
                    seen_usernames.add(username)
                    all_influencers.append({
                        "username": username,
                        "followers": followers,
                        "engagement_rate": round(engagement_rate, 2),
                        "tier": tier,
                        "niche": keyword,
                        "profile_url": f"https://instagram.com/{username}"
                    })
            except Exception as e:
                logger.error(f"Error searching influencers for #{keyword}: {e}")
                continue
        
        all_influencers.sort(key=lambda x: x["engagement_rate"], reverse=True)
        return all_influencers[:limit]
    
    def _calculate_influencer_tier(self, followers: int, engagement_rate: float) -> str:
        if engagement_rate >= 5 and 10000 <= followers <= 100000:
            return "A-Tier"
        elif engagement_rate >= 3:
            return "B-Tier"
        else:
            return "C-Tier"
    
    async def get_profile_details(self, username: str) -> Optional[Dict]:
        if not self._is_available():
            return None
        try:
            run = self.client.actor("apify/instagram-profile-scraper").call(
                run_input={"username": [username]}
            )
            items = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
            return items[0] if items else None
        except Exception as e:
            logger.error(f"Error fetching profile @{username}: {e}")
            return None
    
    def _mock_trends(self, keywords: List[str]) -> List[Dict]:
        import random
        return [{"keyword": kw, "post_count": random.randint(100, 1000),
                "avg_engagement": random.randint(50, 500),
                "trending_score": round(random.uniform(0.3, 0.9), 3),
                "sample_posts": []} for kw in keywords]
    
    def _mock_influencers(self, keywords: List[str]) -> List[Dict]:
        import random
        return [{"username": f"influencer_{i}", "followers": random.randint(10000, 100000),
                "engagement_rate": round(random.uniform(2, 8), 2),
                "tier": random.choice(["A-Tier", "B-Tier", "C-Tier"]),
                "niche": keywords[0] if keywords else "general",
                "profile_url": f"https://instagram.com/influencer_{i}"} for i in range(10)]

apify_service = ApifyService()
