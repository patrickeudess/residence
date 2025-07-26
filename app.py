from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Charger les données des résidences depuis le fichier JSON
def load_residences():
    try:
        with open('residences.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

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
    try:
        residences = load_residences()
        residences = [r for r in residences if r['id'] != residence_id]
        
        if save_residences(residences):
            return jsonify({"success": True, "message": "Résidence supprimée avec succès"})
        else:
            return jsonify({"success": False, "message": "Erreur lors de la suppression"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Erreur: {str(e)}"})

# Route pour éditer une résidence
@app.route('/editer/<int:residence_id>', methods=['GET', 'POST'])
def editer_residence(residence_id):
    residences = load_residences()
    residence = next((r for r in residences if r['id'] == residence_id), None)
    
    if not residence:
        return "Résidence non trouvée", 404
    
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
                residence.update({
                    "nom": nom,
                    "ville": ville,
                    "adresse": adresse,
                    "prix": int(prix),
                    "description": description,
                    "equipements": equipements,
                    "telephone": telephone,
                    "telephone2": request.form.get('telephone2', '').strip(),
                    "latitude": float(latitude) if latitude else 0.0,
                    "longitude": float(longitude) if longitude else 0.0,
                })
                
                # Sauvegarder les modifications
                if save_residences(residences):
                    message = f"Résidence '{nom}' modifiée avec succès !"
                    message_type = "success"
                else:
                    message = "Erreur lors de la sauvegarde. Veuillez réessayer."
                    message_type = "danger"
                
                return render_template('editer.html', 
                                     residence=residence,
                                     message=message,
                                     message_type=message_type,
                                     villes_existantes=get_all_villes())
        
        except Exception as e:
            message = f"Erreur lors de la modification: {str(e)}"
            message_type = "danger"
    
    return render_template('editer.html', 
                         residence=residence,
                         villes_existantes=get_all_villes())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 