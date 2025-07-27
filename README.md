# 🏠 Résidence CI+ - Plateforme de Location

Application web Flask pour la gestion et la location de résidences en Côte d'Ivoire.

## 🚀 Déploiement Rapide

### Option 1: Render (Recommandé - Gratuit)

1. **Créez un compte** sur [Render.com](https://render.com)
2. **Connectez votre GitHub** et sélectionnez ce repository
3. **Cliquez sur "New Web Service"**
4. **Configurez** :
   - **Name**: `residence-ci-plus`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. **Cliquez sur "Create Web Service"**

**Votre site sera disponible en 2-3 minutes !**

### Option 2: Railway (Alternative - Gratuit)

1. **Créez un compte** sur [Railway.app](https://railway.app)
2. **Connectez votre GitHub** et sélectionnez ce repository
3. **Cliquez sur "Deploy Now"**
4. **Attendez 2-3 minutes** pour le déploiement

### Option 3: Heroku (Payant)

1. **Créez un compte** sur [Heroku.com](https://heroku.com)
2. **Installez Heroku CLI** et connectez-vous
3. **Exécutez** :
   ```bash
   heroku create votre-app-name
   git push heroku main
   ```

## 📱 Accès Mobile

Une fois déployé, votre application sera accessible :
- **Ordinateur** : `https://votre-app.render.com`
- **Téléphone** : Même URL, responsive design
- **Partout** : 24h/24, 7j/7

## 🔧 Fonctionnalités

### 👥 **Espace Visiteurs**
- ✅ **Recherche** par ville et prix
- ✅ **Carte interactive** avec localisation
- ✅ **Filtres avancés** (équipements, disponibilité)
- ✅ **Détails complets** des résidences

### 👨‍💼 **Espace Propriétaires**
- ✅ **Dashboard** avec vue d'ensemble
- ✅ **Mes Résidences** - Gestion personnelle
- ✅ **Ajouter Résidence** - Formulaire complet
- ✅ **Statistiques** - Métriques détaillées
- ✅ **Sécurité** - Accès restreint aux propriétaires

## 🛠️ Installation Locale

```bash
# Cloner le repository
git clone https://github.com/votre-username/residence.git
cd residence

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py

# Accéder à http://127.0.0.1:5000
```

## 📊 Technologies Utilisées

- **Backend** : Flask (Python)
- **Frontend** : HTML5, CSS3, Bootstrap 5
- **Base de données** : JSON (fichiers)
- **Carte** : Leaflet.js
- **Icons** : Font Awesome
- **Déploiement** : Render/Railway/Heroku

## 🔒 Sécurité

- ✅ **Authentification** propriétaire
- ✅ **Filtrage** par propriétaire
- ✅ **Validation** des données
- ✅ **Protection** contre les injections

## 📞 Support

Pour toute question ou problème :
- **Email** : support@residence-ci.com
- **GitHub** : Ouvrir une issue

---

**Développé avec ❤️ pour la Côte d'Ivoire** 