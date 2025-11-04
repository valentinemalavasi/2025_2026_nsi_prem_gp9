#importation du fichier data.json dans le dossier ressource
import json

def load_data_from_json (json_file):
    with open (json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_in_json_file (data, json_file):
    with open (json_file, "w", encoding="utf-8") as f:
        json.dump (data, f, indent=4)

def system (account):
    pass

def account (data):
    pass

def reading_file ():
    for e in data:
        account in range (len)

def written ():
    for e in system:
        pass

def answer ():
    for answer in input():
        pass

def correct_pin ():
    for pin_c in account:
        if answer == pin:
            return True
        else:
            return False
