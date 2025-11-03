"""Niche Definitions & Strategies"""

NICHE_DEFINITIONS = {
    "fitness_wellness": {
        "name": "Fitness & Wellness",
        "icon": "💪",
        "description": "Fitness trainers, yoga instructors, wellness coaches",
        "bio_keywords": [
            "fitness", "trainer", "coach", "gym", "workout", "personal trainer",
            "yoga", "pilates", "wellness", "health", "antrenör", "spor", "sağlık"
        ],
        "search_templates": [
            "fitness trainer OR personal coach",
            "yoga instructor OR pilates coach",
            "wellness coach OR health influencer"
        ],
        "min_followers": 5000,
        "ideal_engagement": 0.02
    },
    "beauty_skincare": {
        "name": "Beauty & Skincare",
        "icon": "💄",
        "description": "Makeup artists, beauty influencers, skincare experts",
        "bio_keywords": [
            "makeup", "beauty", "mua", "skincare", "cosmetics", "dermatologist",
            "makyaj", "güzellik", "cilt bakımı", "beauty blogger", "makeup artist"
        ],
        "search_templates": [
            "makeup artist OR beauty influencer",
            "skincare expert OR beauty blogger",
            "cosmetics OR dermatologist"
        ],
        "min_followers": 3000,
        "ideal_engagement": 0.03
    },
    "food_culinary": {
        "name": "Food & Culinary",
        "icon": "🍕",
        "description": "Food bloggers, chefs, restaurant reviewers",
        "bio_keywords": [
            "food", "chef", "culinary", "recipe", "cooking", "foodie",
            "restaurant", "yemek", "mutfak", "lezzet", "gastronomy", "food blogger"
        ],
        "search_templates": [
            "food blogger OR chef",
            "restaurant reviewer OR foodie",
            "culinary expert OR recipe creator"
        ],
        "min_followers": 5000,
        "ideal_engagement": 0.025
    },
    "tech_ai": {
        "name": "Tech & AI",
        "icon": "🤖",
        "description": "Tech reviewers, AI experts, software developers",
        "bio_keywords": [
            "tech", "ai", "ml", "developer", "software", "engineer",
            "technology", "coding", "programmer", "data scientist", "artificial intelligence"
        ],
        "search_templates": [
            "tech influencer OR ai expert",
            "software developer OR data scientist",
            "tech reviewer OR programmer"
        ],
        "min_followers": 3000,
        "ideal_engagement": 0.015
    },
    "business_finance": {
        "name": "Business & Finance",
        "icon": "💼",
        "description": "Entrepreneurs, business coaches, finance experts",
        "bio_keywords": [
            "entrepreneur", "business", "ceo", "founder", "startup",
            "finance", "investing", "coach", "mentor", "girişimci", "iş"
        ],
        "search_templates": [
            "entrepreneur OR business coach",
            "finance expert OR investor",
            "ceo OR founder"
        ],
        "min_followers": 5000,
        "ideal_engagement": 0.02
    },
    "travel_adventure": {
        "name": "Travel & Adventure",
        "icon": "✈️",
        "description": "Travel bloggers, photographers, adventure seekers",
        "bio_keywords": [
            "travel", "traveler", "wanderlust", "adventure", "explorer",
            "photography", "seyahat", "gezgin", "world traveler", "travel blogger"
        ],
        "search_templates": [
            "travel blogger OR photographer",
            "adventure seeker OR explorer",
            "world traveler OR wanderlust"
        ],
        "min_followers": 5000,
        "ideal_engagement": 0.025
    },
    "lifestyle": {
        "name": "Lifestyle",
        "icon": "🌟",
        "description": "Lifestyle influencers, daily vloggers",
        "bio_keywords": [
            "lifestyle", "life", "blogger", "vlogger", "daily",
            "yaşam", "influencer", "content creator"
        ],
        "search_templates": [
            "lifestyle blogger OR influencer",
            "daily vlogger OR content creator"
        ],
        "min_followers": 5000,
        "ideal_engagement": 0.025
    },
    "custom": {
        "name": "Custom Search",
        "icon": "🔍",
        "description": "Custom keyword search",
        "bio_keywords": [],
        "search_templates": [],
        "min_followers": 1000,
        "ideal_engagement": 0.01
    }
}

def get_niche_config(niche_key: str) -> dict:
    """Get niche configuration"""
    return NICHE_DEFINITIONS.get(niche_key, NICHE_DEFINITIONS["custom"])

def get_all_niches() -> list:
    """Get all available niches"""
    return [
        {"key": key, "name": config["name"], "icon": config["icon"], "description": config["description"]}
        for key, config in NICHE_DEFINITIONS.items()
    ]
