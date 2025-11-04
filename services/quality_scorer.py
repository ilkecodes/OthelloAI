"""Quality Scoring System"""
from typing import Dict

def calculate_quality_score(profile: Dict, bio_analysis: Dict, content_analysis: Dict) -> Dict:
    """0-100 kalite skoru hesapla"""
    
    scores = {
        "bio_match": 0,        # 30 points
        "content_match": 0,    # 30 points
        "engagement": 0,       # 20 points
        "authenticity": 0,     # 10 points
        "activity": 0          # 10 points
    }
    
    # 1. Bio Match (0-30)
    scores["bio_match"] = min((bio_analysis.get("score", 0) / 100) * 30, 30)
    
    # 2. Content Match (0-30)
    scores["content_match"] = min((content_analysis.get("score", 0) / 100) * 30, 30)
    
    # 3. Engagement Quality (0-20)
    engagement_rate = profile.get("engagement_rate", 0)
    if engagement_rate >= 3.0:
        scores["engagement"] = 20
    elif engagement_rate >= 2.0:
        scores["engagement"] = 15
    elif engagement_rate >= 1.0:
        scores["engagement"] = 10
    elif engagement_rate >= 0.5:
        scores["engagement"] = 5
    
    # 4. Authenticity (Comments/Likes ratio) (0-10)
    avg_likes = profile.get("avg_likes", 0)
    avg_comments = profile.get("avg_comments", 0)
    
    if avg_likes > 0:
        comment_ratio = avg_comments / avg_likes
        if 0.01 <= comment_ratio <= 0.05:  # Healthy ratio
            scores["authenticity"] = 10
        elif 0.005 <= comment_ratio <= 0.08:
            scores["authenticity"] = 7
        elif comment_ratio > 0:
            scores["authenticity"] = 3
    
    # 5. Activity (0-10)
    posts_count = profile.get("posts_count", 0)
    if posts_count >= 100:
        scores["activity"] = 10
    elif posts_count >= 50:
        scores["activity"] = 7
    elif posts_count >= 20:
        scores["activity"] = 5
    elif posts_count >= 10:
        scores["activity"] = 3
    
    # Total score
    total_score = sum(scores.values())
    
    # Quality tier
    if total_score >= 80:
        tier = "🏆 Excellent"
        color = "green"
    elif total_score >= 60:
        tier = "⭐ Great"
        color = "blue"
    elif total_score >= 40:
        tier = "✓ Good"
        color = "orange"
    else:
        tier = "○ Fair"
        color = "gray"
    
    # Reasons
    reasons = []
    
    if scores["bio_match"] >= 20:
        reasons.append(f"Strong bio match ({bio_analysis.get('keywords', [])})")
    
    if scores["content_match"] >= 20:
        consistency = content_analysis.get("consistency", 0)
        reasons.append(f"Consistent content ({consistency}%)")
    
    if scores["engagement"] >= 15:
        reasons.append(f"High engagement ({profile.get('engagement_rate')}%)")
    
    if scores["authenticity"] >= 7:
        reasons.append("Authentic audience")
    
    if scores["activity"] >= 7:
        reasons.append(f"Active account ({posts_count} posts)")
    
    return {
        "total_score": round(total_score, 1),
        "breakdown": scores,
        "tier": tier,
        "color": color,
        "reasons": reasons,
        "badge": get_badge(total_score)
    }

def get_badge(score: float) -> str:
    """Skor rozetini döndür"""
    if score >= 80:
        return "🏆 Perfect Match"
    elif score >= 60:
        return "⭐ Great Match"
    elif score >= 40:
        return "✓ Good Match"
    else:
        return "○ Fair Match"
