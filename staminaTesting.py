# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 21:34:06 2021

@author: Kevin
"""
import random
#cost = ["Any", "Any", "Any", "Intelligence"]
#hand = ["Strength", "Dexterity", "Faith", "Intelligence"]

cost = ['Strength', 'Any']
hand = ['Strength', 'Strength', 'Strength', 'Dexterity']

def tribute(cost, hand):
    for stamina in cost: # Check that each stamina in cost is actually in the player's hand
        if stamina not in hand and stamina != "Any":
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

'''
def tribute(cost, hand):
    if len(cost) <= len(hand): # Only execute if the amount of cards between lists are the same   
        remain = []
        for stamina in hand:
            cost.remove(stamina) if stamina in cost else remain.append(stamina) # Remove other staminas until "Any" is left
        
        if cost.count("Any") <= len(remain): # Use remaining staminas to fulfill the "Any" staminas
            for i in range(cost.count("Any")):
                remain.remove(random.choice(remain)) # Remove random staminas
            print("Cost fulfilled.")
            print(remain)
            print(cost)
        else:
            print("Cannot fulfill cost with selected cards.")
    else:
        print("You need more stamina cards for the cost.")
'''

state, remaining = tribute(cost, hand)
print(state)
print(remaining)
    