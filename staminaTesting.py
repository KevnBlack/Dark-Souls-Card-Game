# -*- coding: utf-8 -*-
"""
Created on Sun Oct 17 21:34:06 2021

@author: Kevin
"""

cost = ["Any", "Any", "Any", "Intelligence"]
hand = ["Strength", "Dexterity", "Faith", "Intelligence"]

def tribute(cost, hand):
    if len(cost) == len(hand): # Only execute if the amount of cards between lists are the same   
        remain = []
        for card in hand:
            cost.remove(card) if card in cost else remain.append(card) # Remove other staminas until "Any" is left
        
        if cost.count("Any") == len(remain): # Use remaining staminas to fulfill the "Any" staminas
            print("Cost fulfilled.")
        else:
            print("Cannot fulfill cost with selected cards.")
    else:
        print("You need more stamina cards for the cost.")


tribute(cost, hand)
    