from tools_file import load_data_from_json, write_in_json_file
from data import quitting_words
import datetime

# Chargement des clients depuis data.json
clients = load_data_from_json("data.json")

# Variable globale pour retenir le client connecté
current_user = None


# =============================
#       FONCTIONS SOLDE
# =============================

def get_sold():
    # ❌ Ancien code :
    # for account in data: return account["sold"]
    # data n’existait pas et retournait un seul élément

    # ✔️ Correction : on utilise le client connecté
    return clients[current_user]["sold"]


def set_sold(new_value):
    clients[current_user]["sold"] = new_value
    write_in_json_file(clients, "data.json")  # sauvegarde automatique


# =============================
#      FONCTIONS RETRAITS
# =============================

def show_withdrawal_history():
    # ❌ Ancien code :
    # print (f"Your old withdrawals are {old_withdrawal}.\n")
    #
    # old_withdrawal était une fonction, pas un résultat

    print("\n--- Withdrawal history ---")

    for entry in clients[current_user]["withdrawal"]:
        print(f"- {entry['montant']}€ on {entry['date']} from {entry['from']}")

    print("\n")


def make_withdrawal():
    print("Enter PIN to continue.")

    # ❌ Ancien code :
    # pin = ""
    # tentative = int(input("enter your pin"))
    #
    # Le PIN était vide !

    pin = clients[current_user]["pin"]

    attempt = int(input("PIN : "))

    while attempt != pin:
        print("Wrong PIN, try again.")
        attempt = int(input("PIN : "))

    amount = int(input("Amount to withdraw : "))

    if amount > get_sold():
        print("Insufficient funds!")
        return

    # Mise à jour du solde
    set_sold(get_sold() - amount)

    # Ajout dans l’historique
    clients[current_user]["withdrawal"].append({
        "montant": amount,
        "date": str(datetime.date.today()),
        "from": "ATM"
    })

    write_in_json_file(clients, "data.json")

    print("Withdrawal successful.")


# =============================
#      FONCTIONS PAYEMENT
# =============================

def make_payment():
    recipient = input("Recipient name (or 'quit' to cancel): ")

    if recipient in quitting_words:
        return

    amount = int(input("Amount to transfer: "))

    if amount > get_sold():
        print("Insufficient funds!")
        return

    print(f"Confirm transfer {amount}€ to {recipient} ?")
    confirmation = input("Enter 1 to confirm, 2 to cancel: ")

    # ❌ Ancien :
    # input == 1  → input était la fonction, pas la valeur !
    # ✔️ Correction :
    if confirmation == "1":

        set_sold(get_sold() - amount)

        clients[current_user]["payment"].append({
            "montant": amount,
            "date": str(datetime.date.today()),
            "to": recipient
        })

        write_in_json_file(clients, "data.json")
        print("Payment successful!")

    else:
        print("Payment canceled.")


# =============================
#         PAGES
# =============================

def go_to_sold_page():
    print(f"\nYour balance is : {get_sold()} €\n")


def go_to_payment_page():
    print("1. Make a payment\n2. Back")

    choice = input("Your choice : ")

    # ❌ Ancien :
    # int(input) == 1
    # ✔️ Correction :
    if choice == "1":
        make_payment()


def go_to_withdrawal_page():
    print("1. Withdraw money\n2. Show history\n3. Back")

    choice = input("Your choice : ")

    if choice == "1":
        make_withdrawal()
    elif choice == "2":
        show_withdrawal_history()


# =============================
#       IDENTIFICATION
# =============================

def identity_is_valid(name, first_name, password):

    # ❌ Ancien :
    # erreur : Name et Fname au lieu de name et first_name

    if name in clients:
        if clients[name]["Fname"] == first_name and clients[name]["password"] == password:
            return True
    return False


# =============================
#     PAGE PRINCIPALE
# =============================

def main_page():
    print(f"\nHello {clients[current_user]['Fname']} {clients[current_user]['Name']}")

    print("1. Balance")
    print("2. Payments")
    print("3. Withdrawals")
    print("4. Quit")

    action = input("Your choice : ")

    if action == "1":
        go_to_sold_page()
    elif action == "2":
        go_to_payment_page()
    elif action == "3":
        go_to_withdrawal_page()
    elif action == "4":
        print("Goodbye!")
        exit()

    main_page()  # retourne au menu après chaque action


# =============================
#         MAIN
# =============================

def main():
    global current_user

    print("=== LOGIN ===")

    name = input("Name : ")
    first_name = input("First name : ")
    password = input("Password : ")

    if identity_is_valid(name, first_name, password):
        print("Login successful!")
        current_user = name
        main_page()

    else:
        print("Login failed. Try again.\n")
        main()


main()
