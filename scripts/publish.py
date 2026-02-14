#!/usr/bin/env python3
"""
AlphaJourney - Script de publication quotidienne
Exécuté par Render Cron Job tous les jours à 19h (Madagascar)
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal, init_db
from app.services.content_service import ContentService
from app.services.facebook_service import get_facebook_service
from app.data.comments import get_first_comment
from app.config import get_settings

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


async def main():
    """Fonction principale de publication."""
    start_time = datetime.now(ZoneInfo(settings.timezone))
    
    logger.info("=" * 60)
    logger.info("🚀 AlphaJourney - Publication quotidienne")
    logger.info(f"🕐 {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    logger.info("=" * 60)
    
    # Initialiser la DB
    init_db()
    db = SessionLocal()
    
    try:
        content_service = ContentService(db)
        fb_service = get_facebook_service()
        
        # 1. Catégorie du jour
        category = content_service.get_today_category()
        logger.info(f"📅 Catégorie : {category}")
        
        # 2. Sujet non répété
        topic = content_service.get_unused_topic(category)
        logger.info(f"📝 Sujet : {topic}")
        
        # 3. Générer contenu + hashtags
        logger.info("🤖 Génération du contenu...")
        content, llm_used = await content_service.generate_post_content(
            category, topic, timeout=60.0
        )
        logger.info(f"✅ Contenu généré avec {llm_used}")
        logger.info(f"📏 Longueur : {len(content)} caractères")
        
        # 4. Récupérer image
        logger.info("📸 Recherche d'image...")
        image_url = await content_service.get_post_image(
            category, timeout=15.0
        )
        
        if image_url:
            logger.info(f"✅ Image trouvée : {image_url[:50]}...")
        else:
            logger.warning("⚠️ Pas d'image - publication en texte seul")
        
        # 5. Publier sur Facebook
        logger.info("📤 Publication sur Facebook...")
        fb_post_id = await fb_service.publish(
            content=content,
            image_url=image_url,
            timeout=30.0
        )
        logger.info(f"✅ Post publié : {fb_post_id}")
        
        # 6. Auto-engagement (si activé)
        if settings.auto_like or settings.auto_comment:
            logger.info(f"⏳ Attente {settings.engagement_delay}s avant engagement...")
            await asyncio.sleep(settings.engagement_delay)
            
            # Like
            if settings.auto_like:
                like_ok = await fb_service.like_post(fb_post_id, timeout=10.0)
                if like_ok:
                    logger.info("👍 Post liké automatiquement")
                else:
                    logger.warning("⚠️ Échec du like")
            
            # Commentaire
            if settings.auto_comment:
                comment_text = get_first_comment(category)
                logger.info(f"💬 Commentaire : {comment_text[:50]}...")
                
                comment_id = await fb_service.comment_post(
                    fb_post_id, comment_text, timeout=10.0
                )
                
                if comment_id:
                    logger.info(f"✅ Commentaire publié : {comment_id}")
                else:
                    logger.warning("⚠️ Échec du commentaire")
        
        # 7. Sauvegarder en base
        logger.info("💾 Sauvegarde en base de données...")
        post = content_service.save_post(
            category=category,
            topic=topic,
            content=content,
            fb_post_id=fb_post_id,
            llm_used=llm_used,
            image_url=image_url
        )
        
        # Résumé final
        end_time = datetime.now(ZoneInfo(settings.timezone))
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=" * 60)
        logger.info("🎉 PUBLICATION RÉUSSIE")
        logger.info(f"📊 Post ID (DB) : {post.id}")
        logger.info(f"📊 Post ID (FB) : {fb_post_id}")
        logger.info(f"🤖 LLM utilisé : {llm_used}")
        logger.info(f"📸 Image : {'Oui' if image_url else 'Non'}")
        logger.info(f"👍 Like : {'Oui' if settings.auto_like else 'Non'}")
        logger.info(f"💬 Commentaire : {'Oui' if settings.auto_comment else 'Non'}")
        logger.info(f"⏱️ Durée totale : {duration:.2f}s")
        logger.info(f"🕐 {end_time.strftime('%H:%M:%S')}")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ ERREUR LORS DE LA PUBLICATION")
        logger.error(f"Type : {type(e).__name__}")
        logger.error(f"Message : {str(e)}")
        logger.error("=" * 60, exc_info=True)
        return 1
        
    finally:
        db.close()


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)