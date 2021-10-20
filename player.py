import random

class Player:
    def __init__(self, playerClass):
        self.playerClass = playerClass
        self.deck = []
        self.hand = []
        self.discard = []
        self.HP = 0
        
    def buildDeck(self, resources):
        for key,value in resources.deckData.items():
            self.deck.append(resources.cards[value[self.playerClass]])
        random.shuffle(self.deck)
        self.HP = self.getHP() # Update HP
    
    def draw(self):        
        while len(self.hand) < 6: # While player doesn't have 6 cards in hand
            if self.HP == 0:
                print("You died.")
                break
            else:
                self.hand.append(self.deck.pop(0)) # Draw from their deck
                self.HP = self.getHP() # Update HP
                
    def displayHand(self):
        print(f"{self.playerClass}: {self.hand}")
    
    def response(self, enemy):
        # TODO: Function for responding to an enemy attack
        choice = input(f"{self.playerClass}, how will you respond to {enemy}?")
    
    def attack(self):
        # TODO: Function for initiating an attack
        choice = input("What will you do?")
        
    def getHP(self):
        return len(self.deck)