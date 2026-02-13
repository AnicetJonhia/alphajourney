"""Service de publication Facebook avec images."""

import logging
import httpx
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FacebookService:
    """Gestion des publications Facebook avec images."""
    
    def __init__(self):
        self.access_token = settings.fb_access_token
        self.page_id = settings.fb_page_id
        self.base_url = "https://graph.facebook.com/v19.0"
    
    async def publish(
        self,
        content: str,
        image_url: Optional[str] = None,
        timeout: float = 30.0
    ) -> str:
        """
        Publie un post sur Facebook avec ou sans image.
        
        Args:
            content: Texte du post
            image_url: URL de l'image (optionnel)
            timeout: Timeout en secondes
            
        Returns:
            ID du post publié
        """
        if image_url:
            return await self._publish_with_photo(content, image_url, timeout)
        else:
            return await self._publish_text_only(content, timeout)
    
    async def _publish_text_only(
        self,
        content: str,
        timeout: float
    ) -> str:
        """Publie un post texte uniquement."""
        url = f"{self.base_url}/{self.page_id}/feed"
        
        payload = {
            "message": content,
            "access_token": self.access_token
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    data=payload,
                    timeout=timeout
                )
                response.raise_for_status()
                
                result = response.json()
                post_id = result.get("id")
                
                logger.info(f"✅ Post texte publié : {post_id}")
                return post_id
                
        except Exception as e:
            logger.error(f"❌ Erreur publication : {e}")
            raise
    
    async def _publish_with_photo(
        self,
        content: str,
        image_url: str,
        timeout: float
    ) -> str:
        """Publie un post avec photo."""
        url = f"{self.base_url}/{self.page_id}/photos"
        
        payload = {
            "url": image_url,  # URL de l'image
            "message": content,
            "access_token": self.access_token
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    data=payload,
                    timeout=timeout
                )
                response.raise_for_status()
                
                result = response.json()
                post_id = result.get("post_id")  # Attention: post_id, pas id
                
                logger.info(f"✅ Post avec photo publié : {post_id}")
                return post_id
                
        except Exception as e:
            logger.error(f"❌ Erreur publication photo : {e}")
            # Fallback : publier sans photo
            logger.info("🔄 Tentative sans photo...")
            return await self._publish_text_only(content, timeout)
    
    async def get_post_insights(self, post_id: str, timeout: float = 30.0) -> dict:
        """Récupère les statistiques d'un post."""
        url = f"{self.base_url}/{post_id}"
        
        params = {
            "fields": "likes.summary(true),shares,comments.summary(true)",
            "access_token": self.access_token
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                data = response.json()
                
                stats = {
                    "likes": data.get("likes", {}).get("summary", {}).get("total_count", 0),
                    "shares": data.get("shares", {}).get("count", 0),
                    "comments": data.get("comments", {}).get("summary", {}).get("total_count", 0),
                    "reach": 0
                }
                
                logger.info(f"📊 Stats récupérées pour {post_id}")
                return stats
                
        except Exception as e:
            logger.error(f"❌ Erreur stats : {e}")
            return {"likes": 0, "shares": 0, "comments": 0, "reach": 0}


def get_facebook_service() -> FacebookService:
    """Retourne une instance du service Facebook."""
    return FacebookService()