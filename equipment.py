class Equipment:
    def __init__(self, equipmentId, name, cardType, weakness, fromSet, choices):
        self.equipmentId = equipmentId
        self.name = name
        self.cardType = cardType
        self.weakness = weakness
        self.fromSet = fromSet
        self.choices = choices
        
    def __str__(self): # String representation of card
        return (f'{self.name}')
    
    def __repr__(self): # Object representation of card
        return (f'{self.name}')