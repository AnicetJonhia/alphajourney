"""
AlphaJourney - API FastAPI
Publication gérée par GitHub Actions
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import get_settings
from app.database import init_db, get_db
from app.models import Post
from app.services.content_service import ContentService
from app.services.facebook_service import get_facebook_service
from app.data.comments import get_first_comment
from app.data.schedules import WEEKLY_SCHEDULE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application."""
    logger.info("🚀 AlphaJourney API - Démarrage")
    init_db()
    logger.info("✅ Base de données initialisée")
    
    yield
    
    logger.info("⏹️ AlphaJourney API - Arrêt")


app = FastAPI(
    title="AlphaJourney",
    description="Publication automatique Facebook avec IA",
    version="3.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Point d'entrée de l'API."""
    today_category = WEEKLY_SCHEDULE[datetime.now().weekday()]
    
    return {
        "app": "AlphaJourney",
        "version": "3.0.0",
        "status": "running",
        "tagline": "💰 Finance | 🤖 IA | 🧠 Dev Personnel",
        "environment": settings.environment,
        "today_category": today_category,
        "scheduling": "GitHub Actions"
    }


@app.get("/health")
async def health_check():
    """Vérification de santé (appelé par GitHub Actions pour warm-up)."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(ZoneInfo(settings.timezone)).isoformat(),
        "timezone": settings.timezone
    }


@app.post("/publish-now")
async def publish_now():
    """
    Publication immédiate (appelé par GitHub Actions).
    Endpoint principal utilisé par le workflow.
    """
    start_time = datetime.now(ZoneInfo(settings.timezone))
    logger.info("=" * 60)
    logger.info("📤 Publication déclenchée par GitHub Actions")
    logger.info(f"🕐 {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    logger.info("=" * 60)
    
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
        
        # 4. Récupérer image
        logger.info("📸 Recherche d'image...")
        image_url = await content_service.get_post_image(category, timeout=15.0)
        
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
            import asyncio
            logger.info(f"⏳ Attente {settings.engagement_delay}s avant engagement...")
            await asyncio.sleep(settings.engagement_delay)
            
            # Like
            if settings.auto_like:
                like_ok = await fb_service.like_post(fb_post_id, timeout=10.0)
                if like_ok:
                    logger.info("👍 Post liké automatiquement")
            
            # Commentaire
            if settings.auto_comment:
                comment_text = get_first_comment(category)
                comment_id = await fb_service.comment_post(
                    fb_post_id, comment_text, timeout=10.0
                )
                if comment_id:
                    logger.info(f"💬 Commentaire publié : {comment_id}")
        
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
        
        # Résultat
        end_time = datetime.now(ZoneInfo(settings.timezone))
        duration = (end_time - start_time).total_seconds()
        
        logger.info("=" * 60)
        logger.info("🎉 PUBLICATION RÉUSSIE")
        logger.info(f"📊 Post ID (DB) : {post.id}")
        logger.info(f"📊 Post ID (FB) : {fb_post_id}")
        logger.info(f"🤖 LLM utilisé : {llm_used}")
        logger.info(f"⏱️ Durée totale : {duration:.2f}s")
        logger.info("=" * 60)
        
        return {
            "status": "success",
            "message": "Publication réussie",
            "post_id": post.id,
            "fb_post_id": fb_post_id,
            "category": category,
            "topic": topic,
            "llm_used": llm_used,
            "has_image": image_url is not None,
            "duration_seconds": round(duration, 2),
            "timestamp": end_time.isoformat()
        }
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error("❌ ERREUR LORS DE LA PUBLICATION")
        logger.error(f"Type : {type(e).__name__}")
        logger.error(f"Message : {str(e)}")
        logger.error("=" * 60, exc_info=True)
        
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now(ZoneInfo(settings.timezone)).isoformat()
        }
        
    finally:
        db.close()


@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Statistiques globales."""
    from sqlalchemy import func
    
    total_posts = db.query(Post).count()
    
    top_posts = db.query(Post).order_by(
        Post.engagement_score.desc()
    ).limit(5).all()
    
    by_category = db.query(
        Post.category,
        func.count(Post.id).label('count'),
        func.avg(Post.engagement_score).label('avg_score')
    ).group_by(Post.category).all()
    
    total_engagement = db.query(
        func.sum(Post.likes + Post.shares * 2 + Post.comments * 3)
    ).scalar() or 0
    
    return {
        "app": "AlphaJourney",
        "total_posts": total_posts,
        "total_engagement": total_engagement,
        "top_posts": [
            {
                "id": p.id,
                "topic": p.topic,
                "category": p.category,
                "engagement": p.engagement_score,
                "llm_used": p.llm_used
            }
            for p in top_posts
        ],
        "by_category": [
            {
                "category": cat,
                "posts": count,
                "avg_engagement": round(avg, 2) if avg else 0
            }
            for cat, count, avg in by_category
        ]
    }


@app.get("/recent-posts")
async def get_recent_posts(limit: int = 10, db: Session = Depends(get_db)):
    """Liste des posts récents."""
    posts = db.query(Post).order_by(
        Post.created_at.desc()
    ).limit(limit).all()
    
    return {
        "posts": [
            {
                "id": p.id,
                "category": p.category,
                "topic": p.topic,
                "llm_used": p.llm_used,
                "engagement_score": p.engagement_score,
                "likes": p.likes,
                "shares": p.shares,
                "comments": p.comments,
                "created_at": p.created_at.isoformat()
            }
            for p in posts
        ]
    }