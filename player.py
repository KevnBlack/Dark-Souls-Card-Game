import random
import re

class Player:
    def __init__(self, playerClass):
        self.playerClass = playerClass
        self.deck = []
        self.hand = []
        self.discardPile = []
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
        
        
    def mulligan(self):
        self.deck.extend(self.hand) # Put hand back in deck
        self.hand.clear() # Clear hand
        random.shuffle(self.deck) # Shuffle deck
        self.draw() # Redraw cards
    
    
    def response(self, enemy):
        # TODO: Function for responding to an enemy attack by blocking
        responses, remaining = self.potentialResponses()
        if len(responses) == 0:
            print(f"{self.playerClass} has no equipment to block {enemy.name}.")
            print(f"{self.playerClass} takes {enemy.power} damage.")
            self.HP -= enemy.power
            self.damaged(enemy.power)
        else:
            print(f"Hand of {self.playerClass}: {self.displayHand()}")
            print(f"\n=== {self.playerClass} Possible Responses ===")
            print(*responses, sep="\n")
            choiceState = True
            while choiceState:
                choice = int(input(f"{self.playerClass}, how do you respond? "))
                if choice == 1: # Block
                    equipChoice = int(input(f"{self.playerClass}, what equipment will you use to block the {enemy}? "))
                    optionChoice = input(f"{self.playerClass}, what option do you choose? ")
                    self.chooseOption(equipChoice, optionChoice, enemy)
                    choiceState = False
                elif choice == 2: # Skip turn by not blocking
                    print(f"{self.playerClass} takes {enemy.power} damage.")
                    self.HP -= enemy.power
                    self.damaged(enemy.power) # Discard amount of cards from top of deck
                    choiceState = False
                elif choice == 3: # Display what choice numbers do
                    print("Help section here.")
                else:
                    print("Enter a valid choice.")
    
    
    def chooseOption(self, equipChoice, optionChoice, enemy):
        selectedCard = self.cardLookup[equipChoice]
        for action in selectedCard.choices:
            if action["option"] == optionChoice:
                if enemy.power >= action['value']:
                    diff = enemy.power - action['value']
                else:
                    diff = 0
                self.damaged(diff)
                # TODO: Discard equipment (if reused isn't used) cards and stamina cards after performing action
                print(f"{self.playerClass} blocks the attack for {action['value']} and receives {diff} damage. HP: {self.getHP()}.")
            else:
                continue
                
    
    def damaged(self, amount):
        deckDiscard = []
        for i in range(amount):
            deckDiscard.append(self.deck.pop(i)) # Discard cards from top of deck
        self.discardPile.extend(deckDiscard) # Send to discard pile
    
    
    def attack(self):
        # TODO: Function for initiating an attack
        choice = input("What will you do?")
        
        
    def potentialResponses(self):
        responses = []
        staminas = []
        
        for card in self.hand: # Take note of staminas in hand
            if card.cardType == "Stamina":
                staminas.append(card.name)
                continue
            
        for card in self.hand: # Check for equipment that can be used
            for option in card.choices:
                try:
                    temp = option["cost"].copy() # Shallow copy to make "cost" immutable in the database
                    checkTribute, remaining = self.tribute(temp,staminas)
                    if checkTribute:
                        actions = re.sub(r'[\[\]]','',str(option['ability']))
                        if ("block" in option["ability"] or "dodge" in option["ability"]) and option["value"] != 0:
                            responses.append(f"- {option['option']} {card.name} to perform {actions} for {option['value']}.\n" 
                                             f"Cost: {option['cost']}\n"
                                             f"Remaining stamina: {remaining}\n")
                        elif ("block" in option["ability"] or "dodge" in option["ability"]) and option["value"] == 0:
                            responses.append(f"- {option['option']} {card.name} to perform {actions}.\n" 
                                             f"Cost: {option['cost']}\n"
                                             f"Remaining stamina: {remaining}\n")
                except KeyError:
                    continue
        return responses, staminas
    
    
    def tribute(self, cost, hand):
        for stamina in cost: # Check that each stamina in cost is actually in the player's hand
            if stamina not in hand and stamina != "Any": # First instance of not having correct stamina, tribute fails
                return False, hand
        
        if len(cost) <= len(hand): # Only execute if the amount of cards between lists are the same   
            remain = []
            for stamina in hand:
                cost.remove(stamina) if stamina in cost else remain.append(stamina) # Remove other staminas until "Any" is left
            
            if cost.count("Any") <= len(remain): # Use remaining staminas to fulfill the "Any" staminas
                for i in range(cost.count("Any")):
                    remain.remove(random.choice(remain)) # Remove random staminas
                return True, remain # Cost fulfilled
            else:
                return False, hand # Cannot fulfill cost with selected cards
        
        else:
            return False, hand # You need more stamina cards for the cost
    
    
    def displayHand(self):
        indices = []
        for index, card in enumerate(self.hand):
            index += 1
            indices.append(index)
        self.cardLookup = dict(zip(indices, self.hand))
        return self.cardLookup
        
    
    def getHP(self):
        return len(self.deck)
    
    
    def __str__(self): # String representation of card
        return (f'{self.playerClass.name}')
    
    
    def __repr__(self):
        return (f'{self.playerClass.name}')