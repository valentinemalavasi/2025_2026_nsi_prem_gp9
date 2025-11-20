# 2025_2026_nsi_prem_gp9
1ere 2
MALAVASI Valentine
LEFAUCONNIER--MARINI Edgar
NEPLAZ Giulio

TOTO'S BANK

Utilisation manual
Welcome to Toto bank. Here’s our user guide to help you understand our human to machine interface.
Our system gives you the possibility to:
-	consult your bank account (sold, withdrawals and payments)
-	retreat money
-	make a payment to another user
Each step to every action is indicated by our Toto interface.
⮚	To connect to your bank account, please enter your name, for name and password as indicated
⮚	If the connection fails, please check your password and try again
⮚	Once connected, enter the number associated to the action you would like to do, as indicated on the main menu
⮚	To make a payment or withdrawal, please enter your pin when asked
⮚	If the payment or withdrawal fails, please check your pin and try again
To exit the system, you can type ‘quit’ at any time

We thank you for having chosen to trust our company, Toto bank wishes you a great day !

Dev Licence

This project is the foundation of an Automatic Money Distributor system for Toto’s Bank. For its operation, the main function asks the user to enter their information, such as name and password. Once entered, this information is sent to another function that checks whether it exists in the database.
If the client’s information is false or corrupted, the checking function returns to the main function, which asks for the information again.
If the information is correct, the system offers different options: making a withdrawal or making a payment.

Withdrawal
For a withdrawal, the function asks the user how much they want to withdraw.
If the amount is not divisible by 5 or 10,
if it contains a decimal point or digits after the decimal,
or if the client does not have enough funds in their account, then the operation is refused.
Otherwise, the system breaks down the amount into banknotes and returns to the user different possible distributions of bills.

Payment
For a payment, the function asks the user to enter the amount and the recipient.
If the amount is valid (with a maximum of two digits after the decimal point)
and if the client has sufficient funds in their account, then the system transfers the money to the specified person.
