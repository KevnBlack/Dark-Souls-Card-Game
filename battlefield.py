import random

class Battlefield:
    def __init__(self, players, resources):
        self.turnNum = 1
        self.turn = "Turn " + str(self.turnNum)
        self.battleState = True
        
        self.friendlyField = {1:None, 2:None, 3:None, 
                              4:None, 5:None, 6:None}

        self.enemyField = {1:None, 2:None, 3:None, 
                           4:None, 5:None, 6:None}
        
        self.players = players
        self.resources = resources
    
    def generateEnemies(self, area, choice):
        enemies = []
        enemyCount = self.resources.encounterDatabase[str(area[choice])].encounter[len(self.players)-1]["enemies"]
        for index,amount in enumerate(enemyCount): # Randomly select enemies
            if index == 0:
                enemies.extend(random.sample(self.resources.level1Enemies,amount))
            elif index == 1:
                enemies.extend(random.sample(self.resources.level2Enemies,amount))
            else:
                enemies.extend(random.sample(self.resources.level3Enemies,amount))
        return enemies
    
    def placement(self, enemies):
        self.openFriendlyZones = [1, 2, 3, 4, 5, 6]
        playerPlacement = random.randint(1,6) # Randomized for testing purposes, players will get to choose their placement
        for player in self.players:
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

    def initialDraw(self):
        """
        Function for the first draw a player makes in an encounter.
        If it is the first turn and a player draws all staminas, they
        will mulligan one time in hopes of drawing an equipment.

        Returns
        -------
        None.

        """
        for player in self.players:
            stamCount = 0                               # Initialize for each player
            player.draw()
            if self.turn == 1:                          # If a hand contains all stamina on first turn, player will mulligan
                for card in player.hand:
                    if card.cardType == "Stamina":
                        stamCount += 1
                    elif card.cardType != "Stamina":    # Break out of loop if there is a non-stamina card
                        break
                if stamCount == 6:
                    print(f"{player} performs a mulligan.")
                    player.mulligan()
                    
    def changePos(self):
        pass
    
    def enemyActivation(self):
        for zone,enemy in self.enemyField.items(): # Enemy attack order
            frontMax, backMax = self.getMaxTaunts() # Get taunts at beginning of each enemy activation
            if enemy is None: # Skip empty zones
                continue
            else:
                for attackZone in enemy.attacks: # Cycle through attack zones per enemy
                    if len(enemy.attacks) == 1: # For single attacks
                        maxFrontPlayer = self.friendlyField[frontMax]
                        maxBackPlayer = self.friendlyField[backMax]
                        directHit = self.friendlyField[attackZone]
                        if self.friendlyField[attackZone] is None and attackZone in [1,2,3]: # If attack zone in player board is empty and in front row
                            if self.friendlyField[1] is None and self.friendlyField[2] is None and self.friendlyField[3] is None:
                                print(f'{enemy} attacks {maxBackPlayer} for {enemy.power}.\n') # Aim for highest taunt in back row if front is empty
                                maxBackPlayer.response(enemy)
                            else:
                                print(f'{enemy} attacks {maxFrontPlayer} for {enemy.power}.\n') # Initially aim for highest taunt player in front row
                                maxFrontPlayer.response(enemy)
                        
                        elif self.friendlyField[attackZone] is None and attackZone in [4,5,6]: # If attack zone in player board is empty and in back row
                            if self.friendlyField[4] is None and self.friendlyField[5] is None and self.friendlyField[6] is None:
                                print(f'{enemy} attacks {maxFrontPlayer} for {enemy.power}.\n') # Aim for highest taunt in front row if back is empty
                                maxFrontPlayer.response(enemy)
                            else:
                                print(f'{enemy} attacks {maxBackPlayer} for {enemy.power}.\n')  # Initially aim for highest taunt player in back row
                                maxBackPlayer.response(enemy)
                        else:
                            print(f'{enemy} attacks {directHit} for {enemy.power}.\n') # Enemy lands hit
                            directHit.response(enemy)
                        
                    elif len(enemy.attacks) > 1: # For AOE attacks
                        occupiedPlayerZones = self.getOccupiedPlayerZones()
                        if len(set.intersection(set(enemy.attacks),set(occupiedPlayerZones))) == 0: # If the enemy attack zones aim at no players
                            print(f'{enemy} missed completely!\n')
                            break # Missed, so move on to next enemy if any
                        elif self.friendlyField[attackZone] is None: # Skip empty zones
                            continue
                        else:
                            currPlayer = self.friendlyField[attackZone]
                            print(f'{enemy} performs an AOE attack and attacks {currPlayer} for {enemy.power}.\n') # Enemy lands hit
                            currPlayer.response(enemy)
    
    def playerActivation(self):
        for zone, player in self.friendlyField.items(): # Player attack order
            if player is None: # Skip empty zones
                continue
            else:
                player.attack()
    
    def battlePhase(self, battlefield):
        self.initialDraw()
        while self.battleState:
            if all(x == None for x in self.enemyField.values()): # If all enemies are killed
                print("Battle won! Returning to exploration board...")
                self.battleState = False
            else:
                print(battlefield)
                self.enemyActivation()
                print(battlefield)
                self.playerActivation()
                self.turnNum += 1
                self.turn = "Turn " + str(self.turnNum)
    
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
        
        for zone in self.friendlyField:
            if self.friendlyField[zone] is None:
                continue
            elif zone in [1,2,3]:
                self.frontTaunts[zone] = self.friendlyField[zone].playerClass.taunt
            else:
                self.backTaunts[zone] = self.friendlyField[zone].playerClass.taunt

        frontMaxTaunt =  max(self.frontTaunts, key=self.frontTaunts.get)
        backMaxTaunt = max(self.backTaunts, key=self.backTaunts.get)
        return frontMaxTaunt, backMaxTaunt

    def __str__(self): # String representation of battlefield
        return (f'=======================================================================================================================\n'
                f'|| {"PLAYER BOARD": ^113} ||\n'
                f'=======================================================================================================================\n'
                f'|| {"": ^35} || {"": ^35} || {"": ^35} ||\n'
                f'|| {str(self.friendlyField[6]): ^35} || {str(self.friendlyField[5]): ^35} || {str(self.friendlyField[4]): ^35} ||\n'
                f'|| {"(Zone 6)": ^35} || {"(Zone 5)": ^35} || {"(Zone 4)": ^35} ||\n'
                f'=======================================================================================================================\n'
                f'|| {"": ^35} || {"": ^35} || {"": ^35} ||\n'
                f'|| {str(self.friendlyField[3]): ^35} || {str(self.friendlyField[2]): ^35} || {str(self.friendlyField[1]): ^35} ||\n'
                f'|| {"(Zone 3)": ^35} || {"(Zone 2)": ^35} || {"(Zone 1)": ^35} ||\n'
                f'=======================================================================================================================\n'
                f'|| {self.turn: ^113} ||'
                f'=======================================================================================================================\n'
                f'|| {"": ^35} || {"": ^35} || {"": ^35} ||\n'
                f'|| {str(self.enemyField[1]): ^35} || {str(self.enemyField[2]): ^35} || {str(self.enemyField[3]): ^35} ||\n'
                f'|| {"(Zone 1)": ^35} || {"(Zone 2)": ^35} || {"(Zone 3)": ^35} ||\n'
                f'=======================================================================================================================\n'
                f'|| {"": ^35} || {"": ^35} || {"": ^35} ||\n'
                f'|| {str(self.enemyField[4]): ^35} || {str(self.enemyField[5]): ^35} || {str(self.enemyField[6]): ^35} ||\n'
                f'|| {"(Zone 4)": ^35} || {"(Zone 5)": ^35} || {"(Zone 6)": ^35} ||\n'
                f'=======================================================================================================================\n'
                f'|| {"ENEMY BOARD": ^113} ||\n'
                f'=======================================================================================================================\n')