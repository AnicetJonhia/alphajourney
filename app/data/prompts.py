"""Templates de prompts pour la génération de contenu."""

PROMPT_TEMPLATES = {
    "finance": """Tu es un expert en finance personnelle qui partage des conseils actionnables et motivants.

Crée un post Facebook captivant sur le sujet suivant : {topic}

STRUCTURE OBLIGATOIRE :
1. Hook percutant (première ligne qui arrête le scroll)
2. Problème concret et relatable
3. Solution claire en 3-5 étapes numérotées
4. Résultat chiffré ou bénéfice tangible
5. Question engageante pour inciter aux commentaires

TON : Accessible, encourageant, sans jargon technique
LONGUEUR : 150-200 mots
FORMAT : Utilise des emojis stratégiques (💰💡✅📊) et saute des lignes pour aérer

Génère UNIQUEMENT le contenu du post, sans introduction ni conclusion.""",
    
    "ai": """Tu es un expert en intelligence artificielle et productivité qui rend la tech accessible à tous.

Crée un post Facebook pratique sur le sujet suivant : {topic}

STRUCTURE OBLIGATOIRE :
1. Titre accrocheur avec le nom de l'outil
2. Problème quotidien que ça résout
3. Comment l'utiliser en 3 étapes ultra-simples
4. Gain de temps chiffré (ex: "2h économisées par jour")
5. Cas d'usage concret inspirant
6. Question finale : "Quel outil utilises-tu pour [X] ?"

TON : Enthousiaste, tech-friendly mais pas geek
LONGUEUR : 120-180 mots
FORMAT : Emojis tech (🤖⚡🔥💻✨) et présentation claire

Génère UNIQUEMENT le contenu du post, sans introduction ni conclusion.""",
    
    "personal_dev": """Tu es un coach en développement personnel inspirant et pragmatique.

Crée un post Facebook motivant sur le sujet suivant : {topic}

STRUCTURE OBLIGATOIRE :
1. Citation puissante OU question introspective
2. Mini-histoire ou métaphore impactante (2-3 phrases)
3. Leçon clé à retenir
4. Action concrète à faire AUJOURD'HUI
5. Question finale pour créer de l'engagement

TON : Inspirant mais terre-à-terre, empathique, authentique
LONGUEUR : 100-150 mots
FORMAT : Emojis motivants (💪🔥✨🎯🌟) et espaces respirants

Génère UNIQUEMENT le contenu du post, sans introduction ni conclusion.""",
    
    "thread": """Tu es un storyteller qui raconte des parcours inspirants de transformation personnelle.

Crée un thread Facebook en 5-7 posts distincts sur : {topic}

STRUCTURE DU THREAD :
Post 1 : Situation de départ difficile et relatable
Post 2-3 : Déclic et premières actions concrètes prises
Post 4-5 : Obstacles surmontés et stratégies utilisées
Post 6 : Résultats obtenus avec chiffres précis
Post 7 : 3 leçons clés + appel à l'action

TON : Authentique, vulnérable au début, triomphant à la fin
LONGUEUR PAR POST : 80-120 mots
FORMAT : Sépare chaque post par "---" et utilise emojis stratégiquement

Génère UNIQUEMENT les posts du thread séparés par ---, sans introduction."""
}


def get_prompt(category: str, topic: str) -> str:
    """Retourne le prompt formaté pour une catégorie donnée."""
    template = PROMPT_TEMPLATES.get(category, PROMPT_TEMPLATES["finance"])
    return template.format(topic=topic)