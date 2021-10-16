import json
from card_class import Card_Class
from card_enemy import Card_Enemy
from battlefield import Battlefield

with open("classes.json","r") as c:
    classesData = json.load(c)
    
with open("enemies.json","r") as e:
    enemiesData = json.load(e)

classDatabase = {}
enemyDatabase = {}

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
  
classChoices = [classDatabase["Assassin"], classDatabase["Knight"]] # For testing purposes
#enemyChoices = []
enemyChoices = [enemyDatabase["Fire Witch"]]
  
battlefield = Battlefield()
battlefield.placement(classChoices,enemyChoices)
battlefield.battlePhase()
print(battlefield)
