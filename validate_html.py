import re
from bs4 import BeautifulSoup
import os

def validate_html_file(file_path):
    """Valide un fichier HTML pour les problèmes courants"""
    print(f"🔍 Validation de {file_path}")
    print("=" * 50)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse avec BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Vérifications
        issues = []
        
        # 1. Vérifier les balises non fermées
        unclosed_tags = []
        for tag in soup.find_all():
            if tag.name and not tag.is_empty_element:
                if not tag.string and not tag.find_all():
                    unclosed_tags.append(tag.name)
        
        if unclosed_tags:
            issues.append(f"⚠️ Balises potentiellement non fermées : {unclosed_tags[:5]}")
        
        # 2. Vérifier les attributs href
        links = soup.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith('javascript:'):
                issues.append("⚠️ Liens javascript: détectés (sécurité)")
        
        # 3. Vérifier les scripts inline
        scripts = soup.find_all('script')
        inline_scripts = [s for s in scripts if s.string]
        if len(inline_scripts) > 2:
            issues.append("⚠️ Trop de scripts inline (performance)")
        
        # 4. Vérifier les images sans alt
        images = soup.find_all('img')
        images_without_alt = [img for img in images if not img.get('alt')]
        if images_without_alt:
            issues.append(f"⚠️ {len(images_without_alt)} images sans attribut alt")
        
        # 5. Vérifier la structure
        if not soup.find('title'):
            issues.append("⚠️ Balise <title> manquante")
        
        if not soup.find('meta', attrs={'name': 'viewport'}):
            issues.append("⚠️ Meta viewport manquante (responsive)")
        
        # 6. Vérifier les classes Bootstrap
        bootstrap_classes = ['container', 'row', 'col-', 'btn-', 'card', 'navbar']
        found_bootstrap = []
        for class_name in bootstrap_classes:
            if soup.find(class_=re.compile(class_name)):
                found_bootstrap.append(class_name)
        
        if found_bootstrap:
            print(f"✅ Classes Bootstrap détectées : {found_bootstrap}")
        
        # 7. Vérifier les icônes Font Awesome
        fa_icons = soup.find_all(class_=re.compile('fas|fab|far'))
        if fa_icons:
            print(f"✅ {len(fa_icons)} icônes Font Awesome détectées")
        
        # 8. Vérifier les templates Jinja2
        jinja_patterns = ['{{', '}}', '{%', '%}']
        jinja_count = sum(content.count(pattern) for pattern in jinja_patterns)
        if jinja_count > 0:
            print(f"✅ {jinja_count} expressions Jinja2 détectées")
        
        # Résultats
        if issues:
            print("❌ Problèmes détectés :")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("✅ Aucun problème majeur détecté")
        
        # Statistiques
        print(f"\n📊 Statistiques :")
        print(f"  - Balises : {len(soup.find_all())}")
        print(f"  - Liens : {len(links)}")
        print(f"  - Images : {len(images)}")
        print(f"  - Scripts : {len(scripts)}")
        print(f"  - Formulaires : {len(soup.find_all('form'))}")
        
        return len(issues) == 0
        
    except Exception as e:
        print(f"❌ Erreur lors de la validation : {e}")
        return False

if __name__ == "__main__":
    html_files = [
        "templates/index.html",
        "templates/proprietaire/connexion.html",
        "templates/proprietaire/inscription.html",
        "templates/ajouter.html",
        "templates/editer.html"
    ]
    
    all_valid = True
    for file_path in html_files:
        if os.path.exists(file_path):
            if not validate_html_file(file_path):
                all_valid = False
            print()
        else:
            print(f"⚠️ Fichier non trouvé : {file_path}")
    
    if all_valid:
        print("🎉 Tous les fichiers HTML sont valides !")
    else:
        print("⚠️ Certains fichiers HTML ont des problèmes.") 