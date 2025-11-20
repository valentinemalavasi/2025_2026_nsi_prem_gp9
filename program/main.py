"""

virement = ["payment"]
sold = ["sold"]
retrait = ["withdrawal"]

def opener ():
    with open ("tools_file.py","r") as f:
        return tools_file = "tools_file.py"
    with open ("data.py", "r") as f:
        return data = "data.py"


#La fonction sld permet de retourner le solde du client
def get_sold():
    return clients[current_user]["sold"]

def set_sold(new_value):
    clients[current_user]["sold"] = new_value
    write_in_json_file(clients, "data.json")

#La fonction old_withdrawal permet de retourner les anciens retraits du client
def old_withdrawal ():
    for account in data:
        return account["withdrawal"]

    # FONCTION a retravailler et connecter solde aux comptes 
def new_sold_received (recipient, payment_amount):
    sld = sld + n
    return sld

def new_sold_given (n):
    sld = sld - n
    if sld < 0 :
        print ("Vous êtes dans le rouge ")
    return sld

def make_a_payment () :
    recipient = input("Enter the name of the recipient (enter 'quit' to cancel): ")
    payment_amount = input("Enter the amount you want to transfer (enter 'quit' to cancel): ")
    if recipient or payment_amount in quitting_words :
        go_to_payment_page
    else :
        input(f"Enter 1 to make a {payment_amount} € payment to {recipient}: \n"
                "Enter 2 to cancel")
        if input == 1 :
            new_sold_given, new_sold_received
            print ("payment made !")
        elif input == 2 :
            go_to_payment_page
        
    
        
#La fonction montre la page permettant de faire des virements
def go_to_payment_page ():
    print("To make a payment, enter 1.\n"
          "To go back to main page, enter 2.")
    if int(input) == 1:
        make_a_payment ()
    elif int(input) == 2:
        main_page ()

def go_to_sold_page ():
    print(f"Your sold is {sld}")


def show_withdrawal_history():
    print("\n--- Withdrawal history ---")
        for entry in clients[current_user]["withdrawal"]:
        print(f"- {entry['montant']}€ on {entry['date']} from {entry['from']}")
    print("\n")

    
def enter_pin ():
    tentative = int(input("enter your pin"))
    pin= ""
    while tentative != pin:
        tentative = int(input("reenter your pin"))
        if pin==tentative:
            print("code correct")

def vnew_sold ():
   value_to_withdraw = int(input("Enter the value you want to withdraw : "))
   print(sld-value_to_withdraw)

def exit_system():
    return main(account)

 

#La fonction main_page permet de demander ce que veux regarder le client sur son compte bancaire.
def main_page (account):
    next_action = input(f"Hello {FName}, {Name}, what do you want to know about your bank account?\n"
          "1.sold\n"
          "2.payment\n"
          "3.withdrawal")
    if next_action == 1 :
        go_to_sold_page()
    elif next_action == 2 :
        go_to_payment_page()
    elif next_action == 3 :
        go_to_withdrawal_page()
    elif next_action in quitting_words:
        exit_system()

def is_a_valid_name (name):
    return name in clients.keys ()

def is_a_valid_first_name (name, first_name):
    return first_name == clients [name]["Fname"]

def is_a_valid_passwd (name, password):
    return password == clients [name]["password"]

#La fonction "ask_identity" permet de demander à l'utilisateur de rentrer les codes du client.
def identity_is_valid (name, first_name, password):
    if is_a_valid_name (name) \
        and is_a_valid_first_name (name, first_name) \
        and is_a_valid_passwd (name, password):
        return True
    else:
        return False

def add_amount (amount, name):
    clients [name]["sold"] = clients [name]["sold"] + amount
    
def main ():  
    name = input ("name : ")
    first_name = input ("Fname : ")
    password =input ("password : ")
    if identity_is_valid (Name, Fname, password):
        print("Login succesfull!")
        #montant_a_deposer = float (input ("Entrez un montant: "))
        #add_amount (montant_a_deposer, "Canard")
        #write_in_json_file (clients, "toto.json")
        main_page(account)
    else:
        print("Login error, please try again.")
        main()


clients = opener()
main ()

"""
