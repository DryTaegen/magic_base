import sqlite3 as sq
import datetime as dt
from PIL import Image
import requests
from io import BytesIO
import pymongo
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog

def connect_database(database_name, host):
    #Wil open a session with the database.
    client = pymongo.MongoClient(host)
    db = client[database_name]
    print(f"Connected to server.")
    return db


def add_card(database, card_name, date_time):
    card_list = Card.where(name = card_name).all()
    
    print(f"Type the number corresponding to the version of {card_name} you want: ")
    i = 0
    for c in card_list:
        print(f"{i}: {c.name}: set: {c.set}")
        i += 1
    count = int(input("> "))
    card = card_list[count]

    cards = database["cards"]    
    card_dict = {"name":card.name,"date added":date_time ,"image url":card.image_url ,"uses": 0}

    ins = cards.insert_one(card_dict)
    

def delete_card(database, card_name):
    cards = database["cards"]
    query = {"name": card_name}
    cards.delete_one(query)


def make_deck(database, deck_name, date_time):
    decks = database["decks"]    
    deck_dict = {"name":deck_name,"date added":date_time}
    ins = decks.insert_one(deck_dict)

    insert_cards(database, deck_name)

def delete_deck(database, deck_name):
    cards = database["cards"]
    decks = database["decks"]
    containers = database["deck_has_cards"]
    query = {"name": deck_name}

    decks.delete_one(query)

    containers_query = {deck_name: { "$regex": ".*" }}
    removal = containers.find(containers_query)
    for card in removal:
        card_query = {"name": card[deck_name]}
        card = cards.find(card_query)
        decrement = card[0]["uses"] - 1
        decrease = { "$set": {"uses": decrement}}
        cards.update_one(card_query, decrease)

    containers.delete_many(containers_query)

def insert_cards(database, deck_name):
    #Runs the process of adding cards to the given deck until the user quits.
    containers = database["deck_has_cards"]
    decks = database["decks"]
    cards = database["cards"]
    deck_query = {"name": deck_name	}
    
    continue_process = True
    while continue_process:
        print("Type the name of card that you want to add ('q' to quit) ")
        query = input("> ")
        if query.lower() == 'q':
            continue_process = False
            continue
        try:
            #Add card and deck pairs
            card_query = {"name": query}
            card = cards.find(card_query)
            deck = decks.find(deck_query)
            contain_pair = {deck[0]["name"]: card[0]["name"]}
            x = containers.insert_one(contain_pair)

            #increase the use of cards
            increment = card[0]["uses"] + 1
            increase = { "$set": {"uses": increment}}
            cards.update_one(card_query, increase)
        except:
            print(f"{query} was not found in the database.")
            continue

        


def remove_cards(database, deck_name):
    #Runs the process of removing cards from the given deck until the user quits.
    containers = database["deck_has_cards"]
    cards = database["cards"]
    continue_process = True
    while continue_process:
        print("Type the name of card that you want to remove ('q' to quit) ")
        remove_card = input("> ")
        if remove_card.lower() == 'q':
            continue_process = False
            continue
        try:
            query = {deck_name: remove_card}

            containers.delete_one(query)

            card_query = {"name": remove_card}
            card = cards.find(card_query)
            decrement = card[0]["uses"] - 1
            decrease = { "$set": {"uses": decrement}}
            cards.update_one(card_query, decrease)
        except:
            print(f"{remove_card} was not found in {deck_name}")
        

def get_deck(database, deck_name):
    containers = database["deck_has_cards"]
    query = {deck_name: { "$regex": ".*" }}

    deck = containers.find(query)

    for c in deck:
        print(c[deck_name])

def get_card_image(database, card_name):
    cards = database["cards"]
    query = {"name": card_name}
    card = cards.find(query)
    url = card[0]["image url"]
    response = requests.get(url, verify=False)
    img= Image.open(BytesIO(response.content))
    img.show()

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
    add_card(db, name, dt.datetime.now())

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
    database_name = "magicbase"
    host = "mongodb://localhost:27017"

    db = connect_database(database_name, host)
    main_menu(db)


main()

