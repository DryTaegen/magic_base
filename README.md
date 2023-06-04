# Overview


This software allows the user to store cards into their collection and then make decks from those cards. An important aspect of this is that any given card can be used in multiple decks. The software uses a Mongo database to store the cards, decks, and their relationships so that your data can persist through different launches of the software. 

When launched, you will be greeted with a menu of options. 


I created this software because as a fan of Magic: The gathering there wasn't an online service that did what I needed it to do, so I developed this for my own purposes.


[Software Demo Video](https://youtu.be/A8yzCIxO_VQ)

# Relational Database

For this I am using Mongodb.

My relational database consists of three tables: cards, deck, and deck_has_card. cards are identified by their name and each are unique. Decks are identified by their id. Any given deck will have multiple unique cards, and their relationship is detailed in deck_has_card.

# Development Environment

I used visual studio code for the python part of the language, and mongoDB to store the data.

I also imported an SDK to get magic cards from an online source rather than locally.

I used python and imported the appropriate libraries for SQLite as well as the libraries datetime and PIL to handle date stamps and image opening.

# Useful Websites


- [MongoDB cheat sheet](https://webdevsimplified.com/mongodb-cheat-sheet.html)
- [W3 Schools](https://www.w3schools.com/python/python_mongodb_getstarted.asp)
- [Web dev Simplified course](https://www.youtube.com/watch?v=ofme2o29ngU)

# Future Work

- Add a way to see the names of all cards that exist, as well as decks.
- Add more data to cards, and implement a search system to find cards by those attributes.
- Implement data validation to user input
- implement an export option for decks.