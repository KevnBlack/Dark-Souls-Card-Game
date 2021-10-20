class ClassCards:
    def __init__(self, classId, name, taunt, ability, usedAbility, placement, fromSet):
        self.classId = classId
        self.name = name
        self.taunt = taunt
        self.ability = ability
        self.usedAbility = usedAbility
        self.placement = placement
        self.fromSet = fromSet
        
    def __str__(self): # String representation of card
        return (f'{self.name}')