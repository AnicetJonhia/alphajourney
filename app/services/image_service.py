"""Service de récupération d'images gratuites (Unsplash/Pexels)."""

import logging
import httpx
import random
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# Mots-clés de recherche par catégorie
IMAGE_KEYWORDS = {
    "finance": [
        "money savings",
        "financial planning",
        "piggy bank",
        "coins growth",
        "investment graph",
        "budget planner",
        "calculator money",
        "wallet cash",
        "financial success",
        "stock market"
    ],
    "ai": [
        "artificial intelligence",
        "technology workspace",
        "laptop coding",
        "digital workspace",
        "robot automation",
        "futuristic tech",
        "computer screen",
        "productivity setup",
        "modern office",
        "smart technology"
    ],
    "personal_dev": [
        "motivation success",
        "goal achievement",
        "person climbing",
        "sunrise motivation",
        "reading book",
        "meditation peace",
        "workout fitness",
        "writing journal",
        "mountain top",
        "focused work"
    ],
    "thread": [
        "success journey",
        "transformation",
        "achievement celebration",
        "path forward",
        "growth mindset"
    ]
}


class ImageService:
    """Service de récupération d'images gratuites."""
    
    def __init__(self):
        # Unsplash (meilleure qualité, gratuit)
        self.unsplash_access_key = settings.unsplash_access_key
        
        # Pexels (backup, gratuit)
        self.pexels_api_key = settings.pexels_api_key
    
    async def get_image_url(
        self,
        category: str,
        timeout: float = 15.0
    ) -> Optional[str]:
        """
        Récupère une URL d'image gratuite pour une catégorie.
        
        Args:
            category: Catégorie du post
            timeout: Timeout en secondes
            
        Returns:
            URL de l'image ou None
        """
        # Essayer Unsplash en priorité
        if self.unsplash_access_key:
            url = await self._get_unsplash_image(category, timeout)
            if url:
                return url
        
        # Fallback sur Pexels
        if self.pexels_api_key:
            url = await self._get_pexels_image(category, timeout)
            if url:
                return url
        
        logger.warning("⚠️ Aucune image trouvée")
        return None
    
    async def _get_unsplash_image(
        self,
        category: str,
        timeout: float
    ) -> Optional[str]:
        """Récupère une image depuis Unsplash."""
        try:
            keywords = IMAGE_KEYWORDS.get(category, IMAGE_KEYWORDS["finance"])
            query = random.choice(keywords)
            
            url = "https://api.unsplash.com/photos/random"
            params = {
                "query": query,
                "orientation": "landscape",
                "content_filter": "high",
                "client_id": self.unsplash_access_key
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                
                data = response.json()
                image_url = data["urls"]["regular"]  # 1080px
                
                logger.info(f"✅ Image Unsplash : {query}")
                return image_url
                
        except Exception as e:
            logger.error(f"❌ Erreur Unsplash : {e}")
            return None
    
    async def _get_pexels_image(
        self,
        category: str,
        timeout: float
    ) -> Optional[str]:
        """Récupère une image depuis Pexels."""
        try:
            keywords = IMAGE_KEYWORDS.get(category, IMAGE_KEYWORDS["finance"])
            query = random.choice(keywords)
            
            url = "https://api.pexels.com/v1/search"
            headers = {"Authorization": self.pexels_api_key}
            params = {
                "query": query,
                "per_page": 1,
                "orientation": "landscape",
                "size": "large"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=headers,
                    params=params,
                    timeout=timeout
                )
                response.raise_for_status()
                
                data = response.json()
                
                if data["photos"]:
                    image_url = data["photos"][0]["src"]["large"]  # 940px
                    logger.info(f"✅ Image Pexels : {query}")
                    return image_url
                
                return None
                
        except Exception as e:
            logger.error(f"❌ Erreur Pexels : {e}")
            return None


def get_image_service() -> ImageService:
    """Retourne une instance du service d'images."""
    return ImageService()