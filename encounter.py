class Encounter:
    def __init__(self, encounterId, name, level, traps, terrain, fromSet, encounter):
        self.encounterId = encounterId
        self.name = name
        self.level = level
        self.traps = traps
        self.terrain = terrain
        self.fromSet = fromSet
        self.encounter = encounter
        
    def __str__(self): # String representation of encounter
        return (f'{self.name}')