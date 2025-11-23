# tools_file.py (Version Corrigée)

import json

# Constante pour le fichier de données (à définir ici)
JSON_FILE_PATH = "data.json" # Assurez-vous que data.json est au même niveau que main.py

def load_data_from_json(json_file=JSON_FILE_PATH):
    """Charge les données depuis un fichier JSON."""
    # Le paramètre json_file est ici pour compatibilité, mais il utilise le chemin fixe.
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        # Permet à main.py de capter l'erreur FileNotFoundError
        raise

def write_in_json_file(data, json_file=JSON_FILE_PATH):
    """Écrit les données dans un fichier JSON avec une indentation de 4."""
    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)