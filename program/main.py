
import tools_file

VIREMENT = ["payment", "virement"]
SOLDE = ["sold", "solde"]
RETRAIT = ["withdrawal", "retrait"]
QUITTING_WORDS = ["quit", "quitter", "exit", "annuler"]

CURRENT_ACCOUNT_KEY = None
CURRENT_ACCOUNT_DATA = None

def get_sold():
    """Retourne le solde de l'utilisateur connecté."""
    return CURRENT_ACCOUNT_DATA.get("sold", 0)

def get_old_withdrawals():
    """Retourne l'historique de retrait de l'utilisateur connecté."""
    return CURRENT_ACCOUNT_DATA.get("withdrawal", [])

def update_sold(amount):
    """Met à jour le solde du compte et le sauvegarde dans les données globales."""
    global CURRENT_ACCOUNT_DATA
    
    # 1. Vérification du compte
    if CURRENT_ACCOUNT_DATA is None or tools_file.DATA is None:
        print("Erreur: Aucun compte connecté ou données non chargées.")
        return False

    # 2. Mise à jour dans la variable locale
    CURRENT_ACCOUNT_DATA["sold"] += amount

    # 3. Mise à jour dans la structure de données globale (tools_file.DATA)
    tools_file.DATA[CURRENT_ACCOUNT_KEY] = CURRENT_ACCOUNT_DATA

    # 4. Sauvegarde dans le fichier
    tools_file.save_data(tools_file.DATA)
    return True

def make_a_payment():
    """Gère le flux de virement d'argent."""
    print("\n--- Page de Virement ---")
    recipient_key = input("Entrez la clé unique du destinataire (ex: 'canard') : ").strip()
    if recipient_key.lower() in QUITTING_WORDS: return go_to_main_page()

    try:
        payment_amount = float(input("Entrez le montant à virer : ").strip())
    except ValueError:
        print("Montant invalide. Annulation du virement.")
        return go_to_main_page()
    
    if payment_amount <= 0:
        print("Le montant doit être positif. Annulation.")
        return go_to_main_page()

    if recipient_key not in tools_file.DATA:
        print(f"Erreur: Le destinataire '{recipient_key}' n'existe pas.")
        return go_to_main_page()

    if recipient_key == CURRENT_ACCOUNT_KEY:
        print("Erreur: Vous ne pouvez pas vous faire un virement à vous-même.")
        return go_to_main_page()
        
    current_sold = get_sold()
    if current_sold < payment_amount:
        print("Solde insuffisant pour effectuer ce virement.")
        return go_to_main_page()
        
    # Confirmation
    confirm = input(f"Confirmer le virement de {payment_amount} € à {recipient_key} (oui/non) ? ").lower()
    if confirm != 'oui':
        print("Virement annulé.")
        return go_to_main_page()

    # Opérations: Retrait du compte courant
    if update_sold(-payment_amount):
        tools_file.DATA[recipient_key]["sold"] += payment_amount
        tools_file.save_data(tools_file.DATA)
    
        print("Virement effectué avec succès!")
    
    return go_to_main_page()


def make_a_withdrawal():
    print("\n--- Page de Retrait ---")
    
    if not enter_pin():
        print("Retrait annulé.")
        return go_to_main_page()

    try:
        amount_to_withdraw = float(input("Entrez le montant à retirer : ").strip())
    except ValueError:
        print("Montant invalide. Annulation du retrait.")
        return go_to_main_page()

    if amount_to_withdraw <= 0:
        print("Le montant doit être positif. Annulation.")
        return go_to_main_page()

    current_sold = get_sold()
    if current_sold < amount_to_withdraw:
        print("Solde insuffisant. Vous seriez dans le rouge.")
        # Laisse la décision d'autoriser le rouge au système bancaire, ici on bloque
        return go_to_main_page()
    
    # Opération: Retrait du solde
    if update_sold(-amount_to_withdraw):
        print(f"Retrait de {amount_to_withdraw} € effectué. Nouveau solde: {get_sold()} €")
    
    return go_to_main_page()

def go_to_sold_page():
    """Affiche le solde."""
    print(f"\n--- Solde de {CURRENT_ACCOUNT_DATA.get('Fname')} {CURRENT_ACCOUNT_DATA.get('Name')} ---")
    print(f"Votre solde actuel est de: {get_sold()} €")
    input("\nAppuyez sur ENTRÉE pour continuer...")
    return go_to_main_page()

def go_to_withdrawal_page():
    """Affiche l'historique de retrait et propose un retrait."""
    print(f"\n--- Historique de Retraits ---")
    withdrawals = get_old_withdrawals()
    if not withdrawals:
        print("Aucun retrait trouvé dans l'historique.")
    else:
        for w in withdrawals:
            print(f"- {w.get('montant')} € le {w.get('date')} (de: {w.get('from')})")
    
    print("\nSouhaitez-vous effectuer un NOUVEAU RETRAIT ?")
    choice = input("Entrez 'oui' pour commencer un retrait, ou ENTRÉE pour revenir : ").lower().strip()
    
    if choice == 'oui':
        return make_a_withdrawal()
    else:
        return go_to_main_page()

def go_to_payment_page():
    """Page d'accueil des virements."""
    print("\n--- Menu Virement ---")
    print("1. Effectuer un virement")
    print("2. Retour au menu principal")
    
    choice = input("Votre choix (1 ou 2) : ").strip()
    
    if choice == "1":
        return make_a_payment()
    elif choice == "2":
        return go_to_main_page()
    else:
        print("Choix invalide.")
        return go_to_payment_page()

def enter_pin():
    MAX_ATTEMPTS = 3
    for attempt in range(1, MAX_ATTEMPTS + 1):
        pin_attempt = input(f"Entrez votre code PIN (Tentative {attempt}/{MAX_ATTEMPTS}) : ")
        if tools_file.check_pin(pin_attempt, CURRENT_ACCOUNT_DATA):
            print("Code PIN correct.")
            return True
        print("Code PIN incorrect.")
    print("\n Code PIN bloqué après plusieurs tentatives échouées.")
    return False

def exit_system():
    print("\n Déconnexion et fermeture du système. Au revoir!")
    global CURRENT_ACCOUNT_KEY, CURRENT_ACCOUNT_DATA
    CURRENT_ACCOUNT_KEY = None
    CURRENT_ACCOUNT_DATA = None
    main()

def ask_identity():
    print("\n--- CONNEXION ---")
    name = input("Nom : ").strip()
    first_name = input("Prénom : ").strip()
    password = input("Mot de passe : ").strip()
    
    
    global CURRENT_ACCOUNT_KEY, CURRENT_ACCOUNT_DATA
    
    key, data = tools_file.get_account_by_identity(name, first_name, password)

    if key and data:
        CURRENT_ACCOUNT_KEY = key
        CURRENT_ACCOUNT_DATA = data
        return True
    else:
        return False

def go_to_main_page():
    """Menu principal après connexion."""
    if CURRENT_ACCOUNT_DATA is None:
        return

    fname = CURRENT_ACCOUNT_DATA.get("Fname", "Client")
    name = CURRENT_ACCOUNT_DATA.get("Name", "")
    
    print(f"\nBonjour **{fname} {name}**, que souhaitez-vous faire ?")
    print("-------------------------------------------------")
    print("Options disponibles: **SOLDE**, **VIREMENT**, **RETRAIT**, **QUITTER**")
    
    user_input = input("Entrez votre choix : ").lower().strip()
    
    # Traitement de l'entrée
    if user_input in SOLDE:
        return go_to_sold_page()
    elif user_input in VIREMENT:
        return go_to_payment_page()
    elif user_input in RETRAIT:
        # Demande du PIN avant de procéder au retrait
        return go_to_withdrawal_page()
    elif user_input in QUITTING_WORDS:
        return exit_system()
    else:
        print("Option non reconnue. Veuillez réessayer.")
        return go_to_main_page()


# --- Point d'Entrée Principal ---

def main():
    """Fonction principale pour gérer le flux de l'application."""
    
    if tools_file.DATA is None:
        if not tools_file.load_data():
            print("Le système ne peut pas démarrer sans données valides.")
            return

    # Boucle d'authentification
    while CURRENT_ACCOUNT_DATA is None:
        if ask_identity():
            print("Connexion réussie!")
            # Démarre le menu principal après connexion
            go_to_main_page()
        else:
            print("Erreur de connexion. Nom, Prénom ou Mot de passe incorrect.")

if __name__ == "__main__":
    main()