"""Service de publication sur Facebook."""

import logging
import requests
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FacebookService:
    """Gestion des publications Facebook Graph API."""
    
    def __init__(self):
        self.access_token = settings.fb_access_token
        self.page_id = settings.fb_page_id
        self.base_url = "https://graph.facebook.com/v19.0"
    
    def publish(self, content: str) -> str:
        """
        Publie un post sur la page Facebook.
        
        Args:
            content: Le contenu du post
            
        Returns:
            str: ID du post publié
        """
        url = f"{self.base_url}/{self.page_id}/feed"
        
        payload = {
            "message": content,
            "access_token": self.access_token
        }
        
        try:
            response = requests.post(url, data=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get("id")
            
            if not post_id:
                raise ValueError(f"Pas d'ID dans la réponse : {result}")
            
            logger.info(f"✅ Post publié sur Facebook : {post_id}")
            return post_id
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur lors de la publication : {e}")
            raise
    
    def get_post_insights(self, post_id: str) -> dict:
        """
        Récupère les statistiques d'un post.
        
        Args:
            post_id: ID du post Facebook
            
        Returns:
            dict: Statistiques (likes, shares, comments, reach)
        """
        url = f"{self.base_url}/{post_id}"
        
        params = {
            "fields": "likes.summary(true),shares,comments.summary(true)",
            "access_token": self.access_token
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            stats = {
                "likes": data.get("likes", {}).get("summary", {}).get("total_count", 0),
                "shares": data.get("shares", {}).get("count", 0),
                "comments": data.get("comments", {}).get("summary", {}).get("total_count", 0),
                "reach": 0  # Nécessite permissions avancées
            }
            
            logger.info(f"📊 Stats récupérées pour {post_id}")
            return stats
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur récupération stats : {e}")
            return {"likes": 0, "shares": 0, "comments": 0, "reach": 0}


def get_facebook_service() -> FacebookService:
    """Retourne une instance du service Facebook."""
    return FacebookService()