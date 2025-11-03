from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class BrandEmbedding(Base):
    __tablename__ = "brand_embeddings"
    
    id = Column(String, primary_key=True)  # INTEGER → String
    client_id = Column(String, ForeignKey("clients.id"), nullable=False, index=True)
    corpus_id = Column(String, nullable=True)  # INTEGER → String
    text = Column(Text, nullable=False)
    source = Column(String(50))
    embedding = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
