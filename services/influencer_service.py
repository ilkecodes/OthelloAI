from apify_client import ApifyClient
from config import settings
from typing import List, Dict

class InfluencerDiscovery:
    def __init__(self):
        self.client = ApifyClient(settings.APIFY_API_TOKEN)
    
    def search_by_hashtag(self, hashtags: List[str], limit: int = 50):
        influencers = []
        for hashtag in hashtags:
            run = self.client.actor("apify/instagram-hashtag-scraper").call(
                run_input={"hashtags": [hashtag], "resultsLimit": limit}
            )
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                owner = item.get("ownerUsername")
                if owner and owner not in [i["username"] for i in influencers]:
                    influencers.append({"username": owner, "source_hashtag": hashtag})
        return influencers
    
    def analyze_profile(self, username: str):
        run = self.client.actor("apify/instagram-profile-scraper").call(
            run_input={"usernames": [username], "resultsLimit": 1}
        )
        data = list(self.client.dataset(run["defaultDatasetId"]).iterate_items())
        if not data:
            return None
        profile = data[0]
        followers = profile.get("followersCount", 0)
        return {
            "username": username,
            "followers": followers,
            "engagement_rate": 3.5,
            "biography": profile.get("biography")
        }

influencer_discovery = InfluencerDiscovery()
