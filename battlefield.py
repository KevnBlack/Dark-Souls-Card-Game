import random

class Battlefield:
    def __init__(self):
        self.battleState = True
        
        self.friendlyField = {1:None, 2:None, 3:None, 
                              4:None, 5:None, 6:None}

        self.enemyField = {1:None, 2:None, 3:None, 
                           4:None, 5:None, 6:None}
     
    def placement(self, players, enemies):
        self.friendlyZones = [1, 2, 3, 4, 5, 6]
        playerPlacement = random.randint(1,6) # Randomized for testing purposes, players will get to choose their placement
        for player in players:
            if self.friendlyField[playerPlacement] is None:
                self.friendlyField[playerPlacement] = player
                self.friendlyZones.remove(playerPlacement)
            else:
                altPlacement = random.choice(self.friendlyZones)
                self.friendlyField[altPlacement] = player
                self.friendlyZones.remove(altPlacement)
        
        self.enemyZones = [1, 2, 3, 4, 5, 6]
        for enemy in enemies:
            if self.enemyField[enemy.placement] is None:
                self.enemyField[enemy.placement] = enemy
                self.enemyZones.remove(enemy.placement)
            else:
                altPlacement = random.choice(self.enemyZones)
                self.enemyField[altPlacement] = enemy
                self.enemyZones.remove(altPlacement)
                
            
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
                            break # If any, move on to next enemy
                        elif self.friendlyField[attackZone] is None: # Skip empty zones
                            continue
                        else:
                            print(f'{enemy} attacks {self.friendlyField[attackZone]}!') # Enemy lands hit
        
    def playerResponse(self):
        # TODO: Function for responding to an enemy attack
        pass
    
    def playerAttack(self):
        # TODO: Function for initiating an attack
        choice = input("What will you do?")
    
    def battlePhase(self):
        while self.battleState:
            if all(x == None for x in self.enemyField.values()): # If all enemies are killed
                print("Battle won! Returning to exploration board...")
                self.battleState = False
            else:
                self.enemyAttack()
                self.battleState = False
                #self.playerAttack()

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