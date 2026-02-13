"""Commentaires automatiques pour les posts AlphaJourney."""

import random

# Commentaires par catégorie
FIRST_COMMENTS = {
    "finance": [
        "T'épargnes combien chaque mois ? 😊",
        "Ton astuce économie préférée ? 💡",
        "Objectif financier 2026 ? 🎯",
        "Première somme mise de côté ? 💰",
        "Erreur argent évitée ? ⚠️",
        "10% de ton salaire de côté ? 📈",
    ],
    "ai": [
        "Ton outil IA du moment ? 🤖",
        "Combien de temps gagné aujourd'hui ? ⚡",
        "Tâche que tu automatises ? 🚀",
        "Meilleur prompt récent ? ✨",
        "IA tous les jours ? 📅",
        "Découverte IA qui t'a choqué ? 😲",
    ],
    "personal_dev": [
        "Habitude changée récemment ? 💪",
        "Objectif de la semaine ? 🗓️",
        "Victoire perso aujourd'hui ? 🌟",
        "Livre qui t'inspire ? 📚",
        "Routine matinale ? ☕",
        "Pensée qui te bloque ? 🤔",
    ],
    "thread": [
        "Ça te parle ? Raconte ! 💬",
        "Ton plus gros défi ? 🔥",
        "Meilleure décision récente ? 👍",
        "Objectif dans 6 mois ? ⏳",
        "Premier pas aujourd'hui ? 👟",
    ]
}

def get_first_comment(category: str) -> str:
    """
    Retourne un commentaire aléatoire pour une catégorie.
    
    Args:
        category: Catégorie du post
        
    Returns:
        Texte du commentaire
    """
    comments = FIRST_COMMENTS.get(category, FIRST_COMMENTS["finance"])
    return random.choice(comments)