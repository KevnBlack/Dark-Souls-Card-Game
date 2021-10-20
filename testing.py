import json
import random
from battlefield import Battlefield
from resources import Loading
from player import Player
from journey import Journey

resources = Loading() # Load game data
resources.sortEnemies()

classChoices = [resources.playerDatabase["Assassin"], resources.playerDatabase["Knight"]] # Preset for testing purposes
enemyChoices = []
for i in range(1,4): # Randomly select 3 enemies
    enemyChoices.append(random.choice(list(resources.enemyDatabase.items()))[1])

journey = Journey("DS3_easy", classChoices, resources) # Load journey
journey.setEncounters(resources)
journey.changePos("Area 1A")

'''
p1 = Player("Assassin")
p1.buildDeck(resources)
p1.draw()

  
if journey.changePos("Area 1A"):
    battlefield.placement(classChoices,enemyChoices)c
    print(battlefield)

#battlefield.generateEnemies(journey.currPos)


p1.displayHand()
print(battlefield)
battlefield.battlePhase(p1)       
'''



