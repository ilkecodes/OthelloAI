"""Platform ve Content Type Specifications"""

PLATFORM_CONTENT_TYPES = {
    "instagram": {
        "post": {
            "name": "Instagram Post",
            "max_chars": 2200,
            "critical_chars": 125,
            "hashtag_limit": "20-30",
            "emoji_usage": "high"
        },
        "carousel": {
            "name": "Instagram Carousel",
            "max_chars": 2200,
            "slides": 5,
            "hashtag_limit": "20-30",
            "emoji_usage": "high"
        },
        "reel": {
            "name": "Instagram Reel",
            "max_chars": 2200,
            "video_length": "15-90 saniye",
            "hashtag_limit": "20-30",
            "emoji_usage": "very_high"
        }
    },
    "linkedin": {
        "post": {
            "name": "LinkedIn Post",
            "max_chars": 3000,
            "hashtag_limit": "3-5",
            "emoji_usage": "low"
        },
        "carousel": {
            "name": "LinkedIn Carousel",
            "max_chars": 3000,
            "slides": 5,
            "hashtag_limit": "3-5",
            "emoji_usage": "medium"
        }
    },
    "twitter": {
        "tweet": {
            "name": "Tweet",
            "max_chars": 280,
            "hashtag_limit": "1-2"
        },
        "thread": {
            "name": "Thread",
            "max_chars": 280,
            "tweets": 5,
            "hashtag_limit": "1-2"
        }
    }
}

def get_platform_spec(platform: str, content_type: str):
    if platform not in PLATFORM_CONTENT_TYPES:
        return None
    return PLATFORM_CONTENT_TYPES[platform].get(content_type)
