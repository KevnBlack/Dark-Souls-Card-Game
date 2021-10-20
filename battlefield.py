import random
from player import Player
from enemyCards import EnemyCards

class Battlefield:
    def __init__(self):
        self.turn = 1
        self.battleState = True
        
        self.friendlyField = {1:None, 2:None, 3:None, 
                              4:None, 5:None, 6:None}

        self.enemyField = {1:None, 2:None, 3:None, 
                           4:None, 5:None, 6:None}
    
    def generateEnemies(self, area, resources, players, choice):
        enemies = []
        enemyCount = resources.encounterDatabase[str(area[choice])].encounter[len(players)-1]["enemies"]
        for index,amount in enumerate(enemyCount): # Randomly select 3 enemies
            if index == 0:
                enemies.extend(random.sample(resources.level1Enemies,amount))
            elif index == 1:
                enemies.extend(random.sample(resources.level2Enemies,amount))
            else:
                enemies.extend(random.sample(resources.level3Enemies,amount))
        return enemies
    
    def placement(self, players, enemies):
        self.openFriendlyZones = [1, 2, 3, 4, 5, 6]
        playerPlacement = random.randint(1,6) # Randomized for testing purposes, players will get to choose their placement
        for player in players:
            if self.friendlyField[playerPlacement] is None:
                self.friendlyField[playerPlacement] = player
                self.openFriendlyZones.remove(playerPlacement)
            else:
                altPlacement = random.choice(self.openFriendlyZones)
                self.friendlyField[altPlacement] = player
                self.openFriendlyZones.remove(altPlacement)
        
        self.openEnemyZones = [1, 2, 3, 4, 5, 6]
        for enemy in enemies:
            if self.enemyField[enemy.placement] is None:
                self.enemyField[enemy.placement] = enemy
                self.openEnemyZones.remove(enemy.placement)
            else:
                altPlacement = random.choice(self.openEnemyZones)
                self.enemyField[altPlacement] = enemy
                self.openEnemyZones.remove(altPlacement)
    
    def enemyAttack(self):
        for zone,enemy in self.enemyField.items(): # Enemy attack order
            frontMax, backMax = self.getMaxTaunts() # Get taunts at beginning of each enemy activation
            if enemy is None: # Skip empty zones
                continue
            else:
                for attackZone in enemy.attacks: # Cycle through attack zones per enemy
                    if len(enemy.attacks) == 1: # For single attacks
                        if self.friendlyField[attackZone] is None and attackZone in [1,2,3]: # If attack zone in player board is empty and in front row
                            if self.friendlyField[1] is None and self.friendlyField[2] is None and self.friendlyField[3] is None:
                                print(f'{enemy} attacks {self.friendlyField[backMax]}!') # Aim for highest taunt in back row if front is empty
                            else:
                                print(f'{enemy} attacks {self.friendlyField[frontMax]}!') # Initially aim for highest taunt player in front row
                        elif self.friendlyField[attackZone] is None and attackZone in [4,5,6]: # If attack zone in player board is empty and in back row
                            if self.friendlyField[4] is None and self.friendlyField[5] is None and self.friendlyField[6] is None:
                                print(f'{enemy} attacks {self.friendlyField[frontMax]}!') # Aim for highest taunt in front row if back is empty
                            else:
                                print(f'{enemy} attacks {self.friendlyField[backMax]}!')  # Initially aim for highest taunt player in back row
                        else:
                            print(f'{enemy} attacks {self.friendlyField[attackZone]}!') # Enemy lands hit
                    
                    elif len(enemy.attacks) > 1: # For AOE attacks
                        occupiedPlayerZones = self.getOccupiedPlayerZones()
                        if len(set.intersection(set(enemy.attacks),set(occupiedPlayerZones))) == 0: # If the enemy attack zones aim at no players
                            print(f'{enemy} missed completely!')
                            break # Missed, so move on to next enemy if any
                        elif self.friendlyField[attackZone] is None: # Skip empty zones
                            continue
                        else:
                            print(f'{enemy} attacks {self.friendlyField[attackZone]}!') # Enemy lands hit
    
    def battlePhase(self, players):
        while self.battleState:
            if all(x == None for x in self.enemyField.values()): # If all enemies are killed
                print("Battle won! Returning to exploration board...")
                self.battleState = False
            else:
                self.enemyAttack()
                self.battleState = False
                #Player.attack(self)
                self.turn += 1
    
    def killEnemy(self, zone): # Kill specified enemy
        if self.enemyField[zone] is not None:
            print(f"Killed {self.enemyField[zone].name} in Zone {zone}.")
            self.enemyField[zone] = None
        else:
            print(f"No enemy to kill in Zone {zone}.")
    
    def getOccupiedPlayerZones(self):
        return list({x for x in self.friendlyField if self.friendlyField[x]})
         
    def getMaxTaunts(self):
        self.frontTaunts = {1:0, 2:0, 3:0}
        self.backTaunts = {4:0, 5:0, 6:0}
        
        for player in self.friendlyField:
            if self.friendlyField[player] is None:
                continue
            elif player in [1,2,3]:
                self.frontTaunts[player] = self.friendlyField[player].taunt
            else:
                self.backTaunts[player] = self.friendlyField[player].taunt

        frontMaxTaunt =  max(self.frontTaunts, key=self.frontTaunts.get)
        backMaxTaunt = max(self.backTaunts, key=self.backTaunts.get)
        return frontMaxTaunt, backMaxTaunt

    def __str__(self): # String representation of battlefield
        return (f'========================================================================================================\n'
                f'|| {"PLAYER BOARD": ^98} ||\n'
                f'========================================================================================================\n'
                f'|| {"": ^30} || {"": ^30} || {"": ^30} ||\n'
                f'|| {str(self.friendlyField[6]): ^30} || {str(self.friendlyField[5]): ^30} || {str(self.friendlyField[4]): ^30} ||\n'
                f'|| {"(Zone 6)": ^30} || {"(Zone 5)": ^30} || {"(Zone 4)": ^30} ||\n'
                f'========================================================================================================\n'
                f'|| {"": ^30} || {"": ^30} || {"": ^30} ||\n'
                f'|| {str(self.friendlyField[3]): ^30} || {str(self.friendlyField[2]): ^30} || {str(self.friendlyField[1]): ^30} ||\n'
                f'|| {"(Zone 3)": ^30} || {"(Zone 2)": ^30} || {"(Zone 1)": ^30} ||\n'
                f'========================================================================================================\n'
                f'\n\n'
                f'========================================================================================================\n'
                f'|| {"": ^30} || {"": ^30} || {"": ^30} ||\n'
                f'|| {str(self.enemyField[1]): ^30} || {str(self.enemyField[2]): ^30} || {str(self.enemyField[3]): ^30} ||\n'
                f'|| {"(Zone 1)": ^30} || {"(Zone 2)": ^30} || {"(Zone 3)": ^30} ||\n'
                f'========================================================================================================\n'
                f'|| {"": ^30} || {"": ^30} || {"": ^30} ||\n'
                f'|| {str(self.enemyField[4]): ^30} || {str(self.enemyField[5]): ^30} || {str(self.enemyField[6]): ^30} ||\n'
                f'|| {"(Zone 4)": ^30} || {"(Zone 5)": ^30} || {"(Zone 6)": ^30} ||\n'
                f'========================================================================================================\n'
                f'|| {"ENEMY BOARD": ^98} ||\n'
                f'========================================================================================================\n')