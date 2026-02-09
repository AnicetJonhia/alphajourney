"""Service de génération et gestion du contenu."""

import logging
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Post
from app.data.schedules import WEEKLY_SCHEDULE, TOPICS
from app.data.prompts import get_prompt
from app.services.llm_service import get_llm_service

logger = logging.getLogger(__name__)


class ContentService:
    """Logique métier pour la génération de contenu."""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = get_llm_service()
    
    def get_today_category(self) -> str:
        """Retourne la catégorie à publier aujourd'hui."""
        day_of_week = datetime.now().weekday()
        return WEEKLY_SCHEDULE[day_of_week]
    
    def get_unused_topic(self, category: str, days: int = 30) -> str:
        """
        Récupère un sujet non utilisé récemment.
        
        Args:
            category: Catégorie de contenu
            days: Nombre de jours à vérifier pour éviter répétitions
            
        Returns:
            str: Sujet sélectionné
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Récupérer les sujets récents
        recent_posts = self.db.query(Post.topic).filter(
            Post.category == category,
            Post.created_at >= cutoff_date
        ).all()
        
        used_topics = {post.topic for post in recent_posts}
        
        # Filtrer les sujets disponibles
        available_topics = [
            topic for topic in TOPICS[category]
            if topic not in used_topics
        ]
        
        # Si tous utilisés, reset
        if not available_topics:
            logger.warning(f"⚠️ Tous les sujets {category} utilisés, reset")
            available_topics = TOPICS[category]
        
        selected = random.choice(available_topics)
        logger.info(f"📝 Sujet sélectionné : {selected}")
        
        return selected
    
    def generate_post_content(self, category: str, topic: str) -> tuple[str, str]:
        """
        Génère le contenu d'un post.
        
        Args:
            category: Catégorie du post
            topic: Sujet du post
            
        Returns:
            tuple: (contenu, nom du LLM utilisé)
        """
        prompt = get_prompt(category, topic)
        
        logger.info(f"🤖 Génération contenu pour : {topic}")
        content, llm_name = self.llm_service.generate(prompt)
        
        return content, llm_name
    
    def save_post(
        self,
        category: str,
        topic: str,
        content: str,
        fb_post_id: str,
        llm_used: str
    ) -> Post:
        """
        Sauvegarde un post en base de données.
        
        Returns:
            Post: Instance du post créé
        """
        post = Post(
            category=category,
            topic=topic,
            content=content,
            fb_post_id=fb_post_id,
            llm_used=llm_used,
            published_at=datetime.utcnow()
        )
        
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        
        logger.info(f"💾 Post sauvegardé : ID {post.id}")
        return post
    
    def update_post_analytics(self, post_id: int, stats: dict) -> None:
        """Met à jour les statistiques d'un post."""
        post = self.db.query(Post).filter(Post.id == post_id).first()
        
        if post:
            post.likes = stats.get("likes", 0)
            post.shares = stats.get("shares", 0)
            post.comments = stats.get("comments", 0)
            post.reach = stats.get("reach", 0)
            
            # Score d'engagement pondéré
            post.engagement_score = (
                stats.get("likes", 0) +
                stats.get("shares", 0) * 2 +
                stats.get("comments", 0) * 3
            )
            
            self.db.commit()
            logger.info(f"📊 Stats mises à jour pour post {post_id}")