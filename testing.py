import json
import random
from card_class import Card_Class
from card_enemy import Card_Enemy
from encounter import Encounter
from battlefield import Battlefield
from journey import Journey

with open("classes.json","r") as c:
    classesData = json.load(c)
    
with open("enemies.json","r") as e:
    enemiesData = json.load(e)
    
with open("encountersTest.json","r") as enc:
    encounterData = json.load(enc)

classDatabase = {}
enemyDatabase = {}
encounterDatabase = {}


for curr in classesData["classes"]: # Load character classes
    character = Card_Class(curr["classId"], curr["name"], curr["taunt"], 
                           curr["ability"], curr["usedAbility"], curr["placement"], 
                           curr["fromSet"])
    classDatabase[curr["name"]] = character
    
for curr in enemiesData["enemies"]: # Load enemy cards
    enemy = Card_Enemy(curr["enemyId"], curr["name"], curr["level"], curr["power"], 
                       curr["defense"], curr["HP"], curr["souls"], curr["weakness"], 
                       curr["inflicts"], curr["condition"], curr["ability"], curr["placement"], 
                       curr["attacks"], curr["fromSet"])
    enemyDatabase[curr["name"]] = enemy

    
for curr in encounterData["encounters"]:
    encounter = Encounter(curr["encounterId"], curr["name"], curr["level"], 
                            curr["traps"], curr["terrain"], curr["fromSet"], 
                            curr["encounter"])
    encounterDatabase[curr["name"]] = encounter
  


'''
classChoices = [classDatabase["Assassin"], classDatabase["Knight"]] # Preset for testing purposes
enemyChoices = []
for i in range(1,4): # Randomly select 3 enemies
    enemyChoices.append(random.choice(list(enemyDatabase.items()))[1])


battlefield = Battlefield()
battlefield.placement(classChoices,enemyChoices)
battlefield.battlePhase()
print(battlefield)
'''

journey = Journey("Dark Souls 3 (Easy)")