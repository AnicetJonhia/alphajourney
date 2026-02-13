"""Configuration centralisée."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Paramètres de l'application."""
    
    # Database
    database_url: str
    
    # Facebook
    fb_access_token: str
    fb_page_id: str
    
    # LLM APIs
    groq_api_key: str | None = None
    gemini_api_key: str | None = None
    
    # Image APIs (optionnels)
    unsplash_access_key: str | None = None
    pexels_api_key: str | None = None
    
    # Scheduler
    publication_hour: int = 14
    publication_minute: int = 0
    
    # App
    environment: str = "production"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Singleton pour accès aux settings."""
    return Settings()