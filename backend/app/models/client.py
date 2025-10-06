from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    industry = Column(String(100))
    keywords = Column(String(500))
    instagram_url = Column(String(200))  # ✅ YENİ
    instagram_username = Column(String(100))  # ✅ YENİ
    brand_voice = Column(Text)  # ✅ YENİ - AI tarafından analiz edilecek
    created_at = Column(DateTime, default=datetime.now)
    winning_patterns = Column(Text)  # JSON string
    trends = relationship("Trend", back_populates="client")
