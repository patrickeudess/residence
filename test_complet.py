import requests
import json
import time

def test_application():
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 Test de l'application Résidence CI+")
    print("=" * 50)
    
    try:
        # Test 1: Page d'accueil
        print("\n1️⃣ Test de la page d'accueil...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Page d'accueil : OK")
        else:
            print(f"❌ Page d'accueil : Erreur {response.status_code}")
        
        # Test 2: Page de connexion propriétaire
        print("\n2️⃣ Test de la page de connexion...")
        response = requests.get(f"{base_url}/proprietaire")
        if response.status_code == 200:
            print("✅ Page de connexion : OK")
        else:
            print(f"❌ Page de connexion : Erreur {response.status_code}")
        
        # Test 3: Page d'inscription
        print("\n3️⃣ Test de la page d'inscription...")
        response = requests.get(f"{base_url}/proprietaire/inscription")
        if response.status_code == 200:
            print("✅ Page d'inscription : OK")
        else:
            print(f"❌ Page d'inscription : Erreur {response.status_code}")
        
        # Test 4: API des résidences
        print("\n4️⃣ Test de l'API des résidences...")
        response = requests.get(f"{base_url}/api/residences")
        if response.status_code == 200:
            try:
                residences = response.json()
                print(f"✅ API résidences : OK ({len(residences)} résidences)")
            except:
                print("❌ API résidences : Erreur de format JSON")
        else:
            print(f"❌ API résidences : Erreur {response.status_code}")
        
        # Test 5: Filtres
        print("\n5️⃣ Test des filtres...")
        response = requests.get(f"{base_url}/?ville=Abidjan&prix_min=50000")
        if response.status_code == 200:
            print("✅ Filtres : OK")
        else:
            print(f"❌ Filtres : Erreur {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 Tests terminés avec succès !")
        print(f"🌐 Application accessible sur : {base_url}")
        print("📱 Prêt pour le déploiement sur mobile !")
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'application")
        print("💡 Assurez-vous que l'application est démarrée avec : python app.py")
    except Exception as e:
        print(f"❌ Erreur lors des tests : {e}")

if __name__ == "__main__":
    test_application() 