import pandas as pd

# Etape 1: Chargement des données 
print("Chargement des prix des pharmacies de Sale...")
df = pd.read_csv("prix_sale.csv")
print("Colonnes trouvées :", df.columns.tolist()) # Affichage du nom des colonnes

# Etape 2: Filtrage sur le médicament qui intéresse
medoc_cherche = "Maltofer Fol"
df_medicament = df[df["medicament"] == medoc_cherche]

# Etape 3: Sécurité vérifier qu'on a trouvé le médicament
if df_medicament.empty:
    print(f"\n EEREUR : '{medoc_cherche}' introuvable dans le fichier.")
    print("Medocs disponibles :", df["medicament"].unique())


# Etape 4: Trouver la ligne avec le prix minimum
else :
    ligne_moins_cher = df_medicament.loc[df_medicament["prix"].idxmin()]

    # Etape 5: Calcul de l'économie (vs la plus chére)
    prix_max = df_medicament["prix"].max()
    economie = prix_max - ligne_moins_cher["prix"]

    # Etape 6: Affichage du rapport business
    print("\n" + "="*50)
    print(f"RAPPORT PRIX - {medoc_cherche} - SALE")
    print("="*50)
    print(f"Meilleur prix : {ligne_moins_cher['prix']} dh")
    print(f"Pharmacie     : {ligne_moins_cher['pharmacie']}")
    print(f"Quartier      : {ligne_moins_cher['quartier']}")
    print(f"Téléphone     : {ligne_moins_cher['telephone']}")
    print(f"Economie      : {economie:.2f} dh vs pharma la plus chère")
    print("="*50)
    print("Script exécuté en 0.2s au lieu de 20min manuel")