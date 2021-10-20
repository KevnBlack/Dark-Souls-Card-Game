import json

with open("./data/cards/decks.json","r") as dec:
    deckData = json.load(dec)

deck = []
for key,value in deckData.items():
    deck.append(cards[value["Assassin"]])