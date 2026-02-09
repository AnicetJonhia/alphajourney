
"""Calendrier éditorial et contenus par catégorie."""

# Calendrier hebdomadaire (jour de la semaine : catégorie)
WEEKLY_SCHEDULE = {
    0: "finance",       # Lundi
    1: "ai",            # Mardi
    2: "personal_dev",  # Mercredi
    3: "finance",       # Jeudi
    4: "ai",            # Vendredi
    5: "personal_dev",  # Samedi
    6: "thread"         # Dimanche
}

# Banque de sujets par catégorie
TOPICS = {
    "finance": [
        "Comment épargner 500€/mois automatiquement",
        "5 erreurs financières à éviter avant 30 ans",
        "Investir 100€/mois : guide pour débutants",
        "La règle 50/30/20 du budget expliquée",
        "Créer un fonds d'urgence en 6 mois",
        "Négocier son salaire : stratégies qui marchent",
        "Budget zero-based : ma méthode pas à pas",
        "Acheter ou louer : le calcul complet",
        "3 revenus passifs accessibles dès maintenant",
        "Éliminer ses dettes : méthode boule de neige"
    ],
    
    "ai": [
        "5 prompts ChatGPT pour gagner 2h par jour",
        "Notion AI : automatiser votre to-do list",
        "Créer des visuels pro en 5 min avec Canva AI",
        "Gamma AI : présentation complète en 60 secondes",
        "Utiliser Claude pour rédiger emails professionnels",
        "Résumer un livre entier en 3 minutes avec IA",
        "Auto-répondeur email intelligent gratuit",
        "Transcription automatique de réunions",
        "Perplexity : le Google boosté à l'IA",
        "10 outils IA gratuits que je utilise chaque jour"
    ],
    
    "personal_dev": [
        "La routine matinale des millionnaires",
        "Atomic Habits : s'améliorer de 1% chaque jour",
        "Vaincre la procrastination en 3 étapes",
        "Le pouvoir de dire NON sans culpabiliser",
        "Lire 50 livres par an : ma méthode",
        "Gérer le stress avec la respiration 4-7-8",
        "Objectifs SMART : template gratuit inclus",
        "La règle des 5 heures de Bill Gates",
        "Méthode Pomodoro : productivité maximale",
        "Comment sortir de sa zone de confort"
    ],
    
    "thread": [
        "Comment j'ai économisé 10 000€ en 1 an",
        "De salarié épuisé à freelance 5K€/mois",
        "J'ai automatisé 80% de mon travail avec l'IA",
        "Ma transformation financière en 365 jours",
        "Comment j'ai quitté le rat race à 32 ans",
        "De 0 à 100K abonnés : les coulisses",
        "La méthode qui a changé ma vie en 6 mois"
    ]
}