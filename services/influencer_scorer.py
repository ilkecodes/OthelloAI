"""Influencer Scoring System"""

def calculate_niche_score(profile: dict, strategy: dict) -> dict:
    """Profil için niş uygunluk skoru hesapla"""
    
    score_breakdown = {
        "niche_match": 0,      # 40 points
        "location_match": 0,   # 10 points
        "engagement": 0,       # 30 points
        "authenticity": 0,     # 10 points
        "follower_range": 0    # 10 points
    }
    
    bio = (profile.get("biography") or "").lower()
    location_info = (profile.get("external_url") or "") + " " + bio
    
    # 1. Niş Match (0-40)
    bio_keywords = strategy.get("bio_keywords", [])
    if bio_keywords:
        matched_keywords = sum(1 for kw in bio_keywords if kw in bio)
        score_breakdown["niche_match"] = min(40, (matched_keywords / len(bio_keywords)) * 40)
    
    # 2. Location Match (0-10)
    location_keywords = strategy.get("location_keywords", [])
    if location_keywords:
        if any(loc in location_info.lower() for loc in location_keywords):
            score_breakdown["location_match"] = 10
    else:
        score_breakdown["location_match"] = 5  # Lokasyon belirtilmemişse nötr
    
    # 3. Engagement Quality (0-30)
    engagement_rate = profile.get("engagement_rate", 0)
    ideal_engagement = strategy.get("ideal_engagement", 0.02)
    
    if engagement_rate >= ideal_engagement:
        score_breakdown["engagement"] = 30
    elif engagement_rate >= ideal_engagement * 0.5:
        score_breakdown["engagement"] = 20
    elif engagement_rate >= ideal_engagement * 0.25:
        score_breakdown["engagement"] = 10
    
    # 4. Authenticity (comments/likes ratio) (0-10)
    avg_likes = profile.get("avg_likes", 0)
    avg_comments = profile.get("avg_comments", 0)
    
    if avg_likes > 0:
        comment_ratio = avg_comments / avg_likes
        if 0.01 <= comment_ratio <= 0.1:  # Sağlıklı oran
            score_breakdown["authenticity"] = 10
        elif 0.005 <= comment_ratio <= 0.15:
            score_breakdown["authenticity"] = 5
    
    # 5. Follower Range (0-10)
    followers = profile.get("followers", 0)
    min_followers = strategy.get("min_followers", 1000)
    
    if followers >= min_followers * 10:  # 10x ideal
        score_breakdown["follower_range"] = 10
    elif followers >= min_followers * 5:
        score_breakdown["follower_range"] = 8
    elif followers >= min_followers * 2:
        score_breakdown["follower_range"] = 6
    elif followers >= min_followers:
        score_breakdown["follower_range"] = 4
    
    # Toplam skor
    total_score = sum(score_breakdown.values())
    
    # Neden uygun açıklaması
    reasons = []
    if score_breakdown["niche_match"] > 20:
        matched = [kw for kw in bio_keywords if kw in bio]
        reasons.append(f"Bio contains: {', '.join(matched[:3])}")
    
    if score_breakdown["location_match"] == 10:
        reasons.append(f"Location match: {location_keywords[0]}")
    
    if score_breakdown["engagement"] >= 20:
        reasons.append(f"High engagement: {engagement_rate:.2%}")
    
    if score_breakdown["authenticity"] >= 5:
        reasons.append("Authentic engagement")
    
    return {
        "total_score": round(total_score, 1),
        "breakdown": score_breakdown,
        "reasons": reasons,
        "badge": get_score_badge(total_score)
    }

def get_score_badge(score: float) -> str:
    """Skor rozetini döndür"""
    if score >= 80:
        return "🏆 Perfect Match"
    elif score >= 60:
        return "⭐ Great Match"
    elif score >= 40:
        return "✓ Good Match"
    else:
        return "○ Fair Match"
