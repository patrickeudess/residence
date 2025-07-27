import requests
import json

def test_proprietaire():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Test des fonctionnalités Propriétaire")
    print("=" * 50)
    
    # Créer une session
    session = requests.Session()
    
    try:
        # 1. Test de la page de connexion
        print("\n1️⃣ Test de la page de connexion...")
        response = session.get(f"{base_url}/proprietaire")
        if response.status_code == 200:
            print("✅ Page de connexion : OK")
        else:
            print(f"❌ Page de connexion : Erreur {response.status_code}")
        
        # 2. Test de la page d'inscription
        print("\n2️⃣ Test de la page d'inscription...")
        response = session.get(f"{base_url}/proprietaire/inscription")
        if response.status_code == 200:
            print("✅ Page d'inscription : OK")
        else:
            print(f"❌ Page d'inscription : Erreur {response.status_code}")
        
        # 3. Test de connexion (simulation)
        print("\n3️⃣ Test de connexion...")
        login_data = {
            'identifiant': 'test@example.com',
            'password': 'test123'
        }
        response = session.post(f"{base_url}/proprietaire", data=login_data)
        print(f"📊 Réponse connexion : {response.status_code}")
        
        # 4. Test des statistiques (sans connexion - devrait rediriger)
        print("\n4️⃣ Test des statistiques (sans connexion)...")
        response = session.get(f"{base_url}/proprietaire/statistiques")
        if response.status_code == 302:  # Redirection
            print("✅ Redirection correcte (non connecté)")
        else:
            print(f"⚠️ Statut inattendu : {response.status_code}")
        
        # 5. Test mes-résidences (sans connexion)
        print("\n5️⃣ Test mes-résidences (sans connexion)...")
        response = session.get(f"{base_url}/proprietaire/mes-residences")
        if response.status_code == 302:  # Redirection
            print("✅ Redirection correcte (non connecté)")
        else:
            print(f"⚠️ Statut inattendu : {response.status_code}")
        
        # 6. Test de l'API des résidences
        print("\n6️⃣ Test de l'API des résidences...")
        response = session.get(f"{base_url}/api/residences")
        if response.status_code == 200:
            residences = response.json()
            print(f"✅ API résidences : OK ({len(residences)} résidences)")
            
            # Vérifier les propriétaires
            proprietaires = set()
            for residence in residences:
                if 'proprietaire_id' in residence:
                    proprietaires.add(residence['proprietaire_id'])
            print(f"📊 {len(proprietaires)} propriétaires différents")
            
        else:
            print(f"❌ API résidences : Erreur {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 Tests propriétaire terminés !")
        print("💡 Pour tester les statistiques, connectez-vous d'abord")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests : {e}")

if __name__ == "__main__":
    test_proprietaire() 