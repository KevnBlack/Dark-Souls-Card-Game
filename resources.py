import json
from classCards import ClassCards
from enemyCards import EnemyCards
from encounter import Encounter
from bonfire import Bonfire
from equipment import Equipment
from stamina import Stamina

class Loading:
    def __init__(self):
        self.bonfireDatabase = {}
        self.playerDatabase = {}
        self.enemyDatabase = {}
        self.equipmentDatabase = {}
        self.staminaDatabase = {}
        self.encounterDatabase = {}
        
        with open("./data/cards/bonfire.json","r") as b:
            self.bonfireData = json.load(b)
        
        with open("./data/cards/players.json","r") as c:
            self.playerData = json.load(c)
        
        with open("./data/cards/enemies.json","r") as e:
            self.enemiesData = json.load(e)
        
        with open("./data/cards/equipment.json","r") as equ:
            self.equipmentData = json.load(equ)
        
        with open("./data/cards/stamina.json","r") as stam:
            self.staminaData = json.load(stam)
        
        with open("./data/journies/encounters.json","r") as enc:
            self.encounterData = json.load(enc)
        
        with open("./data/cards/decks.json","r") as dec:
            self.deckData = json.load(dec)
        
        for curr in self.bonfireData["bonfire"]:
            bonfire = Bonfire(curr["bonfireId"], curr["name"], curr["level"], 
                                   curr["deckMax"], curr["fromSet"])
            self.bonfireDatabase[curr["name"]] = bonfire
        
        for curr in self.playerData["players"]: # Load character classes
            character = ClassCards(curr["classId"], curr["name"], curr["taunt"], 
                                   curr["ability"], curr["usedAbility"], curr["placement"], 
                                   curr["changedPos"], curr["fromSet"])
            self.playerDatabase[curr["name"]] = character

        for curr in self.enemiesData["enemies"]: # Load enemy cards
            enemy = EnemyCards(curr["enemyId"], curr["name"], curr["level"], curr["power"], 
                               curr["defense"], curr["HP"], curr["souls"], curr["weakness"], 
                               curr["inflicts"], curr["condition"], curr["ability"], curr["placement"], 
                               curr["attacks"], curr["fromSet"])
            self.enemyDatabase[curr["name"]] = enemy

        for curr in self.equipmentData["equipment"]:
            equipment = Equipment(curr["equipmentId"], curr["name"], curr["cardType"], 
                                  curr["weakness"], curr["fromSet"], curr["choices"])
            self.equipmentDatabase[curr["name"]] = equipment
            
        for curr in self.staminaData["stamina"]:
            stamina = Stamina(curr["staminaId"], curr["name"], curr["cardType"], curr["cost"],
                                  curr["fromSet"], curr["choices"])
            self.staminaDatabase[curr["name"]] = stamina
        
        for curr in self.encounterData["encounters"]:
            encounter = Encounter(curr["encounterId"], curr["name"], curr["level"], 
                                    curr["traps"], curr["terrain"], curr["fromSet"], 
                                    curr["encounter"])
            self.encounterDatabase[curr["name"]] = encounter
            
        self.cards = {**self.staminaDatabase, **self.equipmentDatabase} # Combine stamina and equipment databases
        # TODO: Eventually create normal and transposed databases
        
    def playerSetup(self, players):
        for player in players:
            player.playerClass = self.playerDatabase[player.playerClass]
            
    def sortEnemies(self):
        self.level1Enemies, self.level2Enemies, self.level3Enemies = [], [], []
        for name,enemy in self.enemyDatabase.items(): # Sort encounters by level
            if enemy.level == 1:
                self.level1Enemies.append(enemy)
            elif enemy.level == 2:
                self.level2Enemies.append(enemy)
            else:
                self.level3Enemies.append(enemy) 
                
    def sortEncounters(self):
        self.level1Encounters, self.level2Encounters, self.level3Encounters = [], [], []
        for name,encounter in self.encounterDatabase.items(): # Sort encounters by level
            if encounter.level == 1:
                self.level1Encounters.append(encounter)
            elif encounter.level == 2:
                self.level2Encounters.append(encounter)
            else:
                self.level3Encounters.append(encounter)
        