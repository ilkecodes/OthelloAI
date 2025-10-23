
async def scan_instagram_profile(self, username: str, max_posts: int = 15) -> List[Dict[str, Any]]:
    """Instagram profilinden son postları çek"""
    
    if not self.apify_token:
        print(f"⚠️  No Apify token, returning mock data for @{username}")
        return self._generate_mock_posts(username, max_posts)
    
    try:
        print(f"📸 Scanning Instagram profile: @{username}")
        
        run_input = {
            "usernames": [username],
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
        print(f"❌ Error scanning Instagram profile: {e}")
        return self._generate_mock_posts(username, max_posts)

def _generate_mock_posts(self, username: str, count: int) -> List[Dict[str, Any]]:
    """Mock Instagram posts for testing"""
    import random
    from datetime import datetime, timedelta
    
    mock_captions = [
        "Yeni koleksiyonumuz çıktı! 🎉 Tarzınızı yansıtın #fashion #style",
        "Bugün harika bir gün! ☀️ Sizin için en iyisini sunuyoruz",
        "Detaylar fark yaratır ✨ #quality #brand",
        "Yaz sezonuna hazır mısınız? 🌞 #summer #collection",
        "Her gün yeni bir hikaye 📖 #brand #story"
    ]
    
    posts = []
    for i in range(min(count, 10)):
        posts.append({
            'caption': random.choice(mock_captions),
            'likesCount': random.randint(100, 1000),
            'commentsCount': random.randint(5, 50),
            'url': f'https://instagram.com/p/mock_{i}',
            'timestamp': (datetime.now() - timedelta(days=i)).isoformat()
        })
    
    return posts
