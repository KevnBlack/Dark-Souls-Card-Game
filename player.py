import random

class Player:
    def __init__(self, playerClass):
        self.playerClass = playerClass
        self.deck = []
        self.hand = []
        self.discardPile = []
        self.HP = 0
        self.redrew = False
        
        
    def buildDeck(self, resources):
        """
        Builds deck for a player, up to an initial amount of 28, then the deck
        is shuffled. Player HP is also set.

        Parameters
        ----------
        resources : Loading
            Data for all objects in the game.

        Returns
        -------
        None.
        """
        for key,value in resources.deckData.items():
            self.deck.append(resources.cards[value[self.playerClass]])
        random.shuffle(self.deck)
        self.HP = self.getHP() # Set HP
    
    
    def draw(self):
        """
        Player draws up to 6 cards. If one player has their deck size (HP) 
        reach zero, the party returns the bonfire to rest.

        Returns
        -------
        None.
        """
        while len(self.hand) < 6: # While player doesn't have 6 cards in hand
            if self.HP == 0:
                print("You died.")
                break
            else:
                self.hand.append(self.deck.pop(0)) # Draw from their deck
                self.HP = self.getHP() # Update HP
        
        
    def mulligan(self):
        """
        A player performs a mulligan if they draw all stamina on the first turn
        of an encounter. If they draw all stamina again, tough luck.

        Returns
        -------
        None.
        """
        self.deck.extend(self.hand) # Put hand back in deck
        self.hand.clear()           # Clear hand
        random.shuffle(self.deck)   # Shuffle deck
        self.draw()                 # Redraw cards
    
    def redraw(self, cards):
        """
        A player may discared one or more cards to draw an equal number of cards
        once per turn.

        Returns
        -------
        None.

        """
        for i in range(len(cards)): # Convert list of input strings to ints
            cards[i] = int(cards[i]) 
    
        self.discard(cards)
        self.draw()
        self.redrew = True
        print(f"{self.playerClass} has re-drew {len(cards)} cards.")
        print(f"Hand of {self.playerClass}: {self.updateHand()}")

    
    def response(self, enemy):
        responses = self.potentialBlockResponses()
        print(f"Hand of {self.playerClass}: {self.updateHand()}")
        if len(responses) == 0:
            print(f"{self.playerClass} has no equipment to block {enemy.name}.")
            self.damaged(enemy.power)
            print(f"{self.playerClass} takes {enemy.power} damage. HP: {self.HP}")
        else:
            print(f"\n=== {self.playerClass} Possible Responses ===")
            for key, value in responses.items():
                print(f"{value}")
            choiceState = True
            while choiceState:
                choice = int(input(f"{self.playerClass}, how do you respond? "))
                if choice == 1: # Block
                    equipChoice = int(input(f"{self.playerClass}, what equipment will you use to block the {enemy}? "))
                    optionChoice = int(input(f"{self.playerClass}, what option do you choose? "))
                    self.blockOption(equipChoice, optionChoice, enemy)
                    choiceState = False
                elif choice == 2: # Skip turn by not blocking
                    self.damaged(enemy.power) # Discard amount of cards from top of deck
                    print(f"{self.playerClass} takes {enemy.power} damage. HP: {self.HP}")
                    choiceState = False
                elif choice == 3: # Display what choice numbers do
                    print("1: Select equipment and option to block enemy attack")
                    print("2: Skip turn by not blocking")
                    print("3: Displays this help menu")
                else:
                    print("Enter a valid choice. Enter 3 for help.")
    
    
    def blockOption(self, equipChoice, optionChoice, enemy):
        """
        Takes the player choice for blocking enemy attack and returns stamina 
        cards used in tribute, discards those cards, and calculates damage to HP.
        
        Parameters
        ----------
        equipChoice : Integer
            Player's chosen equipment to block enemy attack.
        optionChoice : Integer
            Player's chosen option for that equipment.
        enemy : EnemyCards
            Enemy object, used for calculating damage difference.

        Returns
        -------
        None.
        """
        selectedCard = self.handLookup[equipChoice]             # Chosen equipment
        cost = selectedCard.choices[optionChoice-1]["cost"]     # Get choice cost of chosen equipment
        _, _, tributed = self.tribute(cost,self.getStaminas())  # Get stamina cards that were used in tribute
        
        for choice in selectedCard.choices:                     # Traverse choices of equipment
            if choice["option"] == optionChoice:                # After coming across the selected choice
                blockVal = choice["ability"]["block"]    
                if enemy.power >= blockVal:           # If the enemy's power is greater than what the player can block
                    dmgDiff = enemy.power - blockVal  # Damage is equal to the difference
                else:
                    dmgDiff = 0                                 # If the enemy's power is less than what the player can block, then no damage is taken
                if optionChoice >= 2:                           # If player chooses a discard option, discard selected equipment
                    tributed.append(selectedCard.name)
                
                self.discard(tributed)                          # Discard tributed cards
                self.damaged(dmgDiff)                           # Apply damage
                print(f"{self.playerClass} blocks the attack for {blockVal} and receives {dmgDiff} damage. HP: {self.HP}.")
            else:
                continue                                        # Skip unselected actions
    
    def attackOption(self, equipChoice, optionChoice, enemyChoice):
        pass

    def potentialBlockResponses(self):
        responses = {}
        staminas = self.getStaminas()
        index = 1
            
        for card in self.hand: # Check for equipment that can be used
            for choice in card.choices:
                try:
                    temp = choice["cost"].copy() # Shallow copy to make "cost" immutable in the database
                    checkTribute, remaining, _ = self.tribute(temp,staminas)
                    if checkTribute:
                        # TODO: Not too important, but implement code that disregards repeat potential responses, i.e., have two or more of same equipment in hand.
                        if "block" in choice["ability"]: # Blocking action
                            text = f"{choice['option']}: {choice['action']} {card.name} to block for {choice['ability']['block']}.\nCost: {choice['cost']}\nRemaining stamina: {remaining}\n"
                            responses[index] = text
                            index += 1
                        elif "dodge" in choice["ability"]: # Non-blocking action
                            text = f"{choice['option']}: {choice['action']} {card.name} to dodge.\nCost: {choice['cost']}\nRemaining stamina: {remaining}\n"
                            responses[index] = text
                            index += 1
                except KeyError:
                    continue      
        
        return responses
    
    def potentialAttackResponses(self):
        responses = {}
        staminas = self.getStaminas()
        index = 1
            
        for card in self.hand: # Check for equipment that can be used
            for choice in card.choices:
                try:
                    temp = choice["cost"].copy() # Shallow copy to make "cost" immutable in the database
                    checkTribute, remaining, _ = self.tribute(temp,staminas)
                    if checkTribute:
                        # TODO: Not too important, but implement code that disregards repeat potential responses, i.e., have two or more of same equipment in hand.
                        if "attack" in choice["ability"] or "ranged" in choice["ability"]: # Attack action
                            text = f"{choice['option']}: {choice['action']} {card.name} to attack for {choice['ability']['attack']}.\nCost: {choice['cost']}\nRemaining stamina: {remaining}\n"
                            responses[index] = text
                            index += 1
                        elif "heal" in choice["ability"]: # Non-attack action 1
                            text = f"{choice['option']}: {choice['action']} {card.name} to heal for {choice['ability']['heal']}.\nCost: {choice['cost']}\nRemaining stamina: {remaining}\n"
                            responses[index] = text
                            index += 1
                        elif "search" in choice["ability"]: # Non-attack action 2
                            text = f"{choice['option']}: {choice['action']} {card.name} to search your deck for {choice['ability']['search']} cards.\nCost: {choice['cost']}\nRemaining stamina: {remaining}\n"
                            responses[index] = text
                            index += 1
                
                except KeyError:
                    continue
        
        return responses
    
    
    def tribute(self, cost, handStaminas):
        for stamina in cost: # Check that each stamina in cost is actually in the player's hand
            if stamina not in handStaminas and stamina != "Any": # First instance of not having correct stamina, tribute fails
                return False, handStaminas, []
        if len(cost) == 0:
            return True, handStaminas, []
        elif len(cost) <= len(handStaminas): # Only execute if the amount of cards between lists are the same   
            remain, removed = [], []
            for stamina in handStaminas:
                if stamina in cost:
                    removed.append(stamina)
                    cost.remove(stamina)
                else:
                    remain.append(stamina) # Remove other staminas until "Any" is left            
            
            if cost.count("Any") <= len(remain): # Use remaining staminas to fulfill the "Any" staminas
                for i in range(cost.count("Any")):
                    toRemove = random.choice(remain)
                    removed.append(toRemove)
                    remain.remove(toRemove) # Remove random staminas
                return True, remain, removed # Cost fulfilled
            else:
                return False, handStaminas, [] # Cannot fulfill cost with selected cards
        
        else:
            return False, handStaminas, [] # You need more stamina cards for the cost
    
    def discard(self, cardsToRemove): # Removes list of cards from player's hand
        if all(isinstance(card, int) for card in cardsToRemove): # For re-drawing, i.e., checks if cardsToRemove is all numbers
            for card in cardsToRemove: 
                cardObj = self.handLookup[card]
                self.hand.remove(cardObj)
                self.discardPile.append(cardObj)
        else:   # For tributes
            for card in cardsToRemove: 
                cardObj = self.objLookup[card]
                self.hand.remove(cardObj)
                self.discardPile.append(cardObj)
    
    
    def damaged(self, amount):
        for i in range(amount):
            self.discardPile.append(self.deck.pop(i)) # Send to discard pile
        self.HP -= amount
    
    
    def attack(self):
        self.draw() # Draw to replace used cards, if any, from enemy attack
        self.hasCondition() # Check for conditions and apply accordingly        
        responses = self.potentialAttackResponses()
        print(f"Hand of {self.playerClass}: {self.updateHand()}")
        if len(responses) == 0:
            print(f"{self.playerClass} has no equipment to attack or cast.")
        else:
            print(f"\n=== {self.playerClass} Possible Attacks/Casts ===")
            for key, value in responses.items():
                print(f"{value}")
            choiceState = True
            while choiceState:
                choice = int(input(f"{self.playerClass}, what do you wish to do? "))
                if choice == 1: # Attack/cast
                    equipChoice = int(input(f"{self.playerClass}, what equipment will you use to attack/cast? "))
                    optionChoice = int(input("What option do you choose? "))
                    enemyChoice = int(input("What enemy zone do you wish to attack? "))
                    self.attackOption(equipChoice, optionChoice, enemyChoice)
                    choiceState = False
                elif choice == 2: # Skip turn by not attacking/casting
                    print(f"{self.playerClass} skips their turn.")
                    choiceState = False
                elif choice == 3:
                    if not self.redrew: # If player didn't redraw
                        cards = input(f"{self.playerClass}, enter the card number you wish to discard, separated by a space: ")
                        self.redraw(cards.split())
                    else:
                        print("You may only re-draw once per turn.")
                elif choice == 4: # Display what choice numbers do
                    print("1: Select equipment and option to perform an attack/cast")
                    print("2: Skip turn by not attacking/casting")
                    print("3: Redraw")
                    print("4: Displays this help menu")
                else:
                    print("Enter a valid choice. Enter 4 for help.")
        
    def getStaminas(self):
        staminas = []   # Take note of staminas in hand
        for card in self.hand: 
            if card.cardType == "Stamina":
                staminas.append(card.name)
                continue
        return staminas 
    
    def updateHand(self):
        indices, names = [], []
        for index, card in enumerate(self.hand):
            index += 1
            indices.append(index)
            names.append(card.name)
        self.handLookup = dict(zip(indices, self.hand))
        self.objLookup = dict(zip(names, self.hand))
        return self.handLookup
        
    
    def getHP(self):
        """
        Return the player's HP.

        Returns
        -------
        len(self.deck) : Integer
            Integer to represent the size of the deck, i.e., the player's HP.
        """
        return len(self.deck)
    
    def hasCondition(self):
        if self.playerClass.condition is None:
            print(f"{self.playerClass} isn't inflicted with a condition.")
        elif self.playerClass.condition == "bleed":
            print(f"{self.playerClass} is inflicted with bleed.")
        elif self.playerClass.condition == "frostbite":
            print(f"{self.playerClass} is inflicted with frostbite.")
        elif self.playerClass.condition == "poison":
            print(f"{self.playerClass} is inflicted with poison.")
        else:
            print(f"{self.playerClass} is inflicted with stagger.")
    
    
    def __str__(self): # String representation of card
        return (f'{self.playerClass.name}')
    
    
    def __repr__(self):
        return (f'{self.playerClass.name}')