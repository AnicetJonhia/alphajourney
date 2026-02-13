"""Service LLM avec fallback automatique sur 3 providers gratuits (async).

Note: les SDKs tiers étant parfois bloquants, on exécute leurs appels dans
`asyncio.to_thread` pour éviter de bloquer la boucle d'événements FastAPI.
"""

import logging
import asyncio
from typing import Optional
import google.generativeai as genai
from groq import Groq
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

        # 1. Gemini (Google)
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

        # 2. Groq
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

    async def _generate_gemini(self, client, prompt: str) -> str:
        """Génère avec Gemini (exécuté dans un thread si bloquant)."""
        def sync_call():
            return client.generate_content(prompt)

        response = await asyncio.to_thread(sync_call)
        return getattr(response, 'text', str(response))

    async def _generate_groq(self, client, prompt: str) -> str:
        """Génère avec Groq (exécuté dans un thread si bloquant)."""
        def sync_call():
            return client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )

        response = await asyncio.to_thread(sync_call)
        # response structure may vary
        try:
            return response.choices[0].message.content
        except Exception:
            return str(response)

    async def generate(self, prompt: str, timeout: float | None = None) -> tuple[str, str]:
        """
        Génère du contenu avec fallback automatique (async).

        If `timeout` is provided, it will be applied to each provider call using
        `asyncio.wait_for` so a slow provider doesn't block the fallback loop.

        Returns:
            tuple: (contenu généré, nom du provider utilisé)
        """
        for provider in self.providers:
            try:
                logger.info(f"🔄 Tentative avec {provider['name']}...")

                if timeout is not None:
                    content = await asyncio.wait_for(
                        provider['method'](provider['client'], prompt), timeout=timeout
                    )
                else:
                    content = await provider['method'](provider['client'], prompt)

                logger.info(f"✅ Contenu généré avec {provider['name']}")
                return content, provider['name']

            except asyncio.TimeoutError:
                logger.error(f"⏱️ Timeout with {provider['name']} after {timeout}s")
                continue
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



