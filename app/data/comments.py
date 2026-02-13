"""Commentaires automatiques pour les posts AlphaJourney."""

import random

# Commentaires par catégorie
FIRST_COMMENTS = {
    "finance": [
        "💡 Et vous, quelle est votre stratégie d'épargne préférée ? Partagez vos astuces en commentaires !",
        "📊 Question : Combien épargnez-vous par mois actuellement ? (Même 50€ c'est un début !)",
        "🎯 Astuce bonus : Automatisez votre épargne dès le jour de paie pour ne jamais y penser !",
        "💰 Fun fact : Épargner seulement 5€/jour = 1825€/an ! Qui commence aujourd'hui ?",
        "🤔 Sondage rapide : Préférez-vous épargner régulièrement ou par gros montants ? Pourquoi ?",
        "✅ Challenge du mois : Économisez 10% de vos revenus et revenez nous dire comment ça s'est passé !",
        "📌 Conseil d'expert : La meilleure épargne est celle que vous ne voyez jamais partir !",
        "💬 Partagez : Quelle est la plus grosse erreur financière que vous ayez évitée ?",
        "🔥 Astuce du jour : Arrondissez vos achats au euro supérieur et épargnez la différence !",
        "🎁 Bonus : Téléchargez notre template de budget gratuit dans les commentaires (bientôt disponible) !",
    ],
    
    "ai": [
        "🤖 Question : Quel outil IA utilisez-vous au quotidien ? Partagez vos découvertes !",
        "⚡ Astuce : Saviez-vous que ChatGPT peut résumer vos réunions en quelques secondes ?",
        "💻 Sondage : Combien de temps économisez-vous par jour grâce à l'IA ?",
        "🔥 Challenge : Testez un nouvel outil IA cette semaine et partagez votre expérience !",
        "✨ Fun fact : 80% des tâches répétitives peuvent être automatisées avec l'IA gratuite !",
        "📌 Conseil : Commencez petit - automatisez UNE tâche cette semaine !",
        "💡 Question bonus : Quelle tâche rêvez-vous d'automatiser ?",
        "🎯 Astuce pro : Combinez plusieurs outils IA pour des résultats encore meilleurs !",
        "🚀 Tendance : L'IA va remplacer les tâches, pas les emplois. Préparez-vous maintenant !",
        "💬 Partagez : Votre plus belle découverte IA du mois ?",
    ],
    
    "personal_dev": [
        "💪 Question : Quelle habitude avez-vous changée récemment ? Comment ça se passe ?",
        "🌅 Astuce : Votre routine matinale définit votre journée. Quelle est la vôtre ?",
        "🎯 Challenge : Notez 3 objectifs pour cette semaine et partagez-les ici !",
        "✨ Motivation : Vous êtes à une décision de transformer votre vie. C'est laquelle ?",
        "📚 Question lecture : Quel livre vous a le plus inspiré cette année ?",
        "🔥 Sondage : Préférez-vous la discipline ou la motivation ? Pourquoi ?",
        "💡 Réflexion : Dans 5 ans, vous remercierez votre vous d'aujourd'hui pour quelle action ?",
        "🎁 Astuce bonus : La méthode des 2 minutes - si ça prend moins de 2 min, faites-le maintenant !",
        "🌟 Inspiration : Votre futur vous observe. Rendez-le fier aujourd'hui !",
        "💬 Partagez : Votre plus grande victoire personnelle cette semaine ?",
    ],
    
    "thread": [
        "🔥 Cette histoire résonne avec vous ? Partagez la vôtre en commentaires !",
        "💬 Question : Quel a été votre plus grand défi cette année ?",
        "✨ Inspiration : Votre parcours peut inspirer quelqu'un. Racontez-le !",
        "🎯 Et vous, quelle transformation visez-vous pour les 6 prochains mois ?",
        "💪 Sondage : Vous êtes plutôt team 'action immédiate' ou 'planification détaillée' ?",
        "🌟 Partagez : Votre meilleure décision de l'année ?",
        "🚀 Challenge : Fixez-vous UN objectif audacieux et partagez-le ici pour l'accountability !",
        "💡 Réflexion : Si vous pouviez revenir 1 an en arrière, quel conseil vous donneriez-vous ?",
        "🔥 Question bonus : Qu'est-ce qui vous empêche encore de passer à l'action ?",
        "💬 Motivation : Votre success story commence aujourd'hui. Premier pas ?",
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