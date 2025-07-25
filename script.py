#!python3.12
# -*- coding: utf-8 -*-
# @Time    : 2025/07/19 15:42
# @Github  : zack Madiba
# @Email   : ofralsesse@gmail.com


import pandas as pd
import numpy as np
import sqlite3
import time
import requests
from io import BytesIO
from IPython.display import display


def telecharger_et_stocker_donnees_brutes(url, save_path):
    """
    Fonction 1: Télécharge les données depuis Google Sheets et les stocke localement
    """
    print("Téléchargement des données depuis Google Sheets...")
    
    try:
        # Téléchargement depuis Google Sheets
        response = requests.get(url)
        response.raise_for_status()
        
        if response.status_code == 200:
            # Lecture du fichier Excel depuis la réponse
            df_raw = pd.read_excel(BytesIO(response.content))
            
            # Sauvegarde locale en CSV
            df_raw.to_csv(save_path, index=False)
            
            print(f"Données téléchargées et sauvegardées dans '{save_path}'")
            print(f"{len(df_raw)} lignes, {len(df_raw.columns)} colonnes")
            print(f"Types de données :")
            for col, dtype in df_raw.dtypes.items():
                print(f"   - {col}: {dtype}")
            
            return df_raw
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur de réseau lors du téléchargement : {e}")
        
        # Tentative de lecture du fichier local en cas d'échec réseau
        try:
            print(f"Lecture de save_path'{save_path}'...")
            df_raw = pd.read_csv(save_path)
            print(f"Fichier local chargé avec succès")
            return df_raw
        except FileNotFoundError:
            print(f"Aucun fichier local '{save_path}' trouvé")
            return None
    
    except Exception as e:
        print(f"Erreur lors du téléchargement : {e}")
        return None


def nettoyer_et_transformer_donnees(df_raw):
    """
    Fonction 2: Nettoie et transforme les données
    """
    print("Nettoyage et transformation des données...")
    
    if df_raw is None:
        print("Aucune donnée à nettoyer")
        return None
    
    df_cleaned = df_raw.copy()
    
    # 1. Initialisation de la colonne contact investisseur
    df_cleaned['contact investisseur'] = np.nan
    df_cleaned['contact investisseur'] = df_cleaned['contact investisseur'].astype(object)
    
    # 2. Nettoyage des colonnes de statut (suppression du premier mot)
    columns_raw = ["Investisseur.statut", "Statut match", "Typologie", "Unnamed: 16"]
    for col in columns_raw:
        if col in df_cleaned.columns:
            df_cleaned[col] = df_cleaned[col].astype(str).str.split(' ', n=1).str[1]
    
    # 3. Conversion des montants (K€ → €)
    montant_cols = ["Montant estimé"]
    for col in montant_cols:
        if col in df_cleaned.columns:
            # Suppression des caractères K et k
            df_cleaned[col] = df_cleaned[col].replace({r"[Kk]": ""}, regex=True)
            # Conversion en numérique et multiplication par 1000
            df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce') * 1000
            df_cleaned[col] = df_cleaned[col].fillna(0)
    
    # 4. Création de la colonne contact unique
    for i, row in df_cleaned.iterrows():
        nom_val = row.get("Nom CP")
        prenom_val = row.get("Prénom")
        client_principal_val = row.get("Client Principal")
        investisseur_val = row.get("Investisseur")
        
        # Priorité 1 : Nom + Prénom
        if (pd.notna(nom_val) and pd.notna(prenom_val) and 
            str(nom_val).strip() != "" and str(prenom_val).strip() != ""):
            contact = f"{str(nom_val).strip()} {str(prenom_val).strip()}"
        # Priorité 2 : Client Principal
        elif pd.notna(client_principal_val) and str(client_principal_val).strip() != "":
            contact = str(client_principal_val).strip()
        # Priorité 3 : Investisseur
        elif pd.notna(investisseur_val) and str(investisseur_val).strip() != "":
            contact = str(investisseur_val).strip()
        else:
            contact = np.nan
        
        df_cleaned.at[i, 'contact investisseur'] = contact
    
    # 5. Suppression des colonnes inutiles
    cols_to_drop = ["Contact client", "Adresse email", "Nom CP", "Prénom", 
                   "Client Principal", "Unnamed: 16"]
    cols_existantes = [col for col in cols_to_drop if col in df_cleaned.columns]
    df_cleaned = df_cleaned.drop(cols_existantes, axis=1)
    
    # 6. Sauvegarde et affichage des résultats
    time.sleep(2)  # pause de 2 secs
    df_cleaned.to_csv("clean_data.csv", index=False)
    
    print("Données nettoyées et sauvegardées dans 'clean_data.csv'")
    print("Vérification des données ci-dessous :")
    print("Données brutes (échantillon) :")
    display(df_raw.iloc[13:16] if len(df_raw) > 16 else df_raw.head(3))
    print("Données nettoyées (échantillon) :")
    display(df_cleaned.iloc[13:16] if len(df_cleaned) > 16 else df_cleaned.head(3))
    
    return df_cleaned


def creer_base_donnees_et_tables(db_path="match.db"):
    """
    Fonction 3: Crée la base de données et toutes les tables
    """
    print("Création de la base de données et des tables...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Table typologie (dimension)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS typologie (
            id_typologie INTEGER PRIMARY KEY AUTOINCREMENT,
            Typologie TEXT UNIQUE
        );
        """)
        
        # Table startup
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS startup (
            id_startup INTEGER PRIMARY KEY,
            nom TEXT
        );
        """)
        
        # Table investisseur
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS investisseur (
            ID_investisseur INTEGER PRIMARY KEY,
            investisseur TEXT,
            Contact TEXT
        );
        """)
        
        # Table statut_investissement (dimension)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS statut_investissement (
            id_statut_investissement INTEGER PRIMARY KEY AUTOINCREMENT,
            statut_investissement TEXT UNIQUE
        );
        """)
        
        # Table statut_match (dimension)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS statut_match (
            ID_statut_match INTEGER PRIMARY KEY AUTOINCREMENT,
            statut_match TEXT UNIQUE
        );
        """)
        
        # Table centrale match_PRINCIPALE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS match_PRINCIPALE (
            id_match INTEGER PRIMARY KEY,
            typologie_id INTEGER,
            startup_id INTEGER,
            statut_investissement_id INTEGER,
            investisseur_ID INTEGER,
            statut_match_id INTEGER,
            depot TEXT,
            montant_estimé REAL,
            commentaire TEXT,

            FOREIGN KEY (typologie_id) REFERENCES typologie(id_typologie),
            FOREIGN KEY (startup_id) REFERENCES startup(id_startup),
            FOREIGN KEY (statut_investissement_id) REFERENCES statut_investissement(id_statut_investissement),
            FOREIGN KEY (investisseur_ID) REFERENCES investisseur(ID_investisseur),
            FOREIGN KEY (statut_match_id) REFERENCES statut_match(ID_statut_match)
        );
        """)
        
        # Table raw_data pour stocker les données brutes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        );
        """)
        
        conn.commit()
        conn.close()
        
        print(f"Base de données '{db_path}' créée avec succès")
        print("Tables créées : typologie, startup, investisseur, statut_investissement, statut_match, match_PRINCIPALE, raw_data")
        
        return db_path
    
    except Exception as e:
        print(f"Erreur lors de la création de la base : {e}")
        return None


def inserer_donnees_dans_bdd(df_cleaned, db_path="match.db"):
    """
    Fonction 4: Insère les données dans la base de données
    """
    print("Début de l'insertion des données dans la base de données...")
    
    if df_cleaned is None:
        print("Aucune donnée à insérer")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Sauvegarde des données dans raw_data
        df_cleaned.to_sql("raw_data", conn, if_exists="replace", index=False)
        print("Données sauvegardées dans la table raw_data")
        
        # 2. Lecture et nettoyage de base
        df = pd.read_sql_query("SELECT * FROM raw_data", conn)
        df["Typologie"] = df["Typologie"].fillna("").str.strip()
        df["Statut match"] = df["Statut match"].fillna("").str.strip()
        df["Investisseur.statut"] = df["Investisseur.statut"].fillna("").str.strip()
        
        # 3. Insertion des tables de dimension
        print("Insertion des données de référence...")
        
        # Table typologie
        cursor.executemany("""
            INSERT OR IGNORE INTO typologie (Typologie)
            VALUES (?)
        """, df[["Typologie"]].drop_duplicates().dropna().values)
        
        # Table statut_match
        cursor.executemany("""
            INSERT OR IGNORE INTO statut_match (statut_match)
            VALUES (?)
        """, df[["Statut match"]].drop_duplicates().dropna().values)
        
        # Table statut_investissement
        cursor.executemany("""
            INSERT OR IGNORE INTO statut_investissement (statut_investissement)
            VALUES (?)
        """, df[["Investisseur.statut"]].drop_duplicates().dropna().values)
        
        # 4. Table startup
        startup_unique = df[["Id.Startup", "Start-up"]].drop_duplicates(subset=["Id.Startup"])
        cursor.executemany("""
            INSERT OR IGNORE INTO startup (id_startup, nom)
            VALUES (?, ?)
        """, startup_unique.values)
        
        # 5. Table investisseur
        invest_unique = df[["Id.Investisseur", "Investisseur", "contact investisseur"]].drop_duplicates(subset=["Id.Investisseur"])
        cursor.executemany("""
            INSERT OR IGNORE INTO investisseur (ID_investisseur, investisseur, Contact)
            VALUES (?, ?, ?)
        """, invest_unique.values)
        
        # 6. Récupération des mappings d'IDs
        print("Création des liens entre les tables...")
        typologie_map = dict(cursor.execute("SELECT Typologie, id_typologie FROM typologie").fetchall())
        statut_match_map = dict(cursor.execute("SELECT statut_match, ID_statut_match FROM statut_match").fetchall())
        statut_invest_map = dict(cursor.execute("SELECT statut_investissement, id_statut_investissement FROM statut_investissement").fetchall())
        
        # 7. Table centrale match_PRINCIPALE
        match_unique = df.drop_duplicates(subset=["Id.Match"])
        match_rows = []
        
        for _, row in match_unique.iterrows():
            try:
                match_rows.append((
                    int(row["Id.Match"]),
                    typologie_map.get(row["Typologie"]),
                    int(row["Id.Startup"]),
                    statut_invest_map.get(row["Investisseur.statut"]),
                    int(row["Id.Investisseur"]),
                    statut_match_map.get(row["Statut match"]),
                    row["Dépôt"],
                    float(row["Montant estimé"]) if str(row["Montant estimé"]).strip() != "" else None,
                    row["Commentaire"]
                ))
            except Exception as e:
                print(f"Erreur à la ligne {row['Id.Match']} : {e}")
        
        cursor.executemany("""
            INSERT OR IGNORE INTO match_PRINCIPALE (
                id_match,
                typologie_id,
                startup_id,
                statut_investissement_id,
                investisseur_ID,
                statut_match_id,
                depot,
                montant_estimé,
                commentaire
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, match_rows)
        
        conn.commit()
        conn.close()
        
        print("Toutes les données ont été insérées avec succès")
        print(f"{len(match_rows)} enregistrements insérés dans la table principale")
        
        return True
    
    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")
        return False

time.sleep(0.5)  # pause de 0.5 secs


def main(url, save_path="data.csv", db_path="match.db"):
    """
    Fonction principale qui orchestre tout le processus
    """
    
    print("-" * 14)
    print("DÉBUT DU TRAITEMENT DES DONNÉES...")
    time.sleep(1.5)  # pause de 0.5 secs
    print("-" * 14)
    print("\n")
    print(" --- Résultats attendus ---")
    print("\n")
    print(f"Source de données, URL Google Sheets : {url}")
    print(f"Fichier local : {save_path}")
    print(f"🗄Base de données : {db_path}")
    print("-" * 30)
    
    # Étape 1 : Téléchargement depuis Google Sheets et stockage local
    df_raw = telecharger_et_stocker_donnees_brutes(url, save_path)
    if df_raw is None:
        print("impossible de télécharger/charger les données")
        return None
    
    print("-" * 60)
    
    # Étape 2 : Nettoyage et transformation
    df_cleaned = nettoyer_et_transformer_donnees(df_raw)
    if df_cleaned is None:
        print("impossible de nettoyer les données")
        return None
    
    print("-" * 60)
    
    # Étape 3 : Création de la base de données et des tables
    db_created = creer_base_donnees_et_tables(db_path)
    if db_created is None:
        print("Arrêt du processus : impossible de créer la base de données")
        return None
    
    print("-" * 60)
    
    # Étape 4 : Insertion des données
    insertion_success = inserer_donnees_dans_bdd(df_cleaned, db_path)
    if not insertion_success:
        print("Erreur lors de l'insertion des données")
        return None
    time.sleep(1.5)  # pause de 0.5 secs
    print("\n")
    print("-" * 30)
    print("=== TRAITEMENT TERMINÉ AVEC SUCCÈS ===")
    print("\n")
    print(f"Fichier nettoyé : clean_data.csv")
    print(f"🗄Base de données : {db_path}")
    print(f"Nombre de lignes traitées : {len(df_cleaned)}")
    
    return df_cleaned


# Point d'entrée du programme
if __name__ == "__main__":
    # Configuration
    url = "https://docs.google.com/spreadsheets/d/1-ozQDxIBwo-XhgNrfqDZaPwlN9j88c8E/export?format=xlsx&id=1-ozQDxIBwo-XhgNrfqDZaPwlN9j88c8E"
    save_path = "data.csv"  # Fichier local de sauvegarde
    db_path = "match.db"    # Nom de la base de données
    
    # Lancement du traitement complet
    resultat = main(url, save_path, db_path)
    
    if resultat is not None:
        print("Le traitement s'est terminé avec succès !")
        time.sleep(0.5)
        print("\n")
        print("Merci")
    else:
        print("Le traitement a échoué.")
        
        

print("-" * 30) 
