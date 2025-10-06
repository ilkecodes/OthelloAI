import os
from typing import List, Dict, Any
from apify_client import ApifyClient

class InfluencerDiscovery:
    """Discover and analyze influencers in niche."""
    
    def __init__(self):
        self.apify_token = os.getenv("APIFY_API_TOKEN")
        if self.apify_token:
            self.client = ApifyClient(self.apify_token)
    
    async def find_niche_influencers(
        self, 
        hashtags: List[str], 
        min_followers: int = 10000,
        max_followers: int = 500000
    ) -> List[Dict[str, Any]]:
        """Find micro/mid-tier influencers in niche."""
        
        if not self.apify_token:
            print("No Apify token, skipping influencer discovery")
            return []
        
        try:
            influencers = []
            
            for hashtag in hashtags[:3]:  # Limit to avoid rate limits
                print(f"Searching influencers for #{hashtag}")
                
                run_input = {
                    "hashtags": [hashtag],
                    "resultsLimit": 20
                }
                
                run = self.client.actor("apify/instagram-hashtag-scraper").call(run_input=run_input)
                
                for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                    owner = item.get('ownerUsername')
                    followers = item.get('ownerFollowers', 0)
                    
                    if min_followers <= followers <= max_followers:
                        influencers.append({
                            'username': owner,
                            'followers': followers,
                            'engagement': item.get('likesCount', 0),
                            'hashtag': hashtag,
                            'profile_url': f"https://instagram.com/{owner}"
                        })
            
            # Deduplicate and sort by engagement
            seen = set()
            unique_influencers = []
            for inf in influencers:
                if inf['username'] not in seen:
                    seen.add(inf['username'])
                    unique_influencers.append(inf)
            
            unique_influencers.sort(key=lambda x: x['engagement'], reverse=True)
            
            print(f"Found {len(unique_influencers)} influencers")
            return unique_influencers[:10]
            
        except Exception as e:
            print(f"Error finding influencers: {e}")
            return []
    
    async def analyze_influencer_content(self, username: str) -> Dict[str, Any]:
        """Analyze an influencer's content strategy."""
        
        if not self.apify_token:
            return {}
        
        try:
            run_input = {
                "username": [username],
                "resultsLimit": 15
            }
            
            run = self.client.actor("apify/instagram-profile-scraper").call(run_input=run_input)
            
            posts = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                if item.get('latestPosts'):
                    posts = item['latestPosts'][:15]
                    break
            
            # Extract patterns
            from .content_analyzer import ContentAnalyzer
            analyzer = ContentAnalyzer()
            patterns = await analyzer.find_winning_patterns(posts)
            
            return {
                'username': username,
                'post_count': len(posts),
                'winning_formula': patterns
            }
            
        except Exception as e:
            print(f"Error analyzing influencer: {e}")
            return {}
