import tools_file

virement = ["payment"]
sold = ["sold"]
retrait = ["withdrawal"]
quitting_words = ["quit", "Quit", "QUIT", "quit "]


#La fonction sld permet de retourner le solde du client
def sld ():
    for account in data:
        return account["sold"]

#La fonction old_withdrawal permet de retourner les anciens retraits du client
def old_withdrawal ():
    for account in data:
        return account["withdrawal"]
    
def new_sold_received ():
    if n > 0:
        sld = sld + n
    if n < 0:
        sld = sld + n 
    if n == 0:
        sld = sld + 0

def new_sold_given ():
    pass

def make_a_payment () :
    recipient = input("Enter the name of the recipient (enter 'quit' to cancel): ")
    payment_amount = input("Enter the amount you want to transfer (enter 'quit' to cancel): ")
    if recipient or payment_amount in quitting_words :
        go_to_payment_page
    else :
        input(f"Enter 1 to make a {payment_amount} € payment to {recipient}: \n"
                "Enter 2 to cancel")
        if input == 1 :
            pass
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


def go_to_withdrawal_page () :
    print (f"Your old withdrawals are {old_withdrawal}.\n")
           #entrez pin si vous voulez retirer argent)
    
def enter_pin ():
    print("enter your pin")
    if pin in correct_pin(account):
        pass
    # pin correct peut proceder a la suite donc choisir la valeur de withdraw

def vnew_sold ():
   value_to_withdraw = int(input("Enter the value you want to withdraw : "))
   print(sld-value_to_withdraw)

def exit_system():
    return main(account)

 

#La fonction main_page permet de demander ce que veux regarder le client sur son compte bancaire.
def main_page ():
    input(f"Hello {FName}, {Name}, what do you want to know about your bank account?\n"
          "sold\n"
          "payment\n"
          "withdrawal")
    if input in sold:
        go_to_sold_page()
    if input in virement:
        go_to_payment_page()
    if input in retrait:
        go_to_withdrawal_page()
    if input in quitting_words:
        exit_system()

#La fonction "ask_identity" permet de demander à l'utilisateur de rentrer les codes du client.
def ask_identity ():
    ask_name = input("name : ")
    ask_first_name = input("Fname : ")
    ask_password =input("password : ")
    if (ask_name == "" and ask_first_name == "" and ask_password):
        return True


#cette fonction permet de demander à l'utilisateur de réécrire ses codes s'il y a une erreur.
def re_ask_identity():
    return ask_identity

def main(account):
    if ask_identity == True:
        print("Login succesfull!")
        terminale(account)
    else:
        print("Login error, please try again.")
        re_ask_identity()