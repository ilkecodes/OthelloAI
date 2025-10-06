from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Trend(Base):
    __tablename__ = "trends"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    platform = Column(String(50))
    hashtag = Column(String(100))
    title = Column(String(500))
    content = Column(Text)
    volume = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)
    url = Column(String(500))
    keywords = Column(Text)  # ✅ BU SATIRI EKLE
    discovered_at = Column(DateTime, default=datetime.now)
    
    # Relationship
    client = relationship("Client", back_populates="trends")
