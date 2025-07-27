from flask import Flask, render_template, request, jsonify, redirect, session # type: ignore
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'  # Clé secrète pour les sessions

# Charger les données des résidences depuis le fichier JSON
def load_residences():
    try:
        with open('residences.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Charger les comptes propriétaires
def load_proprietaires():
    try:
        with open('proprietaires.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Sauvegarder les comptes propriétaires
def save_proprietaires(proprietaires):
    try:
        with open('proprietaires.json', 'w', encoding='utf-8') as file:
            json.dump(proprietaires, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des propriétaires: {e}")
        return False

# Route principale
@app.route('/')
def index():
    residences = load_residences()
    
    # Récupérer les paramètres de filtrage depuis l'URL
    ville = request.args.get('ville', '')
    prix_min = request.args.get('prix_min', '')
    prix_max = request.args.get('prix_max', '')
    equipements = request.args.get('equipements', '')
    
    # Filtrer les résidences selon les critères
    filtered_residences = residences
    
    if ville:
        filtered_residences = [r for r in filtered_residences if ville.lower() in r['ville'].lower()]
    
    if prix_min:
        try:
            prix_min = int(prix_min)
            filtered_residences = [r for r in filtered_residences if r['prix'] >= prix_min]
        except ValueError:
            pass
    
    if prix_max:
        try:
            prix_max = int(prix_max)
            filtered_residences = [r for r in filtered_residences if r['prix'] <= prix_max]
        except ValueError:
            pass
    
    if equipements:
        equipements_list = [e.strip().lower() for e in equipements.split(',')]
        filtered_residences = [r for r in filtered_residences 
                            if any(eq in r['equipements'].lower() for eq in equipements_list)]
    
    # Récupérer la liste unique des villes pour le filtre
    villes = list(set([r['ville'] for r in residences]))
    villes.sort()
    
    return render_template('index.html', 
                         residences=filtered_residences,
                         all_residences=residences,
                         villes=villes,
                         filters={
                             'ville': ville,
                             'prix_min': prix_min,
                             'prix_max': prix_max,
                             'equipements': equipements
                         })

# Route API pour récupérer les résidences en JSON (pour la carte)
@app.route('/api/residences')
def api_residences():
    residences = load_residences()
    return jsonify(residences)

# Sauvegarder les résidences dans le fichier JSON
def save_residences(residences):
    try:
        with open('residences.json', 'w', encoding='utf-8') as file:
            json.dump(residences, file, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde: {e}")
        return False

def get_all_villes():
    """Retourne toutes les villes de la Côte d'Ivoire"""
    return [
        'Abidjan', 'Bouaké', 'Korhogo', 'Daloa', 'San-Pédro', 'Man', 'Gagnoa', 
        'Abengourou', 'Bondoukou', 'Yamoussoukro', 'Grand-Bassam', 'Bingerville', 
        'Anyama', 'Dabou', 'Agboville', 'Adzopé', 'Tiassalé', 'Séguéla', 'Divo', 
        'Ferkessédougou', 'Katiola', 'Soubré', 'Guiglo', 'Issia', 'Sassandra', 
        'Tabou', 'Odienné', 'Bouna', 'Tengrela', 'Boundiali', 'Kouto', 'M\'Batto', 
        'Aboisso', 'Agnibilékrou', 'Arrah', 'Bocanda', 'Daoukro', 'Méagui', 
        'Oumé', 'Sinfra', 'Vavoua', 'Zuenoula', 'Toumodi', 'Yakassé-Attobrou', 
        'Alépé', 'Bonoua', 'Jacqueville', 'Touba', 'Kong', 'Sakassou', 'Tanda', 
        'Tingrela', 'Biankouma', 'Danané', 'Kouibly', 'Sipilou', 'Buyo', 'Guéyo', 
        'Lakota', 'Oragahio', 'Ayamé', 'Bongouanou', 'Dimbokro', 'M\'Bahiakro', 
        'Prikro', 'Béoumi', 'Botro', 'Bouaflé', 'Zuénoula', 'Bangolo', 'Duékoué', 
        'Toulépleu', 'Bloléquin', 'Téapleu', 'Zagné'
    ]

# Route pour le formulaire d'ajout (fonctionnel)
@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_residence():
    message = ""
    message_type = ""
    form_data = {}
    
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            nom = request.form.get('nom', '').strip()
            ville = request.form.get('ville', '').strip()
            adresse = request.form.get('adresse', '').strip()
            prix = request.form.get('prix', '').strip()
            telephone = request.form.get('telephone', '').strip()
            description = request.form.get('description', '').strip()
            latitude = request.form.get('latitude', '').strip()
            longitude = request.form.get('longitude', '').strip()
            
            # Récupérer les équipements sélectionnés
            equipements_selectionnes = request.form.getlist('equipements')
            equipements = ', '.join(equipements_selectionnes) if equipements_selectionnes else ''
            
            # Validation des données
            if not nom or not ville or not prix:
                message = "Tous les champs obligatoires doivent être remplis."
                message_type = "danger"
            elif not prix.isdigit() or int(prix) <= 0:
                message = "Le prix doit être un nombre positif."
                message_type = "danger"
            elif telephone and telephone.strip() and (not telephone.replace(' ', '').isdigit() or len(telephone.replace(' ', '')) > 14):
                message = "Le numéro de téléphone doit contenir uniquement des chiffres et ne pas dépasser 14 caractères."
                message_type = "danger"
            elif request.form.get('telephone2', '').strip() and (not request.form.get('telephone2', '').strip().replace(' ', '').isdigit() or len(request.form.get('telephone2', '').strip().replace(' ', '')) > 14):
                message = "Le numéro de téléphone 2 doit contenir uniquement des chiffres et ne pas dépasser 14 caractères."
                message_type = "danger"
            else:
                # Charger les résidences existantes
                residences = load_residences()
                
                # Générer un nouvel ID
                max_id = max([r['id'] for r in residences]) if residences else 0
                new_id = max_id + 1
                
                # Créer la nouvelle résidence
                nouvelle_residence = {
                    "id": new_id,
                    "nom": nom,
                    "ville": ville,
                    "adresse": adresse,
                    "prix": int(prix),
                    "description": description,
                    "equipements": equipements,
                    "image": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400&h=300&fit=crop",  # Image par défaut
                    "telephone": telephone,
                    "telephone2": request.form.get('telephone2', '').strip(),
                    "latitude": float(latitude) if latitude else 0.0,
                    "longitude": float(longitude) if longitude else 0.0,
                    "disponible": True
                }
                
                # Ajouter la nouvelle résidence
                residences.append(nouvelle_residence)
                
                # Sauvegarder dans le fichier JSON
                if save_residences(residences):
                    message = f"Résidence '{nom}' ajoutée avec succès ! Elle est maintenant visible sur la carte."
                    message_type = "success"
                    form_data = {}  # Vider le formulaire
                else:
                    message = "Erreur lors de la sauvegarde. Veuillez réessayer."
                    message_type = "danger"
                    form_data = request.form.to_dict()
        
        except Exception as e:
            message = f"Erreur lors de l'ajout: {str(e)}"
            message_type = "danger"
            form_data = request.form.to_dict()
    
    # Récupérer toutes les villes de la Côte d'Ivoire
    villes_existantes = get_all_villes()
    villes_existantes.sort()
    
    return render_template('ajouter.html', 
                         message=message, 
                         message_type=message_type,
                         form_data=form_data,
                         villes_existantes=villes_existantes)

# Route pour supprimer une résidence
@app.route('/supprimer/<int:residence_id>', methods=['POST'])
def supprimer_residence(residence_id):
    # Vérifier si l'utilisateur est connecté
    if 'proprietaire_id' not in session:
        return jsonify({'success': False, 'message': 'Authentification requise'})
    
    residences = load_residences()
    
    # Trouver et supprimer la résidence
    for i, residence in enumerate(residences):
        if residence['id'] == residence_id:
            nom_residence = residence['nom']
            del residences[i]
            
            # Sauvegarder les modifications
            if save_residences(residences):
                return jsonify({'success': True, 'message': f'Résidence "{nom_residence}" supprimée avec succès'})
            else:
                return jsonify({'success': False, 'message': 'Erreur lors de la suppression'})
    
    return jsonify({'success': False, 'message': 'Résidence non trouvée'})

# Route pour éditer une résidence
@app.route('/editer/<int:residence_id>', methods=['GET', 'POST'])
def editer_residence(residence_id):
    # Vérifier si l'utilisateur est connecté
    if 'proprietaire_id' not in session:
        return redirect('/proprietaire')
    
    residences = load_residences()
    residence = None
    
    # Trouver la résidence à éditer
    for r in residences:
        if r['id'] == residence_id:
            residence = r
            break
    
    if not residence:
        return redirect('/')
    
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            nom = request.form.get('nom', '').strip()
            ville = request.form.get('ville', '').strip()
            adresse = request.form.get('adresse', '').strip()
            prix = request.form.get('prix', '').strip()
            telephone = request.form.get('telephone', '').strip()
            description = request.form.get('description', '').strip()
            latitude = request.form.get('latitude', '').strip()
            longitude = request.form.get('longitude', '').strip()
            
            # Récupérer les équipements sélectionnés
            equipements_selectionnes = request.form.getlist('equipements')
            equipements = ', '.join(equipements_selectionnes) if equipements_selectionnes else ''
            
            # Validation des données
            if not nom or not ville or not prix:
                message = "Tous les champs obligatoires doivent être remplis."
                message_type = "danger"
            elif not prix.isdigit() or int(prix) <= 0:
                message = "Le prix doit être un nombre positif."
                message_type = "danger"
            elif telephone and telephone.strip() and (not telephone.replace(' ', '').isdigit() or len(telephone.replace(' ', '')) > 14):
                message = "Le numéro de téléphone doit contenir uniquement des chiffres et ne pas dépasser 14 caractères."
                message_type = "danger"
            elif request.form.get('telephone2', '').strip() and (not request.form.get('telephone2', '').strip().replace(' ', '').isdigit() or len(request.form.get('telephone2', '').strip().replace(' ', '')) > 14):
                message = "Le numéro de téléphone 2 doit contenir uniquement des chiffres et ne pas dépasser 14 caractères."
                message_type = "danger"
            else:
                # Mettre à jour la résidence
                residence['nom'] = nom
                residence['ville'] = ville
                residence['adresse'] = adresse
                residence['prix'] = int(prix)
                residence['description'] = description
                residence['equipements'] = equipements
                residence['telephone'] = telephone
                residence['telephone2'] = request.form.get('telephone2', '').strip()
                residence['latitude'] = float(latitude) if latitude else 0.0
                residence['longitude'] = float(longitude) if longitude else 0.0
                
                # Sauvegarder les modifications
                if save_residences(residences):
                    message = f"Résidence '{nom}' modifiée avec succès !"
                    message_type = "success"
                    form_data = {}
                else:
                    message = "Erreur lors de la sauvegarde. Veuillez réessayer."
                    message_type = "danger"
                    form_data = request.form.to_dict()
        
        except Exception as e:
            message = f"Erreur lors de la modification: {str(e)}"
            message_type = "danger"
            form_data = request.form.to_dict()
    
    # Récupérer toutes les villes de la Côte d'Ivoire
    villes_existantes = get_all_villes()
    villes_existantes.sort()
    
    return render_template('editer.html', 
                         residence=residence,
                         message=message, 
                         message_type=message_type,
                         form_data=form_data,
                         villes_existantes=villes_existantes)

# Route pour l'espace propriétaire
@app.route('/proprietaire', methods=['GET', 'POST'])
def espace_proprietaire():
    message = ""
    message_type = ""
    
    if request.method == 'POST':
        # Récupérer les identifiants
        identifiant = request.form.get('identifiant', '').strip()  # Email ou téléphone
        password = request.form.get('password', '').strip()
        
        if not identifiant or not password:
            message = "Veuillez remplir tous les champs."
            message_type = "danger"
        else:
            # Charger les propriétaires
            proprietaires = load_proprietaires()
            
            # Chercher le propriétaire par email ou téléphone
            proprietaire_trouve = None
            for prop in proprietaires:
                if (prop.get('email') == identifiant or 
                    prop.get('telephone') == identifiant):
                    proprietaire_trouve = prop
                    break
            
            # Vérifier le mot de passe
            if proprietaire_trouve and proprietaire_trouve.get('mot_de_passe') == password:
                # Créer la session
                session['proprietaire_id'] = proprietaire_trouve['id']
                session['proprietaire_nom'] = proprietaire_trouve['nom']
                return redirect('/proprietaire/dashboard')
            else:
                message = "Identifiant ou mot de passe incorrect."
                message_type = "danger"
    
    return render_template('proprietaire/login.html', 
                         message=message, 
                         message_type=message_type)

# Dashboard propriétaire
@app.route('/proprietaire/dashboard')
def dashboard_proprietaire():
    # Vérifier si l'utilisateur est connecté
    if 'proprietaire_id' not in session:
        return redirect('/proprietaire')
    
    residences = load_residences()
    
    # Statistiques simulées
    stats = {
        'total_residences': len(residences),
        'residences_actives': len([r for r in residences if r.get('disponible', True)]),
        'vues_total': sum([r.get('vues', 0) for r in residences]),
        'contacts_total': sum([r.get('contacts', 0) for r in residences]),
        'prix_moyen': sum([r.get('prix', 0) for r in residences]) // len(residences) if residences else 0
    }
    
    return render_template('proprietaire/dashboard.html', 
                         residences=residences,
                         stats=stats,
                         proprietaire_nom=session.get('proprietaire_nom'))

# Route de déconnexion
@app.route('/proprietaire/deconnexion')
def deconnexion_proprietaire():
    session.clear()
    return redirect('/proprietaire')

# Gérer les résidences du propriétaire
@app.route('/proprietaire/mes-residences')
def mes_residences():
    # Vérifier si l'utilisateur est connecté
    if 'proprietaire_id' not in session:
        return redirect('/proprietaire')
    
    residences = load_residences()
    
    # Filtrer les résidences du propriétaire connecté
    proprietaire_id = session.get('proprietaire_id')
    residences_proprietaire = [r for r in residences if r.get('proprietaire_id') == proprietaire_id]
    
    return render_template('proprietaire/mes_residences.html', 
                         residences=residences_proprietaire)

# Ajouter une résidence (version propriétaire)
@app.route('/proprietaire/ajouter-residence', methods=['GET', 'POST'])
def ajouter_residence_proprietaire():
    message = ""
    message_type = ""
    form_data = {}
    
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            nom = request.form.get('nom', '').strip()
            ville = request.form.get('ville', '').strip()
            adresse = request.form.get('adresse', '').strip()
            prix = request.form.get('prix', '').strip()
            telephone = request.form.get('telephone', '').strip()
            description = request.form.get('description', '').strip()
            latitude = request.form.get('latitude', '').strip()
            longitude = request.form.get('longitude', '').strip()
            
            # Récupérer les équipements sélectionnés
            equipements_selectionnes = request.form.getlist('equipements')
            equipements = ', '.join(equipements_selectionnes) if equipements_selectionnes else ''
            
            # Validation des données
            if not nom or not ville or not prix:
                message = "Tous les champs obligatoires doivent être remplis."
                message_type = "danger"
            elif not prix.isdigit() or int(prix) <= 0:
                message = "Le prix doit être un nombre positif."
                message_type = "danger"
            elif telephone and telephone.strip() and (not telephone.replace(' ', '').isdigit() or len(telephone.replace(' ', '')) > 14):
                message = "Le numéro de téléphone doit contenir uniquement des chiffres et ne pas dépasser 14 caractères."
                message_type = "danger"
            elif request.form.get('telephone2', '').strip() and (not request.form.get('telephone2', '').strip().replace(' ', '').isdigit() or len(request.form.get('telephone2', '').strip().replace(' ', '')) > 14):
                message = "Le numéro de téléphone 2 doit contenir uniquement des chiffres et ne pas dépasser 14 caractères."
                message_type = "danger"
            else:
                # Charger les résidences existantes
                residences = load_residences()
                
                # Générer un nouvel ID
                max_id = max([r['id'] for r in residences]) if residences else 0
                new_id = max_id + 1
                
                # Créer la nouvelle résidence
                nouvelle_residence = {
                    "id": new_id,
                    "nom": nom,
                    "ville": ville,
                    "adresse": adresse,
                    "prix": int(prix),
                    "description": description,
                    "equipements": equipements,
                    "image": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400&h=300&fit=crop",
                    "telephone": telephone,
                    "telephone2": request.form.get('telephone2', '').strip(),
                    "latitude": float(latitude) if latitude else 0.0,
                    "longitude": float(longitude) if longitude else 0.0,
                    "disponible": True,
                    "proprietaire_id": session.get('proprietaire_id', 1),  # Utiliser l'ID du propriétaire connecté
                    "date_creation": datetime.now().strftime("%Y-%m-%d"),
                    "vues": 0,
                    "contacts": 0
                }
                
                # Ajouter la nouvelle résidence
                residences.append(nouvelle_residence)
                
                # Sauvegarder dans le fichier JSON
                if save_residences(residences):
                    message = f"Résidence '{nom}' ajoutée avec succès !"
                    message_type = "success"
                    form_data = {}
                else:
                    message = "Erreur lors de la sauvegarde. Veuillez réessayer."
                    message_type = "danger"
                    form_data = request.form.to_dict()
        
        except Exception as e:
            message = f"Erreur lors de l'ajout: {str(e)}"
            message_type = "danger"
            form_data = request.form.to_dict()
    
    # Récupérer toutes les villes de la Côte d'Ivoire
    villes_existantes = get_all_villes()
    villes_existantes.sort()
    
    return render_template('proprietaire/ajouter_residence.html', 
                         message=message, 
                         message_type=message_type,
                         form_data=form_data,
                         villes_existantes=villes_existantes)

# Statistiques détaillées
@app.route('/proprietaire/statistiques')
def statistiques_proprietaire():
    try:
        # Vérifier si l'utilisateur est connecté
        if 'proprietaire_id' not in session:
            # Temporairement, utiliser un propriétaire par défaut pour les tests
            session['proprietaire_id'] = 1
            session['proprietaire_nom'] = 'Propriétaire Test'
        
        residences = load_residences()
        
        # Filtrer les résidences du propriétaire connecté
        proprietaire_id = session.get('proprietaire_id')
        residences_proprietaire = [r for r in residences if r.get('proprietaire_id') == proprietaire_id]
        
        # Statistiques simplifiées
        stats_detaillees = {
            'total_residences': len(residences_proprietaire),
            'residences_par_ville': {},
            'prix_moyen_par_ville': {},
            'prix_total': 0,
            'prix_moyen': 0
        }
        
        for residence in residences_proprietaire:
            ville = residence.get('ville', 'Inconnue')
            prix = residence.get('prix', 0)
            
            # Compter par ville
            if ville not in stats_detaillees['residences_par_ville']:
                stats_detaillees['residences_par_ville'][ville] = 0
            stats_detaillees['residences_par_ville'][ville] += 1
            
            # Prix moyen par ville
            if ville not in stats_detaillees['prix_moyen_par_ville']:
                stats_detaillees['prix_moyen_par_ville'][ville] = []
            stats_detaillees['prix_moyen_par_ville'][ville].append(prix)
            
            # Calculer le prix total
            stats_detaillees['prix_total'] += prix
        
        # Calculer les prix moyens
        if residences_proprietaire:
            stats_detaillees['prix_moyen'] = stats_detaillees['prix_total'] // len(residences_proprietaire)
            
            for ville, prix_list in stats_detaillees['prix_moyen_par_ville'].items():
                if prix_list:
                    stats_detaillees['prix_moyen_par_ville'][ville] = sum(prix_list) // len(prix_list)
        
        return render_template('proprietaire/statistiques.html', 
                             stats=stats_detaillees,
                             residences=residences_proprietaire)
    
    except Exception as e:
        print(f"Erreur dans statistiques_proprietaire: {e}")
        import traceback
        traceback.print_exc()
        return f"Erreur: {str(e)}", 500

@app.route('/proprietaire/inscription', methods=['GET', 'POST'])
def inscription_proprietaire():
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip()
        telephone = request.form.get('telephone', '').strip()
        mot_de_passe = request.form.get('mot_de_passe', '').strip()
        confirmation_mot_de_passe = request.form.get('confirmation_mot_de_passe', '').strip()
        
        # Validation
        errors = []
        
        if not nom:
            errors.append("Le nom est obligatoire")
        
        # Au moins email OU téléphone doit être fourni
        if not email and not telephone:
            errors.append("Vous devez fournir au moins un email ou un numéro de téléphone")
        
        if email and '@' not in email:
            errors.append("Format d'email invalide")
        
        if telephone and not telephone.startswith('225'):
            errors.append("Le numéro doit commencer par 225")
        elif telephone and (len(telephone) < 13 or len(telephone) > 15):
            errors.append("Le numéro doit contenir 225 + 10 à 12 chiffres")
        
        if not mot_de_passe:
            errors.append("Le mot de passe est obligatoire")
        elif len(mot_de_passe) < 6:
            errors.append("Le mot de passe doit contenir au moins 6 caractères")
        
        if mot_de_passe != confirmation_mot_de_passe:
            errors.append("Les mots de passe ne correspondent pas")
        
        if errors:
            return render_template('proprietaire/inscription.html', 
                                 errors=errors,
                                 form_data=request.form)
        
        # Vérifier si le compte existe déjà
        proprietaires = load_proprietaires()
        
        # Vérifier par email
        if email:
            for prop in proprietaires:
                if prop.get('email') == email:
                    errors.append("Un compte avec cet email existe déjà")
                    return render_template('proprietaire/inscription.html', 
                                         errors=errors,
                                         form_data=request.form)
        
        # Vérifier par téléphone
        if telephone:
            for prop in proprietaires:
                if prop.get('telephone') == telephone:
                    errors.append("Un compte avec ce numéro de téléphone existe déjà")
                    return render_template('proprietaire/inscription.html', 
                                         errors=errors,
                                         form_data=request.form)
        
        # Créer le nouveau compte
        nouveau_proprietaire = {
            "id": len(proprietaires) + 1,
            "nom": nom,
            "email": email,
            "telephone": telephone,
            "mot_de_passe": mot_de_passe,  # En production, hasher le mot de passe
            "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        proprietaires.append(nouveau_proprietaire)
        
        if save_proprietaires(proprietaires):
            success_message = "Compte créé avec succès ! Vous pouvez maintenant vous connecter."
            return render_template('proprietaire/inscription.html', 
                                 success_message=success_message)
        else:
            errors.append("Erreur lors de la création du compte. Veuillez réessayer.")
            return render_template('proprietaire/inscription.html', 
                                 errors=errors,
                                 form_data=request.form)
    
    return render_template('proprietaire/inscription.html')

# Route de test pour simuler une connexion propriétaire
@app.route('/test-login/<int:proprietaire_id>')
def test_login(proprietaire_id):
    session['proprietaire_id'] = proprietaire_id
    session['proprietaire_nom'] = f'Propriétaire {proprietaire_id}'
    return redirect('/proprietaire/statistiques')

# Route de test pour les statistiques (sans authentification)
@app.route('/test-statistiques')
def test_statistiques():
    residences = load_residences()
    
    # Simuler un propriétaire connecté
    proprietaire_id = 1
    residences_proprietaire = [r for r in residences if r.get('proprietaire_id') == proprietaire_id]
    
    # Statistiques détaillées pour le propriétaire
    stats_detaillees = {
        'total_residences': len(residences_proprietaire),
        'residences_par_ville': {},
        'prix_moyen_par_ville': {},
        'equipements_populaires': {},
        'evolution_mensuelle': {},
        'prix_total': 0,
        'prix_moyen': 0
    }
    
    for residence in residences_proprietaire:
        ville = residence.get('ville', 'Inconnue')
        prix = residence.get('prix', 0)
        equipements = residence.get('equipements', '').split(', ')
        
        # Compter par ville
        if ville not in stats_detaillees['residences_par_ville']:
            stats_detaillees['residences_par_ville'][ville] = 0
        stats_detaillees['residences_par_ville'][ville] += 1
        
        # Prix moyen par ville
        if ville not in stats_detaillees['prix_moyen_par_ville']:
            stats_detaillees['prix_moyen_par_ville'][ville] = []
        stats_detaillees['prix_moyen_par_ville'][ville].append(prix)
        
        # Équipements populaires
        for equipement in equipements:
            if equipement:
                if equipement not in stats_detaillees['equipements_populaires']:
                    stats_detaillees['equipements_populaires'][equipement] = 0
                stats_detaillees['equipements_populaires'][equipement] += 1
        
        # Calculer le prix total
        stats_detaillees['prix_total'] += prix
    
    # Calculer les prix moyens
    if residences_proprietaire:
        stats_detaillees['prix_moyen'] = stats_detaillees['prix_total'] // len(residences_proprietaire)
        
        for ville, prix_list in stats_detaillees['prix_moyen_par_ville'].items():
            stats_detaillees['prix_moyen_par_ville'][ville] = sum(prix_list) // len(prix_list)
    
    return render_template('proprietaire/statistiques.html', 
                         stats=stats_detaillees,
                         residences=residences_proprietaire)

if __name__ == '__main__':
    # Configuration pour la production
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port) 