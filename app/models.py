"""Modèles SQLAlchemy pour la base de données."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime
from app.database import Base


class Post(Base):
    """Historique des posts publiés."""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True)
    topic = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    fb_post_id = Column(String(100), unique=True)
    llm_used = Column(String(50))
    image_url = Column(Text, nullable=True)  
    
    # Analytics
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    engagement_score = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    published_at = Column(DateTime)
    
    def __repr__(self):
        return f"<Post {self.id}: {self.category} - {self.topic[:30]}>"