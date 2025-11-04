"""Authenticity & Bot Detection"""
from typing import Dict, List

def check_authenticity(profile: Dict) -> Dict:
    """Sahte follower ve bot tespiti"""
    
    red_flags = []
    warnings = []
    score = 100  # Start at 100, deduct for issues
    
    followers = profile.get("followers", 0)
    following = profile.get("following", 0)
    posts_count = profile.get("posts_count", 0)
    engagement_rate = profile.get("engagement_rate", 0)
    avg_likes = profile.get("avg_likes", 0)
    avg_comments = profile.get("avg_comments", 0)
    
    # 1. Follower/Following Ratio
    if following > 0:
        ratio = followers / following
        if ratio < 0.1:  # Following çok fazla
            red_flags.append("Following too many accounts (possible follow-for-follow)")
            score -= 20
        elif ratio < 0.5:
            warnings.append("High following count")
            score -= 10
    
    # 2. Posts vs Followers
    if followers > 1000:
        posts_per_1k = (posts_count / followers) * 1000
        if posts_per_1k < 5:  # Çok az post, çok takipçi
            warnings.append("Low post count for follower size")
            score -= 10
    
    # 3. Engagement Rate
    if followers > 5000:
        if engagement_rate < 0.5:
            red_flags.append("Very low engagement rate (possible fake followers)")
            score -= 30
        elif engagement_rate < 1.0:
            warnings.append("Below average engagement")
            score -= 15
    
    # 4. Comments/Likes Ratio
    if avg_likes > 0:
        comment_ratio = avg_comments / avg_likes
        if comment_ratio < 0.005:  # Çok az yorum
            red_flags.append("Suspiciously low comments (bot followers?)")
            score -= 25
        elif comment_ratio > 0.1:  # Çok fazla yorum
            warnings.append("Unusually high comment rate")
            score -= 10
    
    # 5. Zero Engagement
    if engagement_rate == 0:
        red_flags.append("No engagement detected")
        score -= 50
    
    # Final score
    score = max(0, score)
    
    # Status
    if score >= 80:
        status = "✅ Authentic"
        status_color = "green"
    elif score >= 60:
        status = "⚠️ Mostly Authentic"
        status_color = "yellow"
    elif score >= 40:
        status = "🤔 Questionable"
        status_color = "orange"
    else:
        status = "🚫 Suspicious"
        status_color = "red"
    
    return {
        "authenticity_score": score,
        "status": status,
        "status_color": status_color,
        "red_flags": red_flags,
        "warnings": warnings,
        "is_authentic": score >= 60
    }

def detect_engagement_pods(latest_posts: List[Dict]) -> Dict:
    """Engagement pod tespiti (aynı kişiler sürekli yorum yapıyor mu?)"""
    
    # Bu özellik için post detaylarında commenter bilgisi gerekir
    # Şimdilik basit bir check
    
    if not latest_posts or len(latest_posts) < 5:
        return {"pod_detected": False, "confidence": 0}
    
    # Engagement tutarlılığına bak
    engagement_values = []
    for post in latest_posts[:10]:
        likes = post.get("likes", 0)
        comments = post.get("comments", 0)
        if likes > 0:
            engagement_values.append(comments / likes)
    
    if len(engagement_values) < 3:
        return {"pod_detected": False, "confidence": 0}
    
    # Çok tutarlı ise (aynı kişiler engage ediyor olabilir)
    avg_ratio = sum(engagement_values) / len(engagement_values)
    variance = sum((x - avg_ratio) ** 2 for x in engagement_values) / len(engagement_values)
    
    # Düşük varyans = sürekli aynı pattern = pod olabilir
    if variance < 0.0001 and avg_ratio > 0.05:
        return {
            "pod_detected": True,
            "confidence": 70,
            "note": "Suspiciously consistent engagement pattern"
        }
    
    return {"pod_detected": False, "confidence": 0}
