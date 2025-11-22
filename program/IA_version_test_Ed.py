# main.py

import datetime
import sys # Importé pour la sortie du programme
from tools_file import load_data_from_json, write_in_json_file
from data import quitting_words

# Constantes utilisées dans le programme
DATA_FILE = "data.json"
NOTES = [500, 200, 100, 50, 20, 10, 5]

class BankManager:
    """
    Gère les opérations de la banque.
    """

    def __init__(self):
        """Initialise le gestionnaire de banque."""
        self.clients_data = {}
        self.current_user_name = None
        self._load_clients_data()

    def _load_clients_data(self):
        """Charge les données des clients au démarrage du programme."""
        try:
            self.clients_data = load_data_from_json(DATA_FILE)
            print("Client data loaded successfully.")
        except FileNotFoundError:
            print("Error: data.json file not found. Cannot start the bank program.")
            self.clients_data = {}
        except Exception as e:
            print(f"Error loading data: {e}")
            self.clients_data = {}

    def _save_clients_data(self):
        """Sauvegarde les données des clients dans le fichier JSON."""
        write_in_json_file(self.clients_data, DATA_FILE)

    # --- Fonctions de lecture/écriture du solde (renommées) ---

    def get_sold(self):
        """Retourne le solde du client actuel (anciennement get_sold)."""
        if self.current_user_name:
            return self.clients_data[self.current_user_name]["sold"]
        return 0

    def set_sold(self, new_value):
        """Met à jour le solde du client actuel et sauvegarde les données (anciennement set_sold)."""
        if self.current_user_name in self.clients_data:
            self.clients_data[self.current_user_name]["sold"] = new_value
            self._save_clients_data()
        else:
            print("Error: Current user not identified for setting sold.")

    # --- Authentification (noms conservés) ---

    def is_a_valid_name(self, name):
        """Vérifie si le nom de famille existe dans les données."""
        return name in self.clients_data

    def is_a_valid_first_name(self, name, first_name):
        """Vérifie si le prénom correspond au nom de famille."""
        # Comparaison insensible à la casse et sans espaces
        return self.clients_data[name]["Fname"].strip().lower() == first_name.strip().lower()

    def is_a_valid_passwd(self, name, password):
        """Vérifie si le mot de passe correspond au nom de famille."""
        return self.clients_data[name]["password"] == password

    def identity_is_valid(self, name, first_name, password):
        """Vérifie si l'identité complète est valide."""
        if self.is_a_valid_name(name):
            return self.is_a_valid_first_name(name, first_name) and self.is_a_valid_passwd(name, password)
        return False

    def handle_login(self):
        """Gère le processus de connexion de l'utilisateur."""
        if not self.clients_data:
            print("Bank service currently unavailable (no client data).")
            return False

        print("\n--- Login ---")
        name = input("Last Name: ").strip()
        first_name = input("First Name: ").strip()
        password = input("Password: ")

        if self.identity_is_valid(name, first_name, password):
            self.current_user_name = name
            print("Login successful! Welcome.")
            return True
        else:
            print("Login error: Invalid credentials, please try again.")
            return False

    # --- 3. Consultation du Solde (renommée) ---

    def go_to_sold_page(self):
        """Affiche le solde du client actuel (anciennement show_balance)."""
        balance = self.get_sold()
        print(f"\n💰 Your current balance is: {balance} €")

    # --- 1. Virement Bancaire (renommée) ---

    def go_to_payment_page(self):
        """Gère un virement vers un autre client de la banque (anciennement make_transfer)."""
        print("\n--- Bank Transfer ---")

        recipient_name = input("Enter the recipient's Last Name (or 'quit'): ").strip()
        if recipient_name.lower() in quitting_words: return

        if recipient_name not in self.clients_data:
            print("Error: Recipient not found in the bank.")
            return

        if recipient_name == self.current_user_name:
            print("Error: Cannot transfer money to your own account.")
            return

        while True:
            try:
                amount_str = input("Enter the amount to transfer (or 'quit'): ").strip()
                if amount_str.lower() in quitting_words: return

                amount = int(amount_str)
                if amount <= 0:
                    print("Transfer amount must be positive.")
                    continue

                current_sold = self.get_sold()
                if amount > current_sold:
                    print(f"Insufficient funds! Your balance is {current_sold} €.")
                    return

                if not self._check_pin():
                    print("Transfer canceled due to incorrect PIN.")
                    return

                # 1. Mise à jour de l'émetteur (utilise set_sold)
                self.set_sold(current_sold - amount)

                # 2. Mise à jour du destinataire (doit modifier directement car set_sold agit sur l'utilisateur courant)
                recipient_sold = self.clients_data[recipient_name]["sold"]
                self.clients_data[recipient_name]["sold"] = recipient_sold + amount

                # 3. Enregistrement des transactions (historique)
                self._log_transaction(
                    self.current_user_name,
                    "payement",
                    amount,
                    to=self.clients_data[recipient_name]["Fname"] + " " + recipient_name
                )
                self._log_transaction(
                    recipient_name,
                    "deposit",
                    amount,
                    from_source="Transfer from " + self.clients_data[self.current_user_name]["Fname"] + " " + self.current_user_name
                )

                self._save_clients_data() # Sauvegarde après modification du destinataire et logs
                self.go_to_sold_page()
                break

            except ValueError:
                print("Invalid input. Please enter a whole number for the amount.")

    # --- 2. Retrait GAB (renommée) ---

    def go_to_withdrawal_page(self):
        """Gère un retrait avec sélection de décomposition de billets (anciennement make_withdrawal)."""
        print("\n--- ATM Withdrawal ---")

        while True:
            try:
                amount_str = input("Enter the amount to withdraw (multiple of 5, or 'quit'): ").strip()
                if amount_str.lower() in quitting_words: return

                amount = int(amount_str)

                if amount <= 0 or amount % 5 != 0:
                    print("Withdrawal amount must be a positive multiple of 5.")
                    continue

                current_sold = self.get_sold()
                if amount > current_sold:
                    print(f"Insufficient funds! Your balance is {current_sold} €.")
                    return

                if not self._check_pin():
                    print("Withdrawal canceled due to incorrect PIN.")
                    return

                if not self._offer_denominations(amount):
                    return

                # Effectuer le retrait
                self.set_sold(current_sold - amount)

                # Enregistrement de la transaction
                self._log_transaction(
                    self.current_user_name,
                    "withdrawal",
                    amount,
                    from_source="ATM Withdrawal"
                )

                self.go_to_sold_page()
                break

            except ValueError:
                print("Invalid input. Please enter a whole number.")

    # --- 4. Dépôt d'Argent (renommée) ---

    def add_amount(self):
        """Permet à l'utilisateur de déposer de l'argent (anciennement make_deposit)."""
        print("\n--- Deposit ---")
        while True:
            try:
                amount_str = input("Enter the amount to deposit (or 'quit'): ").strip()
                if amount_str.lower() in quitting_words: return

                deposit_amount = int(amount_str)
                if deposit_amount <= 0:
                    print("Deposit amount must be positive.")
                    continue

                # Mise à jour du solde
                current_sold = self.get_sold()
                self.set_sold(current_sold + deposit_amount)

                # Enregistrement de la transaction
                self._log_transaction(
                    self.current_user_name,
                    "deposit",
                    deposit_amount,
                    from_source="ATM Deposit"
                )

                self.go_to_sold_page()
                break

            except ValueError:
                print("Invalid input. Please enter a whole number.")

    # --- Fonctions Utilitaires (internes, noms conservés) ---

    def _check_pin(self):
        """Vérifie le PIN de l'utilisateur actuel (3 tentatives)."""
        pin_attempts = 3
        correct_pin_str = str(self.clients_data[self.current_user_name]["pin"])

        print("\n> Please confirm with your PIN to proceed (3 attempts).")
        for i in range(pin_attempts):
            attempt = input("PIN: ").strip()

            if attempt == correct_pin_str:
                return True
            else:
                remaining_attempts = pin_attempts - (i + 1)
                if remaining_attempts > 0:
                    print(f"Wrong PIN, {remaining_attempts} attempts left.")
                else:
                    print("Wrong PIN. Too many failed attempts.")
                    return False

        return False

    def _log_transaction(self, user_name, transaction_type, amount, to=None, from_source=None):
        """Enregistre une transaction dans l'historique du client."""
        client = self.clients_data[user_name]
        if transaction_type not in client:
            client[transaction_type] = []

        log_entry = {
            "montant": amount,
            "date": str(datetime.date.today()),
        }
        if to:
            log_entry["to"] = to
        if from_source:
            log_entry["from"] = from_source

        client[transaction_type].append(log_entry)
        self._save_clients_data()

    def _get_denominations(self, amount, max_combinations=4):
        """Calcule jusqu'à 4 décompositions possibles en billets."""
        combinations = []
        # [Implementation des stratégies de décomposition de billets...]
        remaining = amount
        combo1 = {}
        for note in NOTES:
            count = remaining // note
            if count > 0:
                combo1[note] = count
                remaining -= count * note
        if remaining == 0:
            combinations.append(combo1)

        # (Les autres stratégies sont omises ici pour la concision, mais elles sont conservées
        # pour garantir 4 choix différents comme dans le code précédent.)
        if amount >= 100 and len(combinations) < max_combinations:
            remaining = amount
            combo2 = {}
            temp_amount = amount
            for note in [500, 200, 100]:
                count = temp_amount // note
                used = max(0, count // 2)
                if used > 0:
                    combo2[note] = used
                    temp_amount -= used * note
            remaining = temp_amount
            for note in [50, 20, 10, 5]:
                count = remaining // note
                if count > 0:
                    combo2[note] = combo2.get(note, 0) + count
                    remaining -= count * note
            if remaining == 0 and combo2 not in combinations and sum(combo2.values()) > 0:
                combinations.append(combo2)

        if amount >= 20 and len(combinations) < max_combinations:
            remaining = amount
            combo3 = {}
            count_20 = remaining // 20
            combo3[20] = count_20
            remaining -= count_20 * 20
            for note in [10, 5]:
                count = remaining // note
                if count > 0:
                    combo3[note] = count
                    remaining -= count * note
            if remaining == 0 and combo3 not in combinations and sum(combo3.values()) > 0:
                combinations.append(combo3)

        if amount >= 50 and len(combinations) < max_combinations:
            remaining = amount
            combo4 = {}
            for note in [50, 20, 10, 5]:
                count = remaining // note
                if count > 0:
                    combo4[note] = count
                    remaining -= count * note
            if remaining == 0 and combo4 not in combinations and sum(combo4.values()) > 0:
                combinations.append(combo4)

        return combinations[:max_combinations]

    def _offer_denominations(self, amount):
        """Présente les propositions de billets à l'utilisateur et gère le choix."""
        combinations = self._get_denominations(amount)

        if not combinations:
            print("Error: Could not find any note decomposition. Withdrawal canceled.")
            return False

        print("\nAvailable note decompositions (Select 1 to {}):".format(len(combinations)))

        for i, combo in enumerate(combinations):
            notes_str = ", ".join([f"{count}x{note}€" for note, count in sorted(combo.items(), reverse=True)])
            print(f"{i + 1}. {notes_str}")
        print(f"{len(combinations) + 1}. Cancel withdrawal")

        while True:
            try:
                choice_str = input("Enter your choice: ").strip()

                if choice_str.lower() in quitting_words or choice_str == str(len(combinations) + 1):
                    print("Selection canceled.")
                    return False

                choice_index = int(choice_str) - 1
                if 0 <= choice_index < len(combinations):
                    print(f"\nDispensing {amount} € using option {choice_index + 1}.")
                    return True
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {len(combinations) + 1}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    # --- Menu Principal ---

    def main_page(self):
        """Affiche le menu principal et gère les choix de l'utilisateur."""

        first_name = self.clients_data[self.current_user_name]["Fname"]
        last_name = self.current_user_name

        while True:
            print(f"\n--- Hello {first_name} {last_name}, what do you want to do? ---")
            # Utilisation des nouveaux noms de fonctions pour le menu
            print("1. Make a Transfer (Faire un virement)")
            print("2. Make a Withdrawal (Faire un retrait)")
            print("3. View Balance (Consulter le solde)")
            print("4. Make a Deposit (Déposer de l'argent)")
            print("5. Logout / Exit (Se déconnecter/Quitter le programme)")

            next_action = input("Enter your choice (1-5): ").strip()

            if next_action == '1':
                self.go_to_payment_page()
            elif next_action == '2':
                self.go_to_withdrawal_page()
            elif next_action == '3':
                self.go_to_sold_page()
            elif next_action == '4':
                self.add_amount()
            elif next_action == '5':
                print("\n👋 Thank you for using our services. Goodbye!")
                self.current_user_name = None
                return

    def run(self):
        """Lance la boucle principale du programme."""
        if not self.clients_data:
            print("Program cannot run without client data.")
            sys.exit(1)

        while True:
            if self.handle_login():
                self.main_page()

# Fin de la classe BankManager

def main():
    """Fonction principale pour instancier et lancer le BankManager."""
    manager = BankManager()
    manager.run()

if __name__ == "__main__":
    main()