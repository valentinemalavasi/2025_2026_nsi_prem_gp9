"""
import json

ressource_folder = "ressources/"

def load_data_from_json (json_file):
    with open (json_file in ressource_folder, "r") as f:
        data = json.load(f)
    return data

def write_in_json_file (data, json_file):
    with open (json_file in ressource_folder, "w") as f:
        json.dump (data, f, indent=4)

import json
"""

ressource_folder = "ressource_folder/"

def load_data_from_json(json_file):
    # ❌ Ancien code :
    # with open (json_file in ressource_folder, "r") as f:

    # ✔️ Correction : concaténation correcte du chemin
    with open(ressource_folder + json_file, "r") as f:
        data = data.json.load(f)
    return data


def write_in_json_file(data, json_file):
    # ❌ Ancien code :
    # with open (json_file in ressource_folder, "w") as f:

    # ✔️ Correction : concaténation correcte du chemin
    with open(ressource_folder + json_file, "w") as f:
        data.json.dump(data, f, indent=4)
