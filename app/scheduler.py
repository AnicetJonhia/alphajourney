"""Planificateur avec auto-engagement (like + comment)."""

import logging
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import SessionLocal
from app.services.content_service import ContentService
from app.services.facebook_service import get_facebook_service
from app.data.comments import get_first_comment
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


async def daily_publication_job():
    """Job de publication quotidienne avec auto-engagement."""
    logger.info("🚀 Démarrage du job de publication")
    
    db = SessionLocal()
    
    try:
        content_service = ContentService(db)
        fb_service = get_facebook_service()
        
        # 1. Catégorie du jour
        category = content_service.get_today_category()
        logger.info(f"📅 Catégorie : {category}")
        
        # 2. Sujet
        topic = content_service.get_unused_topic(category)
        
        # 3. Générer contenu + hashtags
        content, llm_used = await content_service.generate_post_content(
            category, topic, timeout=60.0
        )
        
        # 4. Récupérer image
        image_url = await content_service.get_post_image(
            category, timeout=15.0
        )
        
        # 5. Publier sur Facebook
        fb_post_id = await fb_service.publish(
            content=content,
            image_url=image_url,
            timeout=30.0
        )
        
        # Dans daily_publication_job(), remplacer la section 6 par :

        # 6. AUTO-ENGAGEMENT (configurable)
        if settings.auto_like or settings.auto_comment:
            logger.info("🎯 Démarrage auto-engagement...")
            
            # Attendre le délai configuré
            await asyncio.sleep(settings.engagement_delay)
            
            # Like si activé
            if settings.auto_like:
                like_success = await fb_service.like_post(fb_post_id, timeout=10.0)
                if like_success:
                    logger.info("👍 Post liké automatiquement")
            
            # Commentaire si activé
            if settings.auto_comment:
                first_comment = get_first_comment(category)
                comment_id = await fb_service.comment_post(
                    fb_post_id,
                    first_comment,
                    timeout=10.0
                )
                if comment_id:
                    logger.info(f"💬 Premier commentaire publié : {comment_id}")
        
        # 7. Sauvegarder
        post = content_service.save_post(
            category=category,
            topic=topic,
            content=content,
            fb_post_id=fb_post_id,
            llm_used=llm_used,
            image_url=image_url
        )
        
        logger.info(
            f"✅ Publication complète ! "
            f"Post ID: {post.id}, FB: {fb_post_id}, "
            f"LLM: {llm_used}, Image: {'✅' if image_url else '❌'}, "
            f"Like: {'✅' if like_success else '❌'}, "
            f"Comment: {'✅' if comment_id else '❌'}"
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur : {e}", exc_info=True)
        
    finally:
        db.close()


async def fetch_analytics_job():
    """Récupère les analytics."""
    logger.info("📊 Récupération analytics")
    
    db = SessionLocal()
    
    try:
        from app.models import Post
        
        yesterday = datetime.utcnow() - timedelta(days=1)
        start = yesterday - timedelta(hours=1)
        end = yesterday + timedelta(hours=1)
        
        posts = db.query(Post).filter(
            Post.published_at >= start,
            Post.published_at <= end,
            Post.fb_post_id.isnot(None)
        ).all()
        
        fb_service = get_facebook_service()
        content_service = ContentService(db)
        
        tasks = [
            fb_service.get_post_insights(p.fb_post_id, timeout=30.0)
            for p in posts
        ]
        
        stats_list = await asyncio.gather(*tasks, return_exceptions=True)
        
        for post, stats in zip(posts, stats_list):
            if isinstance(stats, Exception):
                logger.error(f"❌ Stats post {post.id} : {stats}")
            else:
                content_service.update_post_analytics(post.id, stats)
        
        logger.info(f"✅ Analytics pour {len(posts)} posts")
        
    except Exception as e:
        logger.error(f"❌ Erreur analytics : {e}")
        
    finally:
        db.close()


scheduler = AsyncIOScheduler()


def start_scheduler():
    """Démarre le planificateur."""
    
    scheduler.add_job(
        daily_publication_job,
        trigger='cron',
        hour=settings.publication_hour,
        minute=settings.publication_minute,
        id='daily_publication',
        replace_existing=True
    )
    
    scheduler.add_job(
        fetch_analytics_job,
        trigger='cron',
        hour=18,
        minute=0,
        id='fetch_analytics',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("⏰ Scheduler démarré (Auto-engagement activé)")


def stop_scheduler():
    """Arrête le planificateur."""
    scheduler.shutdown()
    logger.info("⏹️ Scheduler arrêté")