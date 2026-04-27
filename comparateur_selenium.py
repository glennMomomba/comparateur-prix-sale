from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import time
import re


def chercher_prix_selenium(nom_medicament):
    """
    Utilisation de selenium pour scraper medicament.ma pour trouver le prix du médicament donné.
        - Lancement de Chrome en mode headless
    Filtre les cartes pour trouver le bon medicament.
    """
    options = webdriver.ChromeOptions() # Pour ne pas ouvrir une fenetre Chrome visible
    options.add_argument('--headless=new') # Mode headless pour ne pas ouvrir une fenetre Chrome visible
    options.add_argument('--no-sandbox') # Nécessaire pour certains environnements (ex: Docker)
    options.add_argument('--disable-gpu') # Désactive l'accélération GPU, utile en mode headless
    options.add_argument('--disable-dev-shm-usage') # Evite les problèmes de mémoire partagée dans certains environnements
    options.add_argument('--window-size=1920,1080') # Définit une taille d'écran pour éviter les problèmes de responsive design qui cachent des éléments
    
    # Initialisation du driver à None pour pouvoir le fermer dans le finally même en cas d'erreur & Lancement de Chrome
    driver = None 
    try: 
        driver = webdriver.Chrome(options=options)
        
        url = f"https://medicament.ma/recherche?search={nom_medicament}"
        driver.get(url)
        
        wait = WebDriverWait(driver, 15) 
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "medicine-card")))
        time.sleep(2)
        
        print("="*50)
        print(f"Page OK: {driver.title}" + "\n")
        
        # 1. On recupere TOUTES les cartes
        toutes_les_cartes = driver.find_elements(By.CLASS_NAME, "medicine-card")
        
        # 2. Recherche de la carte qui contient vraiment le nom cherche
        carte_cible = None
        for carte in toutes_les_cartes:
            texte_carte = carte.text.lower()
            # Recherche du mot exact, pas "Ozempic" quand on veut "Doliprane"
            if nom_medicament.lower() in texte_carte:
                carte_cible = carte
                print(f"Carte trouvee contenant : {nom_medicament}" + "\n")
                break
        
        # 3. Recuperation du texte de la carte cible ou de la 1ere carte si aucune ne correspond exactement
        if not carte_cible:
            carte_cible = toutes_les_cartes[0]
            print("Aucune carte exacte. Prise de la 1ere carte par defaut." + "\n")
        
        texte_complet = carte_cible.text
        lignes = texte_complet.split('\n')
        nom = lignes[0].strip()
        
        # 4. Utilisation de Regex pour extraire le prix
        prix_match = re.search(r'PPV:\s*([\d,\.]+\s*dhs)', texte_complet, re.IGNORECASE)
        if prix_match:
            prix = f"PPV: {prix_match.group(1)}"
        else:
            prix_match = re.search(r'([\d,\.]+\s*dhs)', texte_complet, re.IGNORECASE)
            prix = prix_match.group(1) if prix_match else "Prix non trouve"
        
        return f"Trouvé : {nom}\n{prix}"
    
    # Gestion des exceptions pour les erreurs Selenium et autres    
    except Exception as e:
        return f"Erreur Selenium : {type(e).__name__} - {str(e)[:100]}"
    finally:
        if driver:
            driver.quit()

           
# PROGRAMME PRINCIPAL : Lancement de la fonction
# OBJECTIF : sys.argv lit ce qui est tapé après python comparateur_selenium.py
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="J5 - Scraper Selenium medicament.ma") # gestion des arguments du terminal
    parser.add_argument("medicament", help="Nom du medicament. Ex: Doliprane") # argument obligatoire pour le nom du médicament
    args = parser.parse_args() # Lecture des args du terminal
    
    print("Lancement Chrome auto-driver..." + "\n")
    print(chercher_prix_selenium(args.medicament)) # Appel de la fonction de recherche et affichage du résultat
    print("="*50 + "\n")
