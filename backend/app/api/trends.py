from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..models.trend import Trend
from ..models.client import Client
from ..agents.apify_scanner import ApifyScanner
from ..agents.content_analyzer import ContentAnalyzer
import logging
import re
import json

logger = logging.getLogger(__name__)

router = APIRouter()

def clean_caption(caption: str) -> str:
    """
    Clean and decode caption to handle Turkish characters properly.
    Instagram API sometimes returns mangled UTF-8 encoding.
    """
    if not caption:
        return ""
    
    try:
        # Try to fix double-encoded UTF-8 (common Instagram API issue)
        # Example: "GÃ¼zel" should be "Güzel"
        cleaned = caption.encode('latin1').decode('utf-8')
        return cleaned[:500]  # Limit length for database
    except (UnicodeDecodeError, UnicodeEncodeError):
        try:
            # Fallback: ensure valid UTF-8
            return caption.encode('utf-8', errors='ignore').decode('utf-8')[:500]
        except:
            # Last resort: remove problematic characters
            return ''.join(char for char in caption if ord(char) < 128)[:500]

def extract_hashtags(caption: str) -> str:
    """
    Extract hashtags from caption and return as comma-separated string.
    Used for the keywords field.
    """
    if not caption:
        return ""
    
    # Find all hashtags (words starting with #)
    hashtags = re.findall(r'#(\w+)', caption)
    
    # Remove duplicates and limit to 10
    unique_hashtags = list(dict.fromkeys(hashtags))[:10]
    
    return ','.join(unique_hashtags)

@router.post("/scan")
async def scan_trends(
    client_id: int,
    deep_analysis: bool = False,
    db: Session = Depends(get_db)
):
    """
    Scan Instagram trends for a client using niche hashtags.
    Handles Turkish characters properly and extracts metadata.
    
    Parameters:
    - client_id: The client to scan for
    - deep_analysis: If True, performs content pattern analysis (default: False)
    """
    try:
        # Verify client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        
        scan_type = "deep scan" if deep_analysis else "scan"
        logger.info(f"🔍 Starting {scan_type} for client: {client.name}")
        
        # Initialize scanner and scan
        scanner = ApifyScanner()
        posts = await scanner.scan_instagram_for_client(client_id, db)
        
        if not posts:
            logger.warning(f"No posts found for {client.name}")
            return {
                "message": "No posts found. Try different hashtags or check API quota.",
                "count": 0,
                "client_id": client_id,
                "client_name": client.name,
                "winning_patterns": None if deep_analysis else None
            }
        
        # Perform deep analysis if requested
        winning_patterns = None
        if deep_analysis:
            try:
                analyzer = ContentAnalyzer()
                winning_patterns = await analyzer.find_winning_patterns(posts)
                
                if winning_patterns:
                    client.winning_patterns = json.dumps(winning_patterns)
                    logger.info(f"✅ Winning patterns analyzed for {client.name}")
            except Exception as e:
                logger.error(f"Error analyzing patterns: {e}")
                # Continue with normal scan even if analysis fails
        
        # Process and save trends
        saved_count = 0
        for post in posts:
            try:
                # Get caption and clean it for Turkish characters
                raw_caption = post.get('caption', '')
                cleaned_caption = clean_caption(raw_caption)
                
                # Extract hashtags for keywords
                keywords = extract_hashtags(cleaned_caption)
                
                # Get main hashtag from post metadata
                main_hashtag = post.get('hashtag', 'unknown')
                
                # Create short title (first 100 chars of caption)
                title = cleaned_caption[:100] if cleaned_caption else f"Post from #{main_hashtag}"
                
                # Calculate engagement (likes + comments)
                likes = post.get('likesCount', 0)
                comments = post.get('commentsCount', 0)
                engagement = likes + (comments * 2)  # Weight comments more
                
                # Create trend object
                trend = Trend(
                    client_id=client_id,
                    platform="instagram",
                    hashtag=main_hashtag,
                    title=title,
                    content=cleaned_caption,  # Full caption with proper encoding
                    volume=engagement,  # Total engagement score
                    engagement_rate=float(comments) if comments > 0 else 0.0,
                    url=post.get('url', ''),
                    keywords=keywords,  # Extracted hashtags
                    discovered_at=datetime.now()
                )
                
                db.add(trend)
                saved_count += 1
                
            except Exception as e:
                logger.error(f"Error processing post: {e}")
                continue
        
        # Commit all changes at once
        db.commit()
        
        logger.info(f"✅ Saved {saved_count}/{len(posts)} trends for {client.name}")
        
        response = {
            "message": f"Successfully scanned and saved {saved_count} posts",
            "count": saved_count,
            "total_posts": len(posts),
            "client_id": client_id,
            "client_name": client.name
        }
        
        if deep_analysis:
            response["winning_patterns"] = winning_patterns
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error scanning trends: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@router.get("/")
def get_trends(
    client_id: Optional[int] = None,
    platform: Optional[str] = None,
    hashtag: Optional[str] = None,
    min_engagement: Optional[int] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get all trends with optional filters.
    
    Query parameters:
    - client_id: Filter by client
    - platform: Filter by platform (e.g., 'instagram')
    - hashtag: Filter by hashtag
    - min_engagement: Filter by minimum engagement score
    - limit: Maximum results (default 50)
    """
    try:
        query = db.query(Trend)
        
        # Apply filters
        if client_id:
            query = query.filter(Trend.client_id == client_id)
        
        if platform:
            query = query.filter(Trend.platform == platform.lower())
        
        if hashtag:
            query = query.filter(Trend.hashtag.ilike(f"%{hashtag}%"))
        
        if min_engagement:
            query = query.filter(Trend.volume >= min_engagement)
        
        # Order by most recent and limit
        trends = query.order_by(Trend.discovered_at.desc()).limit(limit).all()
        
        logger.info(f"Retrieved {len(trends)} trends")
        
        # Return properly formatted response
        return [
            {
                "id": t.id,
                "client_id": t.client_id,
                "platform": t.platform,
                "hashtag": t.hashtag,
                "title": t.title,
                "content": t.content,  # Properly encoded Turkish text
                "volume": t.volume,
                "engagement_rate": t.engagement_rate,
                "url": t.url,
                "keywords": t.keywords,
                "created_at": t.discovered_at.isoformat() if t.discovered_at else None
            }
            for t in trends
        ]
        
    except Exception as e:
        logger.error(f"Error fetching trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_trend_stats(
    client_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Get statistics about trends.
    
    Returns:
    - Total trends
    - Average engagement
    - Top hashtags
    - Platform breakdown
    """
    try:
        query = db.query(Trend)
        
        if client_id:
            query = query.filter(Trend.client_id == client_id)
        
        trends = query.all()
        
        if not trends:
            return {
                "total": 0,
                "average_engagement": 0,
                "top_hashtags": [],
                "platforms": {}
            }
        
        # Calculate stats
        total = len(trends)
        total_engagement = sum(t.volume or 0 for t in trends)
        avg_engagement = total_engagement / total if total > 0 else 0
        
        # Top hashtags
        hashtag_counts = {}
        for t in trends:
            if t.hashtag:
                hashtag_counts[t.hashtag] = hashtag_counts.get(t.hashtag, 0) + 1
        
        top_hashtags = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Platform breakdown
        platform_counts = {}
        for t in trends:
            platform = t.platform or 'unknown'
            platform_counts[platform] = platform_counts.get(platform, 0) + 1
        
        return {
            "total": total,
            "average_engagement": round(avg_engagement, 2),
            "top_hashtags": [{"hashtag": h[0], "count": h[1]} for h in top_hashtags],
            "platforms": platform_counts
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{trend_id}")
def delete_trend(
    trend_id: int,
    db: Session = Depends(get_db)
):
    """Delete a specific trend by ID."""
    try:
        trend = db.query(Trend).filter(Trend.id == trend_id).first()
        
        if not trend:
            raise HTTPException(status_code=404, detail=f"Trend {trend_id} not found")
        
        db.delete(trend)
        db.commit()
        
        logger.info(f"Deleted trend {trend_id}")
        
        return {"message": f"Trend {trend_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting trend: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/")
def delete_all_trends(
    client_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Delete all trends, optionally filtered by client.
    ⚠️ Use with caution!
    """
    try:
        query = db.query(Trend)
        
        if client_id:
            query = query.filter(Trend.client_id == client_id)
        
        count = query.count()
        query.delete()
        db.commit()
        
        logger.warning(f"Deleted {count} trends" + (f" for client {client_id}" if client_id else ""))
        
        return {
            "message": f"Deleted {count} trends",
            "count": count
        }
        
    except Exception as e:
        logger.error(f"Error bulk deleting trends: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/scan-deep")
async def scan_trends_deep(
    client_id: int,
    db: Session = Depends(get_db)
):
    """Deep scan with content structure analysis."""
    
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    
    logger.info(f"🔍 Deep scanning for {client.name}")
    
    try:
        # 1. Scan Instagram posts
        scanner = ApifyScanner()
        posts = await scanner.scan_instagram_for_client(client_id, db)
        
        if not posts:
            return {
                "message": "No posts found",
                "posts_found": 0,
                "client_id": client_id
            }
        
        # 2. Analyze content patterns
        from ..agents.content_analyzer import ContentAnalyzer
        analyzer = ContentAnalyzer()
        winning_patterns = await analyzer.find_winning_patterns(posts)
        
        # 3. Store winning patterns in client
        if winning_patterns:
            import json
            client.winning_patterns = json.dumps(winning_patterns)
            db.commit()
            logger.info(f"✅ Winning patterns saved for {client.name}")
        
        return {
            "success": True,
            "message": f"Deep scan complete for {client.name}",
            "posts_found": len(posts),
            "winning_patterns": winning_patterns,
            "client_id": client_id,
            "client_name": client.name
        }
        
    except Exception as e:
        logger.error(f"Error in deep scan: {e}")
        raise HTTPException(status_code=500, detail=str(e))
