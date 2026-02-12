# 🚀 AlphaJourney

**Publication automatique quotidienne sur Facebook avec génération de contenu IA**

> 💰 Finance Personnelle • 🤖 IA & Productivité • 🧠 Développement Personnel

---

## ✨ Fonctionnalités

- ✅ **Publication automatique** à 14h chaque jour
- ✅ **3 LLMs gratuits** avec fallback intelligent (Gemini → Groq → Mistral)
- ✅ **Évite les répétitions** de sujets (30 jours de mémoire)
- ✅ **Analytics automatiques** des performances des posts
- ✅ **Base PostgreSQL** pour historique et optimisation
- ✅ **Clean Architecture** modulaire et maintenable
- ✅ **100% gratuit** (Neon + Render)

---

## 📊 Stratégie de contenu

### Calendrier hebdomadaire

| Jour | Catégorie | Focus |
|------|-----------|-------|
| **Lundi** | 💰 Finance | Conseils pratiques d'épargne/investissement |
| **Mardi** | 🤖 IA | Outils IA gratuits pour productivité |
| **Mercredi** | 🧠 Dev Personnel | Mindset et habitudes gagnantes |
| **Jeudi** | 💰 Finance | Stratégies financières avancées |
| **Vendredi** | 🤖 IA | Tutoriels IA rapides |
| **Samedi** | 🧠 Dev Personnel | Citations motivantes + actions |
| **Dimanche** | 📖 Thread | Success stories inspirantes |

### Mix de contenu

- **40%** Finance personnelle (épargne, investissement, budget)
- **30%** IA & Productivité (outils, automatisation)
- **30%** Développement personnel (mindset, habitudes)

---

## 🛠️ Stack technique

- **Backend**: FastAPI + Python 3
- **Database**: PostgreSQL (Neon.tech)
- **Scheduler**: APScheduler
- **LLMs**: Gemini, Groq, Mistral (gratuits)
- **Hosting**: Render.com (gratuit)
- **API**: Facebook Graph API

---

## 🚀 Installation locale

### Prérequis

- Python 3.11+
- Git
- Compte Neon.tech (gratuit)
- Clés API LLM (gratuit)
- Facebook Developer Account

### Étapes d'installation

#### 1. Cloner le projet
```bash
git clone https://github.com/votre-user/alphajourney.git
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
# Database
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb

# Facebook
FB_ACCESS_TOKEN=EAAxxxxx
FB_PAGE_ID=123456789

# LLM APIs (au moins 1 requis)
GEMINI_API_KEY=AIzaxxxxx
GROQ_API_KEY=gsk_xxxxx
MISTRAL_API_KEY=xxxxx

# Configuration
PUBLICATION_HOUR=14
PUBLICATION_MINUTE=0
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
2. Sign up (gratuit, pas de CB)
3. "Create Project" → Nom : `alphajourney-db`
4. Copier la **Connection String** :
```
   postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb
```

### 2. Obtenir clés API LLM

#### **Gemini (Google)** - Recommandé
```
1. https://makersuite.google.com/app/apikey
2. "Get API Key" → "Create API key"
3. Copier la clé
```

#### **Groq** - Très rapide
```
1. https://console.groq.com
2. Sign up
3. "Create API Key"
4. Copier
```

#### **Mistral** - Alternative
```
1. https://console.mistral.ai
2. Sign up
3. "Create new key"
4. Copier
```

### 3. Configurer Facebook

1. [Facebook Developers](https://developers.facebook.com)
2. Créer une App → Type "Business"
3. Ajouter produit **"Facebook Login for Business"**
4. Dans Settings → Basic, copier **App ID** et **App Secret**
5. Tools → Graph API Explorer :
   - Sélectionner votre App
   - Permissions : `pages_manage_posts`, `pages_read_engagement`
   - Générer **Page Access Token**
6. Copier **Page ID** depuis votre page Facebook

### 4. Déployer sur Render
```bash
# 1. Push sur GitHub
git add .
git commit -m "Initial AlphaJourney deployment"
git push origin main

# 2. Sur render.com
# - "New" → "Blueprint"
# - Connecter votre repo GitHub
# - Render détecte automatiquement render.yaml
# - Cliquer "Apply"

# 3. Ajouter variables d'environnement
# Dans le dashboard Render, onglet "Environment" :
DATABASE_URL=postgresql://...
FB_ACCESS_TOKEN=EAAxxxxx
FB_PAGE_ID=123456789
GEMINI_API_KEY=AIzaxxxxx
GROQ_API_KEY=gsk_xxxxx
MISTRAL_API_KEY=xxxxx

# 4. Déploiement automatique !
```

URL de votre app : `https://alphajourney.onrender.com`

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

# Voir les statistiques
curl https://alphajourney.onrender.com/stats

# Dashboard complet
curl https://alphajourney.onrender.com/dashboard

# Forcer une publication (test)
curl -X POST https://alphajourney.onrender.com/publish-now
```

---

## 🎯 Architecture
```
┌─────────────────────────────────┐
│   Neon PostgreSQL (gratuit)     │
│   - Historique posts            │
│   - Analytics                   │
│   - 500 MB (10+ ans d'usage)    │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│   Render.com (gratuit)          │
│   FastAPI + APScheduler         │
│   - Publication 14h/jour        │
│   - Fallback LLM intelligent    │
│   - 750h/mois (largement OK)    │
└────────────┬────────────────────┘
             │
      ┌──────┴──────┬──────────┬──────────┐
      │             │          │          │
┌─────▼─────┐ ┌────▼────┐ ┌───▼────┐ ┌───▼─────┐
│  Gemini   │ │  Groq   │ │Mistral │ │Facebook │
│  (LLM 1)  │ │ (LLM 2) │ │(LLM 3) │ │Graph API│
└───────────┘ └─────────┘ └────────┘ └─────────┘
```

---

## 💡 Fonctionnement du Fallback LLM

AlphaJourney essaie les LLMs dans cet ordre :

1. **Gemini** (Google) - Priorité 1
   - Gratuit, performant, bien structuré
   
2. **Groq** (Meta Llama) - Priorité 2
   - Ultra-rapide, gratuit
   
3. **Mistral** - Priorité 3
   - Alternative française

Si un LLM échoue, le suivant est automatiquement utilisé.

**Log exemple :**
```
🔄 Tentative avec gemini...
✅ Contenu généré avec gemini
```

---

## 📊 Calculs de consommation

### Base de données
```
1 post/jour = ~2 KB (contenu + analytics)
1 an = 365 × 2 KB = 730 KB
10 ans = 7.3 MB sur 500 MB disponibles

➡️ Vous pouvez tourner 68+ ans gratuitement !
```

### Serveur Render
```
Publication : 1×/jour à 14h
Durée execution : ~1 minute
Mois : 30 minutes sur 750h disponibles

➡️ Utilisation : 0.07% du quota gratuit
```

### Coût total

| Service | Coût mensuel |
|---------|--------------|
| Neon PostgreSQL | 0€ (gratuit à vie) |
| Render Hosting | 0€ (gratuit à vie) |
| LLMs (Gemini/Groq/Mistral) | 0€ (gratuits) |
| Facebook API | 0€ (gratuit) |
| **TOTAL** | **0€** |

---

## 🔧 Maintenance

### Voir les logs
```bash
# Sur Render.com, onglet "Logs"
# Ou en local :
tail -f logs/alphajourney.log
```

### Ajouter des sujets

Éditer `app/data/schedules.py` :
```python
TOPICS = {
    "finance": [
        "Nouveau sujet finance",
        # ... autres sujets
    ]
}
```

### Changer l'heure de publication

Modifier `.env` :
```env
PUBLICATION_HOUR=18  # Publier à 18h au lieu de 14h
```

---

## 🧪 Tests

### Test local de publication
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

## 📈 Roadmap

- [ ] Dashboard web React
- [ ] Support Instagram
- [ ] Génération d'images avec DALL-E
- [ ] A/B testing automatique
- [ ] Analyse sentiment commentaires
- [ ] Scheduling avancé (plusieurs posts/jour)
- [ ] Export analytics CSV

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

---

## 📝 Licence

MIT License - Voir [LICENSE](LICENSE)

---

## 🙏 Remerciements

- **Neon** pour le PostgreSQL gratuit
- **Render** pour l'hébergement gratuit
- **Google, Groq, Mistral** pour les LLMs gratuits
- **FastAPI** pour le framework Python

---

## 📧 Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/votre-user/alphajourney/issues)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/votre-user/alphajourney/discussions)
- 📧 **Email** : support@alphajourney.com

---

<div align="center">

**Fait avec ❤️ pour la communauté**

🚀 **AlphaJourney** - *Votre voyage vers le succès commence ici*

[⭐ Star](https://github.com/votre-user/alphajourney) • [🔄 Fork](https://github.com/votre-user/alphajourney/fork) • [🐛 Report Bug](https://github.com/votre-user/alphajourney/issues)

</div>