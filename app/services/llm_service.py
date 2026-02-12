"""Service LLM avec fallback automatique sur 3 providers gratuits."""

import logging
from typing import Optional
import google.generativeai as genai
from groq import Groq
from mistralai.models.chat_completion import ChatMessage
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMService:
    """Service de génération de contenu avec fallback automatique."""
    
    def __init__(self):
        self.providers = []
        self._init_providers()
    
    def _init_providers(self):
        """Initialise les providers disponibles dans l'ordre de priorité."""
        
        # 1. Gemini (Google) - Gratuit, performant
        if settings.gemini_api_key:
            try:
                genai.configure(api_key=settings.gemini_api_key)
                self.providers.append({
                    'name': 'gemini',
                    'client': genai.GenerativeModel('gemini-3-flash-preview'),
                    'method': self._generate_gemini
                })
                logger.info("✅ Gemini initialisé")
            except Exception as e:
                logger.warning(f"⚠️ Gemini non disponible : {e}")
        
        # 2. Groq (Meta Llama) - Très rapide, gratuit
        if settings.groq_api_key:
            try:
                client = Groq(api_key=settings.groq_api_key)
                self.providers.append({
                    'name': 'groq',
                    'client': client,
                    'method': self._generate_groq
                })
                logger.info("✅ Groq initialisé")
            except Exception as e:
                logger.warning(f"⚠️ Groq non disponible : {e}")
        
        
        if not self.providers:
            raise ValueError("❌ Aucun provider LLM configuré ! Ajoutez au moins une clé API.")
    
    def _generate_gemini(self, client, prompt: str) -> str:
        """Génère avec Gemini."""
        response = client.generate_content(prompt)
        return response.text
    
    def _generate_groq(self, client, prompt: str) -> str:
        """Génère avec Groq."""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    
    def generate(self, prompt: str) -> tuple[str, str]:
        """
        Génère du contenu avec fallback automatique.
        
        Returns:
            tuple: (contenu généré, nom du provider utilisé)
        """
        for provider in self.providers:
            try:
                logger.info(f"🔄 Tentative avec {provider['name']}...")
                
                content = provider['method'](provider['client'], prompt)
                
                logger.info(f"✅ Contenu généré avec {provider['name']}")
                return content, provider['name']
                
            except Exception as e:
                logger.error(f"❌ Erreur avec {provider['name']} : {e}")
                continue
        
        raise Exception("❌ Tous les providers LLM ont échoué")


# Singleton
_llm_service: Optional[LLMService] = None

def get_llm_service() -> LLMService:
    """Retourne l'instance singleton du service LLM."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service