# Résidence CI+ 🏠

Une application web pour référencer les résidences meublées des villes secondaires de Côte d'Ivoire.

## 🎯 Fonctionnalités

### Côté utilisateur
- **Moteur de recherche** : Filtrage par ville, prix, équipements
- **Carte interactive** : Visualisation des résidences sur OpenStreetMap
- **Liste des résidences** : Affichage en grille avec photos et informations
- **Contact WhatsApp** : Lien direct vers WhatsApp pour chaque résidence
- **Interface responsive** : Optimisée pour mobile et desktop

### Côté propriétaire (simulation)
- **Formulaire d'ajout** : Interface pour ajouter de nouvelles résidences
- **Gestion des équipements** : WiFi, climatisation, parking, etc.

## 🚀 Installation et lancement

### Prérequis
- Python 3.7 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   # Si vous avez Git
   git clone [URL_DU_REPO]
   cd residence
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

4. **Accéder à l'application**
   Ouvrez votre navigateur et allez sur : `http://localhost:5000`

## 📁 Structure du projet

```
residence/
├── app.py                 # Application Flask principale
├── residences.json        # Données des résidences (JSON)
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation
├── templates/
│   ├── index.html        # Page principale
│   └── ajouter.html      # Formulaire d'ajout
└── static/
    └── css/
        └── style.css     # Styles personnalisés
```

## 🛠️ Technologies utilisées

- **Backend** : Python Flask
- **Frontend** : HTML5, CSS3, Bootstrap 5
- **Carte** : Leaflet.js avec OpenStreetMap
- **Icônes** : Font Awesome
- **Données** : JSON (simulation de base de données)

## 📊 Données incluses

L'application inclut des résidences simulées pour les villes suivantes :
- Bouaké
- Korhogo
- Daloa
- San-Pédro
- Man
- Gagnoa
- Abengourou
- Bondoukou

Chaque résidence contient :
- Nom et description
- Ville et adresse
- Prix mensuel
- Équipements disponibles
- Photo
- Coordonnées GPS
- Numéro WhatsApp

## 🔧 Configuration

### Ajouter de nouvelles résidences
1. Éditez le fichier `residences.json`
2. Ajoutez une nouvelle entrée avec le format :
   ```json
   {
     "id": [ID_UNIQUE],
     "nom": "Nom de la résidence",
     "ville": "Nom de la ville",
     "adresse": "Adresse complète",
     "prix": [PRIX_EN_FCFA],
     "description": "Description de la résidence",
     "equipements": "WiFi, Climatisation, Parking, etc.",
     "image": "URL_DE_L_IMAGE",
     "telephone": "22507012345",
     "latitude": [LATITUDE],
     "longitude": [LONGITUDE],
     "disponible": true
   }
   ```

### Personnaliser le style
- Éditez `static/css/style.css` pour modifier l'apparence
- Les styles Bootstrap peuvent être surchargés

## 🚀 Déploiement

### En local (développement)
```bash
python app.py
```

### En production
Pour un déploiement en production, utilisez un serveur WSGI comme Gunicorn :
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔮 Évolutions futures

- [ ] Base de données PostgreSQL/MySQL
- [ ] Système d'authentification
- [ ] Upload d'images
- [ ] Système de réservation
- [ ] Notifications par email/SMS
- [ ] API REST pour applications mobiles
- [ ] Système de paiement en ligne
- [ ] Gestion des avis et notes

## 📞 Support

Pour toute question ou suggestion :
- Créez une issue sur GitHub
- Contactez l'équipe de développement

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

**Résidence CI+** - Votre partenaire immobilier en Côte d'Ivoire 🇨🇮 