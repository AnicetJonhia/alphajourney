"""Configuration de la base de données PostgreSQL."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# Engine SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Vérifier la connexion avant utilisation
    pool_size=5,
    max_overflow=10
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()


def get_db():
    """Générateur de sessions DB."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialiser les tables."""
    Base.metadata.create_all(bind=engine)