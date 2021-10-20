class Bonfire:
    def __init__(self, bonfireId, name, level, deckMax, fromSet):
        self.bonfireId = bonfireId
        self.name = name
        self.level = level
        self.deckMax = deckMax
        self.fromSet = fromSet
        
    def __str__(self): # String representation of bonfire
        return (f'{self.name} ({self.level})\n'
                f'Max Deck Size:{self.deckMax}')