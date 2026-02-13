"""Service de génération de contenu avec hashtags et images."""

import logging
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Post
from app.data.schedules import WEEKLY_SCHEDULE, TOPICS
from app.data.prompts import get_prompt
from app.data.hashtags import get_hashtags, format_hashtags
from app.services.llm_service import get_llm_service
from app.services.image_service import get_image_service

logger = logging.getLogger(__name__)


class ContentService:
    """Logique métier pour la génération de contenu."""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = get_llm_service()
        self.image_service = get_image_service()
    
    def get_today_category(self) -> str:
        """Retourne la catégorie à publier aujourd'hui."""
        day_of_week = datetime.now().weekday()
        return WEEKLY_SCHEDULE[day_of_week]
    
    def get_unused_topic(self, category: str, days: int = 30) -> str:
        """Récupère un sujet non utilisé récemment."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        recent_posts = self.db.query(Post.topic).filter(
            Post.category == category,
            Post.created_at >= cutoff_date
        ).all()
        
        used_topics = {post.topic for post in recent_posts}
        
        available_topics = [
            topic for topic in TOPICS[category]
            if topic not in used_topics
        ]
        
        if not available_topics:
            logger.warning(f"⚠️ Tous les sujets {category} utilisés, reset")
            available_topics = TOPICS[category]
        
        selected = random.choice(available_topics)
        logger.info(f"📝 Sujet sélectionné : {selected}")
        
        return selected
    
    async def generate_post_content(
        self,
        category: str,
        topic: str,
        timeout: float = 45.0
    ) -> tuple[str, str]:
        """Génère le contenu d'un post avec hashtags."""
        prompt = get_prompt(category, topic)
        
        logger.info(f"🤖 Génération contenu pour : {topic}")
        
        # Générer le contenu principal
        content, llm_name = await self.llm_service.generate(prompt, timeout)
        
        # Ajouter les hashtags
        hashtags = get_hashtags(category, count=5)
        hashtags_str = format_hashtags(hashtags)
        
        # Combiner contenu + hashtags
        full_content = content + hashtags_str
        
        logger.info(f"✅ Contenu généré avec hashtags : {hashtags}")
        
        return full_content, llm_name
    
    async def get_post_image(
        self,
        category: str,
        timeout: float = 15.0
    ) -> str | None:
        """Récupère une image pour le post."""
        logger.info(f"📸 Recherche d'image pour : {category}")
        
        image_url = await self.image_service.get_image_url(category, timeout)
        
        if image_url:
            logger.info(f"✅ Image trouvée : {image_url[:50]}...")
        else:
            logger.warning("⚠️ Pas d'image - publication en texte seul")
        
        return image_url
    
    def save_post(
        self,
        category: str,
        topic: str,
        content: str,
        fb_post_id: str,
        llm_used: str,
        image_url: str | None = None
    ) -> Post:
        """Sauvegarde un post en base."""
        post = Post(
            category=category,
            topic=topic,
            content=content,
            fb_post_id=fb_post_id,
            llm_used=llm_used,
            image_url=image_url,  # Nouveau champ
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
            
            post.engagement_score = (
                stats.get("likes", 0) +
                stats.get("shares", 0) * 2 +
                stats.get("comments", 0) * 3
            )
            
            self.db.commit()
            logger.info(f"📊 Stats mises à jour pour post {post_id}")