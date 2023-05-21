# Overview


This software allows the user to store cards into their collection and then make decks from those cards. An important aspect of this is that any given card can be used in multiple decks. The software uses a SQL database to store the cards, decks, and their relationships so that your data can persist through different launches of the software. 

When launched, you will be greeted with a menu of options. When you add cards or decks, remember them so that you can look them up later. 


I created this software because as a fan of Magic: The gathering there wasn't an online service that did what I needed it to do, so I developed this for my own purposes.

{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}

[Software Demo Video](https://youtu.be/YXKqH1fjCBU)

# Relational Database

For this I am using SQLite.

My relational database consists of three tables: cards, deck, and deck_has_card. cards are identified by their name and each are unique. Decks are identified by their id. Any given deck will have multiple unique cards, and their relationship is detailed in deck_has_card.

# Development Environment

I used visual studio code for the python part of the language, and to initially structure the database I used SQLite studio.

I used python and imported the appropriate libraries for SQLite as well as the libraries datetime and PIL to handle date stamps and image opening.

# Useful Websites


- [Python sqlite](https://docs.python.org/3/library/sqlite3.html)
- [Sqlite tutorial](https://www.sqlitetutorial.net/)

# Future Work

- Add a way to see the names of all cards that exist, as well as decks.
- Add more data to cards, and implement a search system to find cards by those attributes.
- Add an attribute that will count how many times any given card is used, then have a menu that sorts by frequency of use.
- Implement data validation to user input
- instead of pulling images from local files, pull images from an API.
- implement an export option for decks.