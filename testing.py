from resources import Loading
from player import Player
from journey import Journey

resources = Loading()       # Load game data
resources.sortEnemies()     # Sort enemies by level
resources.sortEncounters()  # Sort encounters by level


choices = ["Assassin", "Knight"]          # Player class choices go in here
players = []                    # List of player objects

p1 = Player(choices[0])         # Build player 1 object
p1.buildDeck(resources)         # Build deck for player 1

p2 = Player(choices[1])
p2.buildDeck(resources)

players.append(p1)              # Add to player roster
players.append(p2)

resources.playerSetup(players)  # Assign player data card to player object


journey = Journey("DS3_easy", resources, players)     # Load journey
journey.setEncounters()                        # Set encounters for journey
journey.travel("Area 1A")



