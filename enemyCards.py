class EnemyCards:
    def __init__(self, enemyId, name, level, power, defense, HP, souls, weakness, inflicts, condition, ability, placement, attacks, fromSet):
        self.enemyId = enemyId
        self.name = name
        self.level = level
        self.power = power
        self.defense = defense
        self.HP = HP
        self.souls = souls
        self.weakness = weakness
        self.inflicts = inflicts
        self.condition = condition
        self.ability = ability
        self.placement = placement
        self.attacks = attacks
        self.fromSet = fromSet
    
    '''
    def enemyAttack(self, bf):
        for zone,enemy in bf.enemyField.items(): # Enemy attack order
            frontMax, backMax = bf.getMaxTaunts() # Get taunts at beginning of each enemy activation
            if enemy is None: # Skip empty zones
                continue
            else:
                for attackZone in enemy.attacks: # Cycle through attack zones per enemy
                    if len(enemy.attacks) == 1: # For single attacks
                        if bf.friendlyField[attackZone] is None and attackZone in [1,2,3]: # If attack zone in player board is empty and in front row
                            if bf.friendlyField[1] is None and bf.friendlyField[2] is None and bf.friendlyField[3] is None:
                                print(f'{enemy} attacks {bf.friendlyField[backMax]}!') # Aim for highest taunt in back row if front is empty
                            else:
                                print(f'{enemy} attacks {bf.friendlyField[frontMax]}!') # Initially aim for highest taunt player in front row
                        elif bf.friendlyField[attackZone] is None and attackZone in [4,5,6]: # If attack zone in player board is empty and in back row
                            if bf.friendlyField[4] is None and bf.friendlyField[5] is None and bf.friendlyField[6] is None:
                                print(f'{enemy} attacks {bf.friendlyField[frontMax]}!') # Aim for highest taunt in front row if back is empty
                            else:
                                print(f'{enemy} attacks {bf.friendlyField[backMax]}!')  # Initially aim for highest taunt player in back row
                        else:
                            print(f'{enemy} attacks {bf.friendlyField[attackZone]}!') # Enemy lands hit
                    
                    elif len(enemy.attacks) > 1: # For AOE attacks
                        occupiedPlayerZones = bf.getOccupiedPlayerZones()
                        if len(set.intersection(set(enemy.attacks),set(occupiedPlayerZones))) == 0: # If the enemy attack zones aim at no players
                            print(f'{enemy} missed completely!')
                            break # Missed, so move on to next enemy if any
                        elif bf.friendlyField[attackZone] is None: # Skip empty zones
                            continue
                        else:
                            print(f'{enemy} attacks {bf.friendlyField[attackZone]}!') # Enemy lands hit    
    '''
    
    def __str__(self): # String representation of card
        return (f'{self.name}')
    
    def __repr__(self): # Object representation of card
        return (f'{self.name}')