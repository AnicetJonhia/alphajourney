"""Point d'entrée de l'application FastAPI."""

import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.config import get_settings
from app.database import init_db, get_db
from app.scheduler import start_scheduler, stop_scheduler, daily_publication_job
from app.models import Post
from datetime import datetime
from zoneinfo import ZoneInfo

# Configuration logging
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
    logger.info("🚀 Démarrage de l'application")
    init_db()
    start_scheduler()
    
    yield
    
    # Shutdown
    logger.info("⏹️ Arrêt de l'application")
    stop_scheduler()


app = FastAPI(
    title="AutoPost Facebook",
    description="Publication automatique sur Facebook avec LLM",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def root():
    """Point d'entrée de l'API."""
    from app.data.schedules import WEEKLY_SCHEDULE
    from datetime import datetime
    
    today_category = WEEKLY_SCHEDULE[datetime.now().weekday()]
    
    return {
        "status": "running",
        "environment": settings.environment,
        "today_category": today_category,
        "publication_time": f"{settings.publication_hour:02d}:{settings.publication_minute:02d}"
    }


@app.get("/health")
def health_check():
    """Vérification de santé de l'application."""
    return {"status": "healthy"}


@app.post("/publish-now")
async def publish_now():
    """Déclenche une publication immédiate (pour tests)."""
    try:
        await asyncio.to_thread(daily_publication_job)
        return {"status": "success", "message": "Publication déclenchée"}
    except Exception as e:
        logger.error(f"Erreur publication manuelle : {e}")
        return {"status": "error", "message": str(e)}


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Statistiques globales."""
    total_posts = db.query(Post).count()
    
    # Top performers
    top_posts = db.query(Post).order_by(
        Post.engagement_score.desc()
    ).limit(5).all()
    
    # Par catégorie
    from sqlalchemy import func
    by_category = db.query(
        Post.category,
        func.count(Post.id).label('count'),
        func.avg(Post.engagement_score).label('avg_score')
    ).group_by(Post.category).all()
    
    return {
        "total_posts": total_posts,
        "top_posts": [
            {
                "id": p.id,
                "topic": p.topic,
                "engagement": p.engagement_score,
                "likes": p.likes
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
def get_recent_posts(limit: int = 10, db: Session = Depends(get_db)):
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
                "likes": p.likes,
                "created_at": p.created_at.isoformat()
            }
            for p in posts
        ]
    }




@app.get("/schedule")
async def get_schedule():
    """Retourne la configuration du schedule."""
    return {
        "publication_hour": settings.publication_hour,
        "publication_minute": settings.publication_minute,
        "timezone": "Indian/Antananarivo",  # UTC+3
        "next_run": get_next_run_time()
    }

def get_next_run_time() -> str:
    """Calcule la prochaine exécution."""
    now = datetime.now(ZoneInfo("Indian/Antananarivo"))
    target = now.replace(
        hour=settings.publication_hour,
        minute=settings.publication_minute,
        second=0,
        microsecond=0
    )
    
    if target < now:
        # Ajouter 1 jour si l'heure est déjà passée
        from datetime import timedelta
        target += timedelta(days=1)
    
    return target.isoformat()