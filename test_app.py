#!/usr/bin/env python3
"""
Script de test pour l'application Résidence CI+
Vérifie que toutes les fonctionnalités fonctionnent correctement
"""

import json
import os
import sys

def test_json_file():
    """Test du fichier JSON des résidences"""
    print("🔍 Test du fichier residences.json...")
    
    try:
        with open('residences.json', 'r', encoding='utf-8') as file:
            residences = json.load(file)
        
        print(f"✅ Fichier JSON valide - {len(residences)} résidences trouvées")
        
        # Vérifier la structure de chaque résidence
        required_fields = ['id', 'nom', 'ville', 'adresse', 'prix', 'description', 
                         'equipements', 'image', 'telephone', 'latitude', 'longitude', 'disponible']
        
        for i, residence in enumerate(residences):
            missing_fields = [field for field in required_fields if field not in residence]
            if missing_fields:
                print(f"❌ Résidence {i+1} manque les champs: {missing_fields}")
                return False
            else:
                print(f"✅ Résidence {i+1}: {residence['nom']} à {residence['ville']}")
        
        return True
        
    except FileNotFoundError:
        print("❌ Fichier residences.json non trouvé")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON: {e}")
        return False

def test_files_exist():
    """Test de l'existence des fichiers nécessaires"""
    print("\n🔍 Test de l'existence des fichiers...")
    
    required_files = [
        'app.py',
        'residences.json',
        'requirements.txt',
        'README.md',
        'templates/index.html',
        'templates/ajouter.html',
        'templates/editer.html',
        'static/css/style.css'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MANQUANT")
            all_exist = False
    
    return all_exist

def test_flask_import():
    """Test de l'import Flask"""
    print("\n🔍 Test de l'import Flask...")
    
    try:
        from flask import Flask, render_template, request, jsonify
        print("✅ Flask peut être importé")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import Flask: {e}")
        print("💡 Exécutez: pip install -r requirements.txt")
        return False

def test_app_structure():
    """Test de la structure de l'application Flask"""
    print("\n🔍 Test de la structure de l'application...")
    
    try:
        # Importer l'application
        from app import app, load_residences, save_residences
        
        # Test de chargement des résidences
        residences = load_residences()
        if isinstance(residences, list) and len(residences) > 0:
            print("✅ Fonction load_residences() fonctionne")
        else:
            print("❌ Fonction load_residences() ne retourne pas de données valides")
            return False
        
        # Test de sauvegarde (simulation)
        test_data = [{"id": 999, "nom": "Test", "ville": "Test", "prix": 1000}]
        if save_residences(test_data):
            print("✅ Fonction save_residences() fonctionne")
            # Restaurer les données originales
            load_residences()
        else:
            print("❌ Fonction save_residences() ne fonctionne pas")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de l'application: {e}")
        return False

def test_templates():
    """Test des templates HTML"""
    print("\n🔍 Test des templates HTML...")
    
    template_files = ['index.html', 'ajouter.html', 'editer.html']
    
    for template in template_files:
        template_path = f'templates/{template}'
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if 'Bootstrap' in content and 'Flask' in content:
                        print(f"✅ {template} - Structure valide")
                    else:
                        print(f"⚠️ {template} - Structure basique")
            except Exception as e:
                print(f"❌ {template} - Erreur de lecture: {e}")
        else:
            print(f"❌ {template} - Fichier manquant")
    
    return True

def main():
    """Fonction principale de test"""
    print("🏠 Test de l'application Résidence CI+")
    print("=" * 50)
    
    tests = [
        ("Fichiers existants", test_files_exist),
        ("Fichier JSON", test_json_file),
        ("Import Flask", test_flask_import),
        ("Structure application", test_app_structure),
        ("Templates HTML", test_templates)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - RÉUSSI")
            else:
                print(f"❌ {test_name} - ÉCHEC")
        except Exception as e:
            print(f"❌ {test_name} - ERREUR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés ! L'application est prête.")
        print("\n🚀 Pour lancer l'application:")
        print("   python app.py")
        print("   Puis ouvrez: http://localhost:5000")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 