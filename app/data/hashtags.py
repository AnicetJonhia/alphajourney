"""Hashtags par catégorie pour AlphaJourney."""

# Hashtags par catégorie (3-5 par post)
HASHTAGS = {
    "finance": [
        # Core
        "#FinancePersonnelle",
        "#Épargne",
        "#Investissement",
        "#BudgetFamilial",
        "#LibertéFinancière",
        
        # Spécifiques
        "#ÉconomiserArgent",
        "#GestionBudget",
        "#InvestirJeune",
        "#RevenusPassifs",
        "#IndépendanceFinancière",
        "#ArgentIntelligent",
        "#ÉducationFinancière",
        "#PatrimoineFinancier",
        
        # Tendances
        "#MoneyTips",
        "#FinanceTips",
        "#SmartMoney"
    ],
    
    "ai": [
        # Core
        "#IntelligenceArtificielle",
        "#IA",
        "#Productivité",
        "#AutomatisationIA",
        "#OutilsIA",
        
        # Spécifiques
        "#ChatGPT",
        "#GeminiAI",
        "#ProductivitéMaximale",
        "#TravailIntelligent",
        "#GainDeTemps",
        "#TechPourTous",
        "#IAAccessible",
        "#TransformationDigitale",
        
        # Tendances
        "#AITools",
        "#ProductivityHacks",
        "#AIForWork"
    ],
    
    "personal_dev": [
        # Core
        "#DéveloppementPersonnel",
        "#Motivation",
        "#Mindset",
        "#CroissancePersonnelle",
        "#SucèsPersonnel",
        
        # Spécifiques
        "#HabitudesGagnantes",
        "#ObjectifsDeVie",
        "#RoutineMatinale",
        "#DisciplinePersonnelle",
        "#ConfianceEnSoi",
        "#AmélioreToiMême",
        "#VersionSupérieure",
        "#TransformationPersonnelle",
        
        # Tendances
        "#SelfImprovement",
        "#PersonalGrowth",
        "#MindsetMatters"
    ],
    
    "thread": [
        # Mix des 3 catégories
        "#SuccessStory",
        "#Inspiration",
        "#Transformation",
        "#LibertéFinancière",
        "#DéveloppementPersonnel",
        "#Motivation",
        "#HistoireDeRéussite",
        "#ChangementDeVie"
    ]
}


def get_hashtags(category: str, count: int = 5) -> list[str]:
    """
    Retourne des hashtags aléatoires pour une catégorie.
    
    Args:
        category: Catégorie du post
        count: Nombre de hashtags à retourner
        
    Returns:
        Liste de hashtags
    """
    import random
    
    tags = HASHTAGS.get(category, HASHTAGS["finance"])
    
    # Sélectionner aléatoirement
    selected = random.sample(tags, min(count, len(tags)))
    
    return selected


def format_hashtags(hashtags: list[str]) -> str:
    """
    Formate les hashtags pour Facebook.
    
    Returns:
        String formaté : "\n\n#Tag1 #Tag2 #Tag3"
    """
    return "\n\n" + " ".join(hashtags)