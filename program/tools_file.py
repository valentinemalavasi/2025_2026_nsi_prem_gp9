# tools_file.py

"""
import json
"""
import json

def load_data_from_json (json_file):
    """Charge les données depuis un fichier JSON."""
   
    with open (json_file, "r") as f:
        data = json.load(f)
    return data

def write_in_json_file (data, json_file):
    """Écrit les données dans un fichier JSON avec une indentation de 4."""
   
    with open (json_file, "w") as f:
        json.dump (data, f, indent=4)

