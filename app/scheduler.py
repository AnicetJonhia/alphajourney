"""Planificateur de tâches automatiques."""

import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.services.content_service import ContentService
from app.services.facebook_service import get_facebook_service
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def daily_publication_job():
    """Job de publication quotidienne."""
    logger.info("🚀 Démarrage du job de publication quotidienne")
    
    db = SessionLocal()
    
    try:
        # Services
        content_service = ContentService(db)
        fb_service = get_facebook_service()
        
        # 1. Déterminer catégorie du jour
        category = content_service.get_today_category()
        logger.info(f"📅 Catégorie du jour : {category}")
        
        # 2. Sélectionner sujet non répété
        topic = content_service.get_unused_topic(category)
        
        # 3. Générer contenu avec LLM
        content, llm_used = content_service.generate_post_content(category, topic)
        
        # 4. Publier sur Facebook
        fb_post_id = fb_service.publish(content)
        
        # 5. Sauvegarder en base
        post = content_service.save_post(
            category=category,
            topic=topic,
            content=content,
            fb_post_id=fb_post_id,
            llm_used=llm_used
        )
        
        logger.info(f"✅ Publication réussie ! Post ID: {post.id}, FB ID: {fb_post_id}")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la publication : {e}", exc_info=True)
        
    finally:
        db.close()


def fetch_analytics_job():
    """Récupère les analytics des posts publiés il y a 24h."""
    logger.info("📊 Récupération des analytics")
    
    db = SessionLocal()
    
    try:
        # Posts publiés il y a ~24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        start_window = yesterday - timedelta(hours=1)
        end_window = yesterday + timedelta(hours=1)
        
        posts = db.query(Post).filter(
            Post.published_at >= start_window,
            Post.published_at <= end_window,
            Post.fb_post_id.isnot(None)
        ).all()
        
        fb_service = get_facebook_service()
        content_service = ContentService(db)
        
        for post in posts:
            try:
                stats = fb_service.get_post_insights(post.fb_post_id)
                content_service.update_post_analytics(post.id, stats)
            except Exception as e:
                logger.error(f"❌ Erreur stats post {post.id} : {e}")
        
        logger.info(f"✅ Analytics récupérés pour {len(posts)} posts")
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération analytics : {e}")
        
    finally:
        db.close()


# Scheduler global
scheduler = BackgroundScheduler()


def start_scheduler():
    """Démarre le planificateur de tâches."""
    
    # Job 1 : Publication quotidienne
    scheduler.add_job(
        daily_publication_job,
        trigger='cron',
        hour=settings.publication_hour,
        minute=settings.publication_minute,
        id='daily_publication',
        replace_existing=True
    )
    
    # Job 2 : Récupération analytics (18h chaque jour)
    scheduler.add_job(
        fetch_analytics_job,
        trigger='cron',
        hour=18,
        minute=0,
        id='fetch_analytics',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("⏰ Scheduler démarré")
    logger.info(f"📅 Publication programmée à {settings.publication_hour}h{settings.publication_minute:02d}")


def stop_scheduler():
    """Arrête le planificateur."""
    scheduler.shutdown()
    logger.info("⏹️ Scheduler arrêté")