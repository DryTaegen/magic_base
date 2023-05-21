import sqlite3 as sq
import datetime as dt
from PIL import Image

def connect_database(database_name):
    #Wil open a session with the database.
    db = sq.connect(database_name)
    print(f"Connected to server. sqlite version: {sq.version}")
    return db

def disconnect_database(database):
    #Will ask if the user wishes to save changes before quitting
    cont = True
    while cont:
        inp = input("Do you wish to save your changes? [Y,N] ")
        if inp.upper() == "Y":
            database.commit()
            cont = False
        elif inp.upper() == "N":
            cont = False
        else:
            print(f"Sorry, {inp} was not recognized.")
    database.close()

def add_card(database, card_name, card_image, date_time):
    #Will take the two required parameters for a card and add them to the card table.'
    values = (card_name, card_image, 0, date_time)
    statement = '''INSERT INTO card(card_name, card_image, num_of_uses, last_update)
                    VALUES(?,?,?,?)'''
    cursor = database.cursor()
    cursor.execute(statement, values)

def delete_card(database, card_name):
    #Will find the card matching the inputted name and remove it from the list.
    statement = '''DELETE FROM card WHERE card_name=?'''
    cursor = database.cursor()
    cursor.execute(statement, (card_name,))
    statement = '''DELETE FROM deck_has_card WHERE card_name=?'''
    cursor = database.cursor()
    cursor.execute(statement, (card_name,))

def make_deck(database, deck_name, date_time):
    #Will take the name of the deck, create a new row in the table, then call, insert_cards 
    #until the user is satisfied
    values = (deck_name, date_time)
    statement = '''INSERT INTO decks(deck_name, last_update)
                    VALUES(?,?)'''
    cursor = database.cursor()
    cursor.execute(statement, values)
    insert_cards(database, deck_name)

def delete_deck(database, deck_name):
    #will take the user input and find the deck matching the name and delete it. 
    cursor = database.cursor()
    cursor.execute("SELECT deck_id FROM decks WHERE deck_name=?", (deck_name,))
    deck_id = cursor.fetchone()
    statement = '''DELETE FROM decks WHERE deck_name=?'''
    cursor.execute(statement, (deck_name,))
    statement = '''DELETE FROM deck_has_card WHERE deck_id=?'''
    cursor = database.cursor()
    cursor.execute(statement, (deck_id[0],))

def insert_cards(database, deck_name):
    #Runs the process of adding cards to the given deck until the user quits.
    continue_process = True
    while continue_process:
        cursor = database.cursor()
        add_card = input("Type the name of the card you want to add, press 'q' to quit: ")
        if add_card == 'q':
            continue_process = False
        else:
            cursor.execute("SELECT * FROM card WHERE card_name=?", (add_card,))
            card = cursor.fetchone()
            statement = '''INSERT INTO deck_has_card(deck_id, card_name, last_update)
                            VALUES(?,?,?)'''
            cursor.execute("SELECT deck_id FROM decks WHERE deck_name=?", (deck_name,))
            deck_id = cursor.fetchone()
            cursor.execute(statement, (deck_id[0], card[0], dt.datetime.now()))

def remove_cards(database, deck_name):
    #Runs the process of removing cards from the given deck until the user quits.
    statement = '''DELETE FROM deck_has_card WHERE deck_id=? AND card_name=?'''
    cursor = database.cursor()
    cursor.execute("SELECT deck_id FROM decks WHERE deck_name=?",(deck_name,))
    deck_id = cursor.fetchone()
    remove_card = input("Type the name of the card you want to remove: ")
    cursor.execute("SELECT card_name FROM card WHERE card_name=?", (remove_card,))
    card_name = cursor.fetchone()
    cursor.execute(statement, (deck_id[0], card_name[0]))

def get_deck(database, deck_name):
    #Gets the list of cards in a deck
    cursor = database.cursor()
    select = '''SELECT c.card_name FROM card c 
                INNER JOIN deck_has_card dhc 
                ON c.card_name = dhc.card_name 
                INNER JOIN decks d 
                ON dhc.deck_id = d.deck_id
                WHERE d.deck_name =?'''
    cursor.execute(select, (deck_name,))
    cards = cursor.fetchall()
    for card in cards:
        print(card)

def get_card_image(database, card_name):
    #gets the image of a given card.
    cursor = database.cursor()
    cursor.execute("SELECT card_image FROM card WHERE card_name=?", (card_name,))
    path = cursor.fetchone()
    image = Image.open(path[0])
    image.show()

def main_menu(db):
    cont = True
    while cont == True:
        print("Welcome to magic base. Type the number of the option you want: ")
        print("1: Add card, 2: Add deck, 3: print deck list, 4: Display a card, 0: leave,")
        print("5: delete a card, 6: delete a deck,")
        print("7: add cards to a deck 8: remove cards from a deck.")
        choice = input(" > ")
        if choice == "1":
            add_card_menu(db)
        elif choice == "2":
            make_deck_menu(db)
        elif choice == "3":
            deck_name = input("What deck do you want? ")
            get_deck(db, deck_name)
        elif choice == "0":
            cont = False
        elif choice == "4":
            card_name = input("What's the name of the card you want to search: ")
            get_card_image(db, card_name)
        elif choice == "5":
            delete_card_menu(db)
        elif choice == "6":
            delete_deck_menu(db)
        elif choice == "7":
            insert_cards_menu(db)
        elif choice == "8":
            remove_cards_menu(db)

def add_card_menu(db):
    name = input("Type the name of the card: ")
    image = input("Type the path of the image of the card: ")
    add_card(db, name, image, dt.datetime.now())

def delete_card_menu(db):
    name = input("Type the name of the card you want removed: ")
    delete_card(db, name)

def make_deck_menu(db):
    deck_name = input("Name your new deck: ")
    make_deck(db,deck_name, dt.datetime.now())

def delete_deck_menu(db):
    deck = input("What deck do you want deleted: ")
    delete_deck(db, deck)
def insert_cards_menu(db):
    deck = input("What deck do you want to add cards to: ")
    insert_cards(db, deck)
def remove_cards_menu(db):
    deck = input("What deck do you want to remove cards from: ")
    remove_cards(db, deck)



def main():
    database = "database\magicBase.db"

    db = connect_database(database)
    main_menu(db)
    disconnect_database(db)


main()

