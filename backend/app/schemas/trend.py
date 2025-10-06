from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class TrendBase(BaseModel):
    client_id: int
    keyword: str
    platform: str
    volume: int = 0
    growth: Optional[str] = None
    relevance: str = "Medium"
    avg_likes: float = 0.0
    avg_comments: float = 0.0
    avg_engagement: float = 0.0
    sample_posts: List[Dict[str, Any]] = []
    description: Optional[str] = None

class TrendCreate(TrendBase):
    pass

class TrendResponse(TrendBase):
    id: int
    discovered_at: datetime
    
    class Config:
        from_attributes = True

class TrendScanRequest(BaseModel):
    client_id: int
    keywords: List[str]
    platforms: List[str] = ["instagram", "facebook"]
