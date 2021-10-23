class Stamina:
    def __init__(self, staminaId, name, cardType, cost, fromSet, choices):
        self.staminaId = staminaId
        self.name = name
        self.cardType = cardType
        self.cost = cost
        self.fromSet = fromSet
        self.choices = choices
        
    def __str__(self): # String representation of card
        return (f'{self.name}')
    
    def __repr__(self): # Object representation of card
        return (f'{self.name}')