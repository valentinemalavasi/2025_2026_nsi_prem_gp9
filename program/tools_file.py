# /programs/tools_file.py

import json
import os
# Chemin vers le fichier data.json
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "ressource_folder",
    "data.json"
)

# Variable globale pour stocker les données du fichier
DATA = None

def load_data():
    """Charge les données clients depuis le fichier JSON."""
    global DATA
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            DATA = json.load(f)
            return DATA
    except FileNotFoundError:
        print(f"ERREUR: Fichier de données non trouvé à l'emplacement: {DATA_PATH}")
        return None
    except json.JSONDecodeError:
        print("ERREUR: Le fichier data.json est corrompu (JSON invalide).")
        return None

def save_data(data_to_save):
    """Sauvegarde les données (ex: après un virement) dans le fichier JSON."""
    try:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4)
        print("Données mises à jour et sauvegardées.")
    except Exception as e:
        print(f"ERREUR lors de la sauvegarde: {e}")


def get_account_by_identity(name, fname, password):
    if DATA is None:
        load_data()
    
    if DATA is None:
        return None, None

    # Parcourt les comptes
    for account_key, account_data in DATA.items():
        # Vérification stricte des champs pour l'identification
        if (account_data.get("Name") == name and
            account_data.get("Fname") == fname and
            account_data.get("password") == password):
            
            # Retourne la clé unique et les données du compte
            return account_key, account_data
            
    return None, None # Identifiants incorrects


def check_pin(pin_attempt, current_account):
    if current_account and "pin" in current_account:
        return int(pin_attempt) == current_account["pin"]
    return False

# Chargement initial des données au démarrage du module
load_data()