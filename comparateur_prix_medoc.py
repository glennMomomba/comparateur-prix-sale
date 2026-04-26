"""
import pandas as pd
import sys # pour lire les arguments du terminal

def trouver_moins_cher(nom_medicament) :
# Cette fonction prend un nom de médicament en paramètre et afihe le rapport complet

    # Etape 1 : Chargement des données
    try :
        df = pd.read_csv("prix_sale.csv")
    except FileNotFoundError :
        print("\n ERREUR : Fichier 'prix_sale.csv' introuvable")  
        print("Vérifie que le fichier est dans le même dossier que le script") 
        return 

    # Etape 2 : Filtrage .str.lower() pour ignorer les majuscules
    df_medicament = df[df["medicament"].str.lower() == nom_medicament.lower()]

    # Etape 3 : Sécurité
    if df_medicament.empty :
        print(f"\n '{nom_medicament}' introuvable")
        print("Médicaments disponibles :", ",".join(df["medicament"].unique()))
        return 
    
    # Etape 4 : Calcul
    ligne_moins_cher = df_medicament.loc[df_medicament["prix"].idxmin()]
    economie = df_medicament["prix"].max() - ligne_moins_cher["prix"]

    # Etape 5 : Affichage du rapport final
    print("\n" + "="*50)
    print(f" RAPPORT PRIX - {nom_medicament} - SALÉ")
    print("="*50)
    print(f"Meilleur prix  : {ligne_moins_cher['prix']} dh")
    print(f"Pharmacie      : {ligne_moins_cher['pharmacie']}")
    print(f"Quartier       : {ligne_moins_cher['quartier']}")
    print(f"Téléphone      : {ligne_moins_cher['telephone']}")
    print(f"Économie       : {economie:.2f} dh vs plus cher")
    print("="*50)



# PROGRAMME PRINCIPAL : Lancement de la fonction
# OBJECTIF : sys.argv lit ce qui est tapé après python comparateur_prix_medoc.py

if __name__ == "__main__" : # Si l'utilisateur tape un médoc 
    if len(sys.argv) > 1 :
        medicament_demande = "".join(sys.argv[1:]) # Gestion du médicament 
        trouver_moins_cher(medicament_demande)

else : # Sinon on utilise le médicament par défaut
    print("Usage : python comparateur_prix_medoc.py 'Nom du medicament")
    print("Exemple : python comparateur_prix_medoc.py 'Maltofer Fol")
    trouver_moins_cher("Maltofer Fol")

"""

import requests
from bs4 import BeautifulSoup
import argparse

def chercher_prix_web(nom_medicament):
    try:
        # 1. Lancement de la requête web
        url = "https://httpbin.org/get"  # Site de test qui renvoie l'@IP + headers
        params = {'medicament': nom_medicament} # renvoie le nom du médicament à  la requette
        
        reponse = requests.get(url, params=params, timeout=5) 
        reponse.raise_for_status() #Verifie que la requette a réussie
        
        # 2. On parse le JSON de réponse comme si c'était une vraie API
        data = reponse.json()
        
        # 3. On simule le résultat métier car pas d'API medoc MA/GA
        prix_simule = {
            'Doliprane': '17.50 DH',
            'Maltofer': '89.00 DH', 
            'Mustela': '95.00 DH'
        }.get(nom_medicament, 'Non référencé') # Si le médoc n'est pas dans la simulation (non référencé)
        
        # Affichage du résultat final
        return f"\nRequête web OK vers {data['url']}\nTrouvé : {nom_medicament}\nPrix PPM Maroc : {prix_simule}\nNote: API medoc MA indisponible, simulation pour J4"
        
    except requests.exceptions.RequestException as e:
        return f"Erreur réseau : {e}"


# PROGRAMME PRINCIPAL : Lancement de la fonction
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comparateur prix medocs J4") # gestion des arguments du terminal
    parser.add_argument("medicament", help="Nom du medicament") #argument obligatoire pour le nom du médicament 
    args = parser.parse_args() # Lecture des args du terminal
    
    resultat = chercher_prix_web(args.medicament) # Appel de la fonction de recherche
    print(resultat)
    print("="*50 + "\n")
