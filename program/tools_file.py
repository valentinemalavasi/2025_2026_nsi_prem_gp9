import json

def load_data_from_json (json_file):
    with open (json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_in_json_file (data, json_file):
    with open (json_file, "w", encoding="utf-8") as f:
        json.dump (data, f, indent=4)