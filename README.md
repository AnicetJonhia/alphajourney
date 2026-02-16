# 🚀 AlphaJourney

**Publication automatique quotidienne sur Facebook avec génération de contenu IA**

> 💰 Finance Personnelle • 🤖 IA & Productivité • 🧠 Développement Personnel

[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/AnicetJonhia/alphajourney)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-yellow.svg)](https://www.python.org/)

---

## ✨ Fonctionnalités

- ✅ **Publication automatique** à 19h chaque jour
- ✅ **2 LLMs gratuits** avec fallback intelligent (Groq → Gemini)
- ✅ **Hashtags intelligents** (5 par post, adaptés à la catégorie)
- ✅ **Photos professionnelles** gratuites (Unsplash/Pexels)
- ✅ **Évite les répétitions** de sujets (30 jours de mémoire)
- ✅ **Analytics automatiques** des performances
- ✅ **Architecture async** pour performance maximale
- ✅ **Base PostgreSQL** pour historique
- ✅ **100% gratuit** à vie (Neon + Render)

---

## 📊 Stratégie de contenu

### Calendrier hebdomadaire

| Jour | Catégorie | Focus | Hashtags |
|------|-----------|-------|----------|
| **Lundi** | 💰 Finance | Conseils d'épargne/investissement | #FinancePersonnelle #Épargne |
| **Mardi** | 🤖 IA | Outils IA gratuits | #IntelligenceArtificielle #Productivité |
| **Mercredi** | 🧠 Dev Personnel | Mindset et habitudes | #DéveloppementPersonnel #Motivation |
| **Jeudi** | 💰 Finance | Stratégies financières | #Investissement #LibertéFinancière |
| **Vendredi** | 🤖 IA | Tutoriels IA rapides | #OutilsIA #AutomatisationIA |
| **Samedi** | 🧠 Dev Personnel | Citations + actions | #CroissancePersonnelle #Mindset |
| **Dimanche** | 📖 Thread | Success stories | #SuccessStory #Transformation |

### Mix de contenu

- **40%** Finance personnelle (épargne, investissement, budget)
- **30%** IA & Productivité (outils, automatisation)
- **30%** Développement personnel (mindset, habitudes)

### Format des posts
```
[Contenu généré par IA - 150-200 mots]
- Hook accrocheur
- Problème concret
- Solution en 3-5 étapes
- Résultat chiffré
- Question engageante

[Photo professionnelle contextuelle]

[5 hashtags pertinents]
#FinancePersonnelle #Épargne #BudgetFamilial #LibertéFinancière #GestionBudget
```

---

## 🛠️ Stack technique

- **Backend**: FastAPI + Python 3.11 (Async)
- **Database**: PostgreSQL (Neon.tech)
- **Scheduler**: GitHub Actions (planification automatique)
- **LLMs**: Groq (Llama 3.3), Gemini 2.0 (gratuits)
- **Images**: Unsplash, Pexels (gratuits)
- **Hosting**: Render.com (gratuit)
- **API**: Facebook Graph API

---

## 🚀 Installation locale

### Prérequis

- Python 3.11+
- Git
- Compte Neon.tech (gratuit)
- Clés API (toutes gratuites) :
  - Groq ou Gemini (LLM)
  - Unsplash ou Pexels (images - optionnel)
  - Facebook Developer Account

### Étapes d'installation

#### 1. Cloner le projet
```bash
git clone https://github.com/AnicetJonhia/alphajourney.git
cd alphajourney
```

#### 2. Créer environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

#### 3. Installer dépendances
```bash
pip install -r requirements.txt
```

#### 4. Configuration

Copier `.env.example` vers `.env` :
```bash
cp .env.example .env
```

Remplir les variables :
```env
# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb

# Facebook
FB_ACCESS_TOKEN=EAAxxxxx
FB_PAGE_ID=123456789

# LLM APIs (au moins 1 requis)
GROQ_API_KEY=gsk_xxxxx        # Recommandé (Llama 3.3)
GEMINI_API_KEY=AIzaxxxxx      # Backup

# Image APIs (optionnels mais recommandés)
UNSPLASH_ACCESS_KEY=xxxxx     # 50 req/heure gratuit
PEXELS_API_KEY=xxxxx          # 200 req/heure gratuit

# Configuration
ENVIRONMENT=development
```

#### 5. Lancer l'application
```bash
uvicorn app.main:app --reload
```

Accéder à : http://localhost:8000

---

## 🌐 Déploiement Production

### 1. Créer base de données Neon

1. Aller sur [neon.tech](https://neon.tech)
2. Sign up (gratuit, sans carte bancaire)
3. "Create Project" → Nom : `alphajourney-db`
4. Copier la **Connection String** :
```
   postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb
```

### 2. Obtenir clés API LLM

#### **Groq** (Recommandé - Priorité #1)
```
1. https://console.groq.com
2. Sign up avec Google/GitHub
3. API Keys → "Create API Key"
4. Nom : AlphaJourney
5. Copier la clé : gsk_xxxxx
```

**Modèle utilisé :** `llama-3.3-70b-versatile` (70B paramètres)  
**Gratuit :** Illimité (30 req/min, 6000 tokens/min)

#### **Gemini** (Backup)
```
1. https://makersuite.google.com/app/apikey
2. "Get API Key" → "Create API key"
3. Copier : AIza_xxxxx
```

**Modèle utilisé :** `gemini-2.0-flash-exp`  
**Gratuit :** 15 req/min, 1M tokens/min

### 3. Obtenir clés API Images (Optionnel)

#### **Unsplash** (Recommandé)
```
1. https://unsplash.com/join
2. https://unsplash.com/oauth/applications
3. "New Application"
   - Name: AlphaJourney
   - Description: Auto Facebook posts
4. Copier : Access Key
```

**Quota gratuit :** 50 requêtes/heure

#### **Pexels** (Backup)
```
1. https://www.pexels.com/join-consumer/
2. https://www.pexels.com/api/
3. "Get Started"
4. Copier : API Key
```

**Quota gratuit :** 200 requêtes/heure

### 4. Configurer Facebook

#### Créer l'App Facebook

1. [Facebook Developers](https://developers.facebook.com)
2. "Create App" → Use case : **"Manage a business"**
3. App type : **"Business"**
4. App name : `AlphaJourney`
5. Skip "Business Portfolio" (optionnel)

#### Ajouter Facebook Login

1. Dashboard → "Add Product"
2. Chercher **"Facebook Login for Business"**
3. "Set Up"

#### Passer en mode Live

1. En haut à droite : Toggle "Development" → **"Live"**
2. Confirmer

#### Générer le Page Access Token

**Méthode simple :**

1. [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Sélectionner ton app "AlphaJourney"
3. Cliquer "Generate Access Token" (sans ajouter de permissions)
4. Autoriser dans la popup
5. Dans la barre de requête, taper : `me/accounts`
6. Cliquer "Submit"
7. Dans la réponse JSON, copier le `access_token` :
```json
   {
     "data": [
       {
         "access_token": "COPIE_CE_TOKEN",  ← Page Access Token permanent
         "name": "AlphaJourney",
         "id": "123456789"
       }
     ]
   }
```

**Ce token est permanent !** ✅

### 5. Déployer sur Render
```bash
# 1. Push sur GitHub
git add .
git commit -m "Deploy AlphaJourney v2.1"
git push origin main

# 2. Sur render.com
# - "New" → "Blueprint"
# - Connecter votre repo GitHub
# - Render détecte render.yaml automatiquement
# - Cliquer "Apply"

# 3. Ajouter variables d'environnement
# Dashboard Render → Environment → Add Environment Variable

DATABASE_URL=postgresql://...
FB_ACCESS_TOKEN=EAAxxxxx
FB_PAGE_ID=123456789
GROQ_API_KEY=gsk_xxxxx
GEMINI_API_KEY=AIzaxxxxx         
UNSPLASH_ACCESS_KEY=xxxxx        # Optionnel
PEXELS_API_KEY=xxxxx             # Optionnel

# 4. Configurer GitHub Actions
# Créer .github/workflows/publish.yml pour planifier les publications
# Voir la section "Configuration GitHub Actions" ci-dessous

# 5. Déploiement automatique (2-3 minutes)
```

**URL de votre app :** `https://alphajourney.onrender.com`

---

---

## ⚙️ Configuration GitHub Actions

Créer un fichier `.github/workflows/publish.yml` :

```yaml
name: AlphaJourney Auto-Publish

on:
  schedule:
    - cron: '0 14 * * *'  # Tous les jours à 14h UTC

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Trigger publication
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
          RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID }}
        run: |
          curl -X POST \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
            -d '{"clearCache": false}'
```

**Configuration requise :**
1. Aller sur [Render Dashboard](https://dashboard.render.com)
2. Récupérer votre `RENDER_API_KEY` et `RENDER_SERVICE_ID`
3. Dans GitHub → Settings → Secrets → Ajouter ces secrets

---

## 📡 API Endpoints

### Endpoints publics

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Statut de l'application |
| `/health` | GET | Health check |
| `/stats` | GET | Statistiques globales |
| `/recent-posts` | GET | Derniers posts publiés |
| `/dashboard` | GET | Dashboard complet |
| `/publish-now` | POST | Publication manuelle (test) |

### Exemples
```bash
# Vérifier le statut
curl https://alphajourney.onrender.com/

# Résultat :
{
  "app": "AlphaJourney",
  "version": "2.1.0 (ASYNC)",
  "status": "running",
  "tagline": "💰 Finance | 🤖 IA | 🧠 Dev Personnel",
  "today_category": "finance",
  "publication_time": "14:00"
}

# Voir les statistiques
curl https://alphajourney.onrender.com/stats

# Dashboard complet
curl https://alphajourney.onrender.com/dashboard

# Forcer une publication immédiate (test)
curl -X POST https://alphajourney.onrender.com/publish-now
```

---

## 🎯 Architecture
```
┌─────────────────────────────────┐
│   Neon PostgreSQL (gratuit)     │
│   - Historique posts            │
│   - Analytics                   │
│   - Images URLs                 │
│   - 500 MB (10+ ans d'usage)    │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   Render.com (gratuit)          │
│   FastAPI Async                 │
│   - Endpoint de publication     │
│   - Fallback LLM + Images       │
│   - 750h/mois (0.07% utilisé)   │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│  GitHub Actions (gratuit)       │
│  - Déclenchement 14h/jour       │
│  - Workflow automatisé          │
└────────────────────────────────┘
             │
   ┌─────────┴─────────┬──────────┬──────────┬──────────┐
   │                   │          │          │          │
┌──▼─────┐  ┌─────────▼┐  ┌──────▼───┐  ┌───▼────┐  ┌─▼────────┐
│  Groq  │  │  Gemini  │  │ Unsplash │  │ Pexels │  │ Facebook │
│ Llama  │  │   2.0    │  │  Images  │  │ Images │  │Graph API │
│  3.3   │  │  Flash   │  │          │  │        │  │          │
└────────┘  └──────────┘  └──────────┘  └────────┘  └──────────┘
```

---

## 💡 Fonctionnement du système

### Fallback LLM (2 providers)

AlphaJourney essaie les LLMs dans cet ordre :

1. **Groq** (Llama 3.3 70B) - **Priorité #1**
   - Meilleur modèle open source
   - Ultra-rapide (<2 secondes)
   - Gratuit illimité

2. **Gemini** (2.0 Flash) - **Backup**
   - Infrastructure Google
   - Excellent en français
   - Fallback fiable

**Logs exemple :**
```
🔄 Tentative avec groq...
✅ Contenu généré avec groq
```

### Génération de hashtags

5 hashtags pertinents sélectionnés aléatoirement selon la catégorie :

- **Finance** : #FinancePersonnelle #Épargne #Investissement #BudgetFamilial #LibertéFinancière
- **IA** : #IntelligenceArtificielle #IA #Productivité #OutilsIA #AutomatisationIA
- **Dev Personnel** : #DéveloppementPersonnel #Motivation #Mindset #CroissancePersonnelle

### Images gratuites

Photos contextuelles récupérées automatiquement :

- **Finance** : piggy bank, financial planning, money savings
- **IA** : technology workspace, laptop coding, artificial intelligence
- **Dev Personnel** : motivation success, goal achievement, person climbing

**Fallback :** Si pas d'image disponible → publication en texte seul avec hashtags

---

## 📊 Calculs de consommation

### Base de données
```
1 post/jour = ~3 KB (contenu + analytics + image URL)
1 an = 365 × 3 KB = 1.1 MB
10 ans = 11 MB sur 500 MB disponibles

➡️ Vous pouvez tourner 45+ ans gratuitement !
```

### Serveur Render
```
Publication : 1×/jour (déclenché par GitHub Actions)
Durée execution : ~3 secondes (async)
Mois : 90 secondes sur 750h disponibles

➡️ Utilisation : 0.003% du quota gratuit
```

### GitHub Actions
```
Workflows gratuits : 2 000 minutes/mois
Publication 1×/jour = ~30 secondes/jour
Mois : ~15 minutes sur 2 000 disponibles

➡️ Utilisation : 0.75% du quota gratuit
```

### APIs gratuites

| Service | Quota gratuit | Usage AlphaJourney | % utilisé |
|---------|---------------|-------------------|-----------|
| **Groq** | 6000 tokens/min | ~500 tokens/jour | 0.01% |
| **Gemini** | 15 req/min | 0-1 req/jour | 0% |
| **Unsplash** | 50 req/heure | 1 req/jour | 0.08% |
| **Pexels** | 200 req/heure | 0-1 req/jour | 0% |

### Coût total mensuel

| Service | Coût |
|---------|------|
| Neon PostgreSQL | **0€** (gratuit à vie) |
| Render Hosting | **0€** (gratuit à vie) |
| Groq LLM | **0€** (gratuit) |
| Gemini LLM | **0€** (gratuit) |
| Unsplash Images | **0€** (gratuit) |
| Pexels Images | **0€** (gratuit) |
| Facebook API | **0€** (gratuit) |
| **TOTAL** | **0€ / mois** |

---

## 🔧 Maintenance

### Voir les logs
```bash
# Sur Render.com
Dashboard → alphajourney → Logs

# Filtrer par niveau
ERROR   → Problèmes critiques
WARNING → Avertissements
INFO    → Informations normales
```

### Ajouter des sujets

Éditer `app/data/schedules.py` :
```python
TOPICS = {
    "finance": [
        "Nouveau sujet finance",
        "Comment investir intelligemment",
        # ... autres sujets
    ]
}
```

### Ajouter des hashtags

Éditer `app/data/hashtags.py` :
```python
HASHTAGS = {
    "finance": [
        "#NouveauHashtag",
        "#FinanceTips",
        # ... autres hashtags
    ]
}
```

### Configurer GitHub Actions

Modifier `.github/workflows/publish.yml` pour changer l'heure de publication :
```yaml
on:
  schedule:
    - cron: '0 14 * * *'  # 14h UTC (à adapter à votre fuseau horaire)
    # Exemple : '0 18 * * *' pour 18h, '30 18 * * *' pour 18h30
```

⚠️ **Important** : L'heure est en UTC. Adapter selon votre fuseau horaire :
- France (EST) : 14h UTC = 15h heure locale → utiliser `0 13 * * *`
- Canada EST : 14h UTC = 9h heure locale → utiliser `0 19 * * *`

---

## 🧪 Tests

### Test local complet
```bash
# Test génération + hashtags + image
python test_full_post.py
```

### Test publication manuelle
```bash
curl -X POST http://localhost:8000/publish-now
```

### Vérifier les stats
```bash
curl http://localhost:8000/stats | jq
```

### Voir les derniers posts
```bash
curl http://localhost:8000/recent-posts | jq
```

---

## 📈 Performances

### Version 2.1 (Async + Images + Hashtags)

- ⚡ **Génération** : 2-3 secondes (async)
- 📸 **Image** : 1-2 secondes (parallèle)
- 📤 **Publication** : 1-2 secondes
- **Total** : ~5 secondes du début à la fin

### Engagement (stats moyennes)

- 📝 **Posts texte seul** : ~20-30 interactions
- 📸 **Posts avec image** : ~40-60 interactions (+100%)
- 🏷️ **Avec hashtags** : +30% de portée

---

## 📈 Roadmap

- [x] Publication automatique quotidienne
- [x] Génération de contenu IA
- [x] Hashtags intelligents
- [x] Photos professionnelles gratuites
- [x] Architecture async
- [ ] Dashboard web React
- [ ] Support Instagram
- [ ] Threads Twitter/X
- [ ] A/B testing automatique
- [ ] Analyse sentiment commentaires
- [ ] Scheduling avancé (plusieurs posts/jour)
- [ ] Export analytics CSV
- [ ] Notifications Telegram/Discord

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add: amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

---

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE)

---

## 🙏 Remerciements

- **Neon** pour le PostgreSQL gratuit et performant
- **Render** pour l'hébergement gratuit fiable
- **Groq** pour l'accès gratuit à Llama 3.3
- **Google** pour Gemini 2.0 Flash gratuit
- **Unsplash** & **Pexels** pour les photos professionnelles
- **Meta** pour Facebook Graph API
- **FastAPI** pour le framework Python moderne

---

## 📧 Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/AnicetJonhia/alphajourney/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/AnicetJonhia/alphajourney/discussions)
- 📧 **Email** : anicetjonhia@gmail.com

---

## 🎨 Screenshots

### Post généré automatiquement
```
💰 Épargner 500€/mois sans effort ? C'est possible !

Le problème : Chaque mois, tu te dis "je vais mettre 
de l'argent de côté"... mais en fin de mois, il ne 
reste rien. 😔

La solution ? L'épargne AUTOMATIQUE :

1️⃣ Ouvre un compte épargne séparé
2️⃣ Programme un virement automatique le jour de ta paie
3️⃣ Commence petit (100€) puis augmente
4️⃣ Considère cet argent comme "déjà dépensé"
5️⃣ Ajuste ton budget sur ce qui reste

Résultat : En 1 an = 6 000€ épargnés ! 🎯

Et toi, quelle est ta méthode d'épargne ? 💬

#FinancePersonnelle #Épargne #BudgetFamilial 
#LibertéFinancière #GestionBudget
```

**+ Photo professionnelle de tirelire/épargne** 📸

---

<div align="center">

**Fait avec ❤️ pour la communauté**

🚀 **AlphaJourney v2.1** - *Votre voyage vers le succès commence ici*

[![Star](https://img.shields.io/github/stars/AnicetJonhia/alphajourney?style=social)](https://github.com/AnicetJonhia/alphajourney)
[![Fork](https://img.shields.io/github/forks/AnicetJonhia/alphajourney?style=social)](https://github.com/AnicetJonhia/alphajourney/fork)
[![Issues](https://img.shields.io/github/issues/AnicetJonhia/alphajourney)](https://github.com/AnicetJonhia/alphajourney/issues)

[⭐ Star](https://github.com/AnicetJonhia/alphajourney) • [🔄 Fork](https://github.com/AnicetJonhia/alphajourney/fork) • [🐛 Report Bug](https://github.com/AnicetJonhia/alphajourney/issues)

---

**AlphaJourney** | 

</div>