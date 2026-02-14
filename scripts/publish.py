#!/usr/bin/env python3
"""
AlphaJourney - Script de publication avec vérification d'heure dynamique
Vérifie PUBLICATION_HOUR avant de publier
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, init_db
from app.services.content_service import ContentService
from app.services.facebook_service import get_facebook_service
from app.data.comments import get_first_comment
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


async def publish_daily_post() -> dict:
    """
    Fonction de publication (retourne un dict pour /publish-now).
    """
    db = SessionLocal()
    
    try:
        content_service = ContentService(db)
        fb_service = get_facebook_service()
        
        # 1. Catégorie
        category = content_service.get_today_category()
        
        # 2. Sujet
        topic = content_service.get_unused_topic(category)
        
        # 3. Contenu + hashtags
        content, llm_used = await content_service.generate_post_content(
            category, topic, timeout=60.0
        )
        
        # 4. Image
        image_url = await content_service.get_post_image(category, timeout=15.0)
        
        # 5. Publication
        fb_post_id = await fb_service.publish(
            content=content,
            image_url=image_url,
            timeout=30.0
        )
        
        # 6. Auto-engagement
        if settings.auto_like or settings.auto_comment:
            await asyncio.sleep(settings.engagement_delay)
            
            if settings.auto_like:
                await fb_service.like_post(fb_post_id, timeout=10.0)
            
            if settings.auto_comment:
                comment_text = get_first_comment(category)
                await fb_service.comment_post(fb_post_id, comment_text, timeout=10.0)
        
        # 7. Sauvegarde
        post = content_service.save_post(
            category=category,
            topic=topic,
            content=content,
            fb_post_id=fb_post_id,
            llm_used=llm_used,
            image_url=image_url
        )
        
        return {
            "success": True,
            "post_id": post.id,
            "fb_post_id": fb_post_id,
            "category": category,
            "llm_used": llm_used
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur : {e}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }
        
    finally:
        db.close()


def should_publish_now() -> bool:
    """
    Vérifie si on doit publier maintenant selon PUBLICATION_HOUR.
    """
    now = datetime.now(ZoneInfo(settings.timezone))
    current_hour = now.hour
    current_minute = now.minute
    
    # Fenêtre de 5 minutes pour éviter de rater
    target_hour = settings.publication_hour
    target_minute = settings.publication_minute
    
    # Publier si on est dans la fenêtre (heure exacte ± 2 minutes)
    if current_hour == target_hour:
        minute_diff = abs(current_minute - target_minute)
        if minute_diff <= 2:
            return True
    
    return False


async def main():
    """Fonction principale avec vérification d'heure."""
    
    logger.info("=" * 60)
    logger.info("🚀 AlphaJourney - Vérification publication")
    
    now = datetime.now(ZoneInfo(settings.timezone))
    logger.info(f"🕐 {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    logger.info(f"⏰ Heure configurée : {settings.publication_hour:02d}:{settings.publication_minute:02d}")
    logger.info("=" * 60)
    
    # Initialiser la DB
    init_db()
    
    # Vérifier si on doit publier
    if should_publish_now():
        logger.info("✅ C'est l'heure de publier !")
        
        result = await publish_daily_post()
        
        if result["success"]:
            logger.info("=" * 60)
            logger.info("🎉 PUBLICATION RÉUSSIE")
            logger.info(f"📊 Post ID (DB) : {result['post_id']}")
            logger.info(f"📊 Post ID (FB) : {result['fb_post_id']}")
            logger.info(f"🤖 LLM : {result['llm_used']}")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("=" * 60)
            logger.error("❌ ÉCHEC DE LA PUBLICATION")
            logger.error(f"Erreur : {result['error']}")
            logger.error("=" * 60)
            return 1
    else:
        logger.info(f"⏳ Pas encore l'heure (heure actuelle : {now.hour:02d}:{now.minute:02d})")
        logger.info("💤 Rien à faire")
        return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)