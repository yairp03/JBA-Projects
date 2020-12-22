import random
import sqlite3
from os import path

CREATE = 1
LOGIN = 2
EXIT = 0

SHOW_BALANCE = 1
ADD_INCOME = 2
DO_TRANSFER = 3
CLOSE_ACCOUNT = 4
LOGOUT = 5

PIN = 'pin'
BALANCE = 'balance'

MAIN_MENU = 1
USER_MENU = 2


class Bank:

    def __init__(self, db_file, user_id_len=9, pin_len=4):
        """
        :type db_file: str
        :type user_id_len: int
        :type pin_len: int
        """
        db_exists = False
        if path.exists(db_file):
            db_exists = True
        self._conn = sqlite3.connect(db_file)
        self._cur = self._conn.cursor()
        if not db_exists:
            self._create_db()

        self.user_id_len = user_id_len
        self.pin_len = pin_len

    def _create_db(self):
        """
        Creates db's 'card' table
        :return: None
        """
        self._exec_and_update(
            'CREATE TABLE card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')

    def _exec_and_update(self, query):
        """
        Execute an sql query on the database
        :param query: the query to execute
        :type query: str
        :return: None
        """
        self._cur.execute(query)
        self._conn.commit()

    def _exec_and_data(self, query):
        """
        Execute an sql query on the database and returns the data given
        :param query: the query to execute
        :type query: str
        :return: data from database
        :rtype: str
        """
        self._cur.execute(query)
        return self._cur.fetchall()

    def create_account(self):
        """
        Creates a new account
        :return: card number and pin
        :rtype: tuple
        """
        while self._card_exists(card_number := self._generate_card_number()):
            continue
        pin = self._generate_pin()
        self._insert_card(card_number, pin)
        return card_number, pin

    def _insert_card(self, card, pin):
        """
        Inserts a card into the database
        :param card: card field
        :param pin: pin field
        :type card: str
        :type pin: str
        :return: None
        """
        self._exec_and_update(f"INSERT INTO card (number, pin) VALUES ({card}, {pin});")

    def _card_exists(self, card):
        """
        Checks if a card is exists in the banking system
        :param card: card number to check
        :type card: str
        :return: if card exists
        :rtype: bool
        """
        if (exists := len(self._exec_and_data(f'SELECT * FROM card WHERE number = {card};'))) > 1:
            self._db_error()
        return exists == 1

    def _db_error(self):
        """
        Raises a db exception
        :return: None
        """
        raise Exception('DB has more than one rows with the same card number')

    def login(self, card, pin):
        """
        Checks if credentials are right
        :param card: card number
        :param pin: card's pin
        :type card: str
        :type pin: str
        :rtype: bool
        """
        if (correct := len(self._exec_and_data(f"SELECT * FROM card WHERE number = {card} AND pin = {pin};"))) > 1:
            self._db_error()
        return correct == 1

    def get_card_balance(self, card):
        """
        Gets a card's balance
        :param card: card number
        :type card: str
        :return: card's balance
        :rtype: int
        :raises KeyError: if card not exists
        """
        if not self._card_exists(card):
            raise KeyError('Card not exists')
        return self._exec_and_data(f"SELECT balance FROM card WHERE number = {card};")[0][0]

    def _generate_card_number(self):
        """
        Generates a new card number
        :return: new card number
        :rtype: str
        """
        card = '400000' + str(random.randint(0, 10 ** self.user_id_len - 1)).rjust(self.user_id_len, '0')
        card += str(self._calc_checksum(card))
        return card

    def add_money(self, card, money):
        """
        Adds money to an account
        :param card: card number
        :param money: money to add
        :type card: str
        :type money: int
        :return: None
        """
        self._exec_and_update(f"UPDATE card SET balance = balance + {money} WHERE number = {card}")

    def take_money(self, card, money):
        """
        Takes money to an account
        :param card: card number
        :param money: money to take
        :type card: str
        :type money: int
        :return: None
        """
        self._exec_and_update(f"UPDATE card SET balance = balance - {money} WHERE number = {card}")

    def do_transfer(self, withdraw):
        """
        Transfers money from the first account to the second
        :param withdraw: withdraw account's card number
        :type withdraw: str
        :return: None
        """
        print('Transfer')
        deposit = input('Enter card number:\n')
        w_balance = self.get_card_balance(withdraw)
        if withdraw == deposit:
            print("You can't transfer money to the same account!")
        elif deposit[:-1] + str(self._calc_checksum(deposit[:-1])) != deposit:
            print('Probably you made mistake in the card number. Please try again!')
        elif not self._card_exists(deposit):
            print('Such a card does not exist.')
        else:
            amount = int(input('Enter how much money you want to transfer:\n'))
            if amount > w_balance:
                print('Not enough money!')
            else:
                self.take_money(withdraw, amount)
                self.add_money(deposit, amount)
                print('Success!')

    def close_account(self, card):
        """
        Closes an account
        :param card: account's card number
        :type card: str
        :return: None
        """
        self._exec_and_update(f"DELETE FROM card WHERE number = {card}")

    @staticmethod
    def _calc_checksum(card):
        """
        Calculates the card's fitting checksum according to Luhn Algorithm
        :param card: card number to calculate his checksum
        :type card: str
        :return: the checksum
        :rtype: int
        """
        numbers = list(map(int, list(str(card))))
        numbers = [x[1] * ((x[0] + 1) % 2 + 1) for x in enumerate(numbers)]
        numbers = [i - 9 if i > 9 else i for i in numbers]
        return (10 - (sum(numbers) % 10)) % 10

    def _generate_pin(self):
        """
        Generates a random pin
        :return: new pin number
        :rtype: str
        """
        return str(random.randint(0, 10 ** self.pin_len - 1)).rjust(self.pin_len, '0')


def main():
    bank = Bank('card.s3db')
    print_menu()
    option = int(input())
    print()
    while option != EXIT:
        if option == CREATE:
            create_account(bank)
        elif option == LOGIN:
            card = login(bank)
            if card:
                handle_account(bank, card)
        print_menu()
        option = int(input())
        print()
    bye()


def login(bank):
    """
    try to login to the bank system
    :param bank: the bank system
    :type bank: Bank
    :return: card number if login successfully else None
    :rtype: str
    """
    card = input('Enter your card number:\n')
    pin = input('Enter your PIN:\n')
    print()
    if bank.login(card, pin):
        print('You have successfully logged in!', end='\n\n')
        return card
    print('Wrong card number or PIN!', end='\n\n')
    return None


def handle_account(bank, card):
    """
    Handles a logged in user
    :param bank: the bank system
    :param card: logged in user's card number
    :type bank: Bank
    :type card: str
    :return: None
    """
    print_menu(USER_MENU)
    option = int(input())
    print()
    while option not in (CLOSE_ACCOUNT, LOGOUT):
        if option == SHOW_BALANCE:
            print('Balance: ' + str(bank.get_card_balance(card)), end='\n\n')
        elif option == ADD_INCOME:
            money = int(input('Enter income:\n'))
            bank.add_money(card, money)
            print('Income was added!', end='\n\n')
        elif option == DO_TRANSFER:
            bank.do_transfer(card)
        elif option == EXIT:
            bye()
        print_menu(USER_MENU)
        option = int(input())
        print()
    if option == CLOSE_ACCOUNT:
        bank.close_account(card)
        print('The account has been closed!', end='\n\n')
    elif option == LOGOUT:
        print('You have successfully logged out!', end='\n\n')


def create_account(bank):
    """
    Creates a new account and print his details
    :param bank: the bank system
    :type bank: Bank
    :return: None
    """
    card, pin = bank.create_account()
    print(f"""\
Your card has been created
Your card number:
{card}
Your card PIN:
{pin}""", end='\n\n')


def bye():
    print('Bye!')
    exit()


def print_menu(menu=MAIN_MENU):
    """
    Prints a menu
    :param menu: which menu to print (default: the main menu)
    :type menu: int
    :return: None
    """
    if menu == MAIN_MENU:
        print("""\
1. Create an account
2. Log into account
0. Exit""")
    elif menu == USER_MENU:
        print("""\
1. Balance
2. Add income
3. Do transfer
4. Close Account
5. Log out
0. Exit""")


if __name__ == '__main__':
    main()
