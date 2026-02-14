"""
AlphaJourney - API FastAPI
Point d'entrée simplifié (sans APScheduler)
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

from app.config import get_settings
from app.database import init_db, get_db
from app.models import Post

# Importer la fonction de publication depuis le script
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from scripts.publish import publish_daily_post

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestion du cycle de vie de l'application."""
    # Startup
    logger.info("🚀 AlphaJourney API - Démarrage")
    init_db()
    
    yield
    
    # Shutdown
    logger.info("⏹️ AlphaJourney API - Arrêt")


app = FastAPI(
    title="AlphaJourney",
    description="Publication automatique Facebook avec IA",
    version="2.3.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Point d'entrée de l'API."""
    from app.data.schedules import WEEKLY_SCHEDULE
    
    today_category = WEEKLY_SCHEDULE[datetime.now().weekday()]
    
    return {
        "app": "AlphaJourney",
        "version": "2.3.0",
        "status": "running",
        "tagline": "💰 Finance | 🤖 IA | 🧠 Dev Personnel",
        "environment": settings.environment,
        "today_category": today_category,
        "publication_schedule": {
            "hour": settings.publication_hour,
            "minute": settings.publication_minute,
            "timezone": settings.timezone
        }
    }


@app.get("/health")
async def health_check():
    """Vérification de santé."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(ZoneInfo(settings.timezone)).isoformat()
    }


@app.get("/config/schedule")
async def get_schedule_config():
    """Retourne la configuration du schedule (pour le cron)."""
    return {
        "publication_hour": settings.publication_hour,
        "publication_minute": settings.publication_minute,
        "timezone": settings.timezone,
        "next_run": _calculate_next_run()
    }


def _calculate_next_run() -> str:
    """Calcule la prochaine exécution."""
    from datetime import timedelta
    
    now = datetime.now(ZoneInfo(settings.timezone))
    target = now.replace(
        hour=settings.publication_hour,
        minute=settings.publication_minute,
        second=0,
        microsecond=0
    )
    
    if target < now:
        target += timedelta(days=1)
    
    return target.isoformat()


@app.post("/publish-now")
async def publish_now():
    """Publication manuelle (pour tests)."""
    try:
        start_time = datetime.now(ZoneInfo(settings.timezone))
        logger.info("📤 Publication manuelle déclenchée")
        
        # Appeler la fonction de publication
        result = await publish_daily_post()
        
        duration = (datetime.now(ZoneInfo(settings.timezone)) - start_time).total_seconds()
        
        if result["success"]:
            return {
                "status": "success",
                "message": "Publication réussie",
                "post_id": result.get("post_id"),
                "fb_post_id": result.get("fb_post_id"),
                "category": result.get("category"),
                "llm_used": result.get("llm_used"),
                "duration_seconds": round(duration, 2),
                "timestamp": start_time.isoformat()
            }
        else:
            return {
                "status": "error",
                "message": result.get("error"),
                "timestamp": start_time.isoformat()
            }
            
    except Exception as e:
        logger.error(f"❌ Erreur : {e}", exc_info=True)
        return {
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now(ZoneInfo(settings.timezone)).isoformat()
        }


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
    
    return {
        "app": "AlphaJourney",
        "total_posts": total_posts,
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
                "created_at": p.created_at.isoformat()
            }
            for p in posts
        ]
    }