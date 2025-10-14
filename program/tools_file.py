#importation du fichier data.json dans le dossier ressource
import json

with open("ressource_folder/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

#La fonction sld permet de retourner le solde du client
def sld ():
    for account in data:
        return account["sold"]

#La foction old_withdrawal permet de retourner les anciens retraits du client
def old_withdrawal ():
    for account in data:
        return account["withdrawal"]
    
def new_sold ():
    if n > 0:
        sld = sld + n
    if n < 0:
        sld = sld + n 
    if n == 0:
        sld = sld + 0