class Card_Enemy:
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
        
    def __str__(self): # String representation of card
        return (f'{self.name}')