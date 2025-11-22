# tools_file.py

"""
import json
"""
import json

# Définition du dossier de ressources si nécessaire, mais pour cet exemple simple,
# nous allons supposer que data.json est au même niveau que main.py
# ressource_folder = "ressources/"

def load_data_from_json (json_file):
    """Charge les données depuis un fichier JSON."""
    # Note: On suppose que data.json est au même niveau.
    with open (json_file, "r") as f:
        data = json.load(f)
    return data

def write_in_json_file (data, json_file):
    """Écrit les données dans un fichier JSON avec une indentation de 4."""
    # Note: On suppose que data.json est au même niveau.
    with open (json_file, "w") as f:
        json.dump (data, f, indent=4)

# L'importation de json est déjà faite, pas besoin de la répéter.
# Les imports de data.json ne sont pas nécessaires ici.