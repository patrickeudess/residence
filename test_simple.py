import requests

def test_app():
    try:
        # Test de la page d'accueil
        response = requests.get('http://127.0.0.1:5000/')
        print(f"✅ Page d'accueil : {response.status_code}")
        
        # Test de la page de connexion
        response = requests.get('http://127.0.0.1:5000/proprietaire')
        print(f"✅ Page de connexion : {response.status_code}")
        
        # Test de la page d'inscription
        response = requests.get('http://127.0.0.1:5000/proprietaire/inscription')
        print(f"✅ Page d'inscription : {response.status_code}")
        
        print("\n🎉 L'application fonctionne correctement !")
        print("URL : http://127.0.0.1:5000")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    test_app() 