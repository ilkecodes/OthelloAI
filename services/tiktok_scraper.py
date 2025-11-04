"""TikTok Creative Center Scraper"""
from typing import List, Dict

class TikTokCreativeCenterScraper:
    def __init__(self):
        pass
    
    def get_trending_hashtags(self, country: str = "TR", limit: int = 20) -> List[Dict]:
        """TikTok trending hashtags (mock data for now)"""
        
        # Mock data - gerçek TikTok Creative Center verilerine benzer
        all_trends = [
            {"hashtag": "fyp", "views": "125.8B", "posts": 284500000, "growth": "🔥", "category": "genel", "rank": 1},
            {"hashtag": "foryou", "views": "89.2B", "posts": 195600000, "growth": "🔥", "category": "genel", "rank": 2},
            {"hashtag": "viral", "views": "78.4B", "posts": 167800000, "growth": "🔥", "category": "genel", "rank": 3},
            {"hashtag": "keşfet", "views": "45.3B", "posts": 89400000, "growth": "📈", "category": "türkiye", "rank": 4},
            {"hashtag": "tiktok", "views": "42.1B", "posts": 156700000, "growth": "→", "category": "genel", "rank": 5},
            {"hashtag": "food", "views": "38.9B", "posts": 78900000, "growth": "🔥", "category": "food", "rank": 6},
            {"hashtag": "recipe", "views": "35.7B", "posts": 45600000, "growth": "📈", "category": "food", "rank": 7},
            {"hashtag": "yemek", "views": "31.2B", "posts": 67800000, "growth": "🔥", "category": "food", "rank": 8},
            {"hashtag": "tarif", "views": "28.4B", "posts": 34500000, "growth": "📈", "category": "food", "rank": 9},
            {"hashtag": "fashion", "views": "26.8B", "posts": 56700000, "growth": "📈", "category": "fashion", "rank": 10},
            {"hashtag": "moda", "views": "24.3B", "posts": 48900000, "growth": "→", "category": "fashion", "rank": 11},
            {"hashtag": "fitness", "views": "22.7B", "posts": 34500000, "growth": "📈", "category": "fitness", "rank": 12},
            {"hashtag": "workout", "views": "21.1B", "posts": 28900000, "growth": "🔥", "category": "fitness", "rank": 13},
            {"hashtag": "spor", "views": "19.8B", "posts": 23400000, "growth": "📈", "category": "fitness", "rank": 14},
            {"hashtag": "travel", "views": "18.4B", "posts": 41200000, "growth": "📈", "category": "travel", "rank": 15},
            {"hashtag": "seyahat", "views": "17.2B", "posts": 19800000, "growth": "📈", "category": "travel", "rank": 16},
            {"hashtag": "beauty", "views": "16.8B", "posts": 45600000, "growth": "→", "category": "beauty", "rank": 17},
            {"hashtag": "makyaj", "views": "15.9B", "posts": 28900000, "growth": "📈", "category": "beauty", "rank": 18},
            {"hashtag": "dance", "views": "14.7B", "posts": 92300000, "growth": "��", "category": "entertainment", "rank": 19},
            {"hashtag": "music", "views": "13.5B", "posts": 78400000, "growth": "→", "category": "entertainment", "rank": 20},
            {"hashtag": "comedy", "views": "12.8B", "posts": 56700000, "growth": "📈", "category": "entertainment", "rank": 21},
            {"hashtag": "tech", "views": "11.9B", "posts": 23400000, "growth": "🔥", "category": "tech", "rank": 22},
            {"hashtag": "teknoloji", "views": "10.7B", "posts": 12300000, "growth": "📈", "category": "tech", "rank": 23},
            {"hashtag": "motivation", "views": "9.8B", "posts": 32100000, "growth": "📈", "category": "lifestyle", "rank": 24},
            {"hashtag": "motivasyon", "views": "8.9B", "posts": 18900000, "growth": "📈", "category": "lifestyle", "rank": 25},
            {"hashtag": "diy", "views": "8.2B", "posts": 25600000, "growth": "→", "category": "lifestyle", "rank": 26},
            {"hashtag": "home", "views": "7.6B", "posts": 19800000, "growth": "📈", "category": "lifestyle", "rank": 27},
            {"hashtag": "ev", "views": "6.9B", "posts": 11200000, "growth": "→", "category": "lifestyle", "rank": 28},
            {"hashtag": "gaming", "views": "6.3B", "posts": 34200000, "growth": "🔥", "category": "gaming", "rank": 29},
            {"hashtag": "oyun", "views": "5.7B", "posts": 15600000, "growth": "📈", "category": "gaming", "rank": 30}
        ]
        
        return all_trends[:limit]
    
    def get_niche_hashtags(self, niche: str, limit: int = 10) -> List[Dict]:
        """Nişe özel hashtag'ler"""
        
        all_hashtags = self.get_trending_hashtags(limit=50)
        
        # Niş mapping
        niche_map = {
            "food": ["food", "recipe", "yemek", "tarif", "cooking"],
            "fitness": ["fitness", "workout", "spor", "gym", "health"],
            "fashion": ["fashion", "moda", "style", "outfit", "ootd"],
            "beauty": ["beauty", "makyaj", "makeup", "skincare"],
            "travel": ["travel", "seyahat", "vacation", "gezi"],
            "tech": ["tech", "teknoloji", "technology", "ai", "gadget"],
            "business": ["business", "entrepreneur", "startup", "motivasyon", "motivation"],
            "lifestyle": ["lifestyle", "diy", "home", "ev", "life"],
            "entertainment": ["dance", "music", "comedy", "entertainment"],
            "gaming": ["gaming", "oyun", "game"]
        }
        
        keywords = niche_map.get(niche.lower(), [niche])
        
        # Filter
        filtered = [
            h for h in all_hashtags
            if any(k.lower() in h["hashtag"].lower() or k.lower() in h["category"].lower() for k in keywords)
        ]
        
        return filtered[:limit]

# Global instance
tiktok_scraper = TikTokCreativeCenterScraper()
