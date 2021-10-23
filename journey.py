import networkx as nx
import pandas as pd
import random
from battlefield import Battlefield

class Journey:
    def __init__(self, journey, resources, players):
        self.journey = pd.read_json(f"./data/journies/{journey}.json",orient="index")
        self.G = nx.from_pandas_edgelist(self.journey, source = "from", target = "to")
        self.rawAreas, self.setAreas = list(self.G.nodes()), list(self.G.nodes())
        self.currPos = "Bonfire"
        self.clearedAreas = ["Bonfire"]     # For simplicity, "bonfire" is always considered a cleared area
        self.mapping = {}                   # For relabeling graph G
        self.players = players
        self.resources = resources
        self.battlefield = Battlefield(self.players, self.resources)    # Setting the battlefield
        
        
    def routeOptions(self): # List options from current position
        """
        Determine the possible routes that can be taken from the party's 
        current position.

        Returns
        -------
        options : List
            List of possible encounters to travel to from current position.
        """
        options = []
        edges = list(nx.edges(self.G,self.currPos))
        for pair in edges:
            options.append(pair[1])
        return options
    
    
    def setEncounters(self):     
        """
        Set up battlefield with random encounters. Also relabels journey map
        represented by graph G with names of encounters. Encounter object look-up
        is performed with default 'area' and 'boss' strings.

        Returns
        -------
        None.
        """
        for index,area in enumerate(self.setAreas):
            if "Area 1" in area:
                choice = random.choice(self.resources.level1Encounters)  # Select a random encounter
                self.resources.level1Encounters.remove(choice)           # Remove to prevent duplicate encounters
                self.setAreas[index] = choice                       # Replace placeholder with encounter object
                self.mapping[area] = choice                         # Mapping for relabeling graph
                
            elif "Area 2" in area:
                choice = random.choice(self.resources.level2Encounters)
                self.resources.level2Encounters.remove(choice)
                self.setAreas[index] = choice
                self.mapping[area] = choice
                
            elif "Area 3" in area:
                choice = random.choice(self.resources.level3Encounters)
                self.resources.level3Encounters.remove(choice)
                self.setAreas[index] = choice
                self.mapping[area] = choice

        self.G = nx.relabel_nodes(self.G, self.mapping)             # Relabel graph with encounters
        self.objLookup = dict(zip(self.rawAreas, self.setAreas))    # For ease of looking up areas
        #nx.draw(self.G, with_labels=True)                          # For testing purposes, remove later
    
    
    def cleared(self, encounter):
        """
        Clears the specified encounter after defeating all enemies in that encounter.
        Also can be used for debugging.

        Parameters
        ----------
        encounter : TYPE
            DESCRIPTION.

        Returns
        -------
        None.
        """
        print(f"{encounter}: {self.objLookup[encounter]} cleared.")
        self.clearedAreas.append(self.objLookup[encounter])
    
    
    def travel(self, choice):
        """
        Changes the position of the player on the journey board.
        
        Parameters
        ----------
        choice : String
            A string of the location that the player wants to travel to.

        Returns
        -------
        bool
            Returns True after successfully traveling, False when path is blocked or invalid input.
        """
        areasToClear = []
        if self.currPos == choice:
            print(f"Already at {choice}.")
        elif choice in self.objLookup:
            possiblePaths = list(nx.all_simple_paths(self.G, source=self.currPos, target=self.objLookup[choice]))
            cleared = set(self.clearedAreas)
            for option in possiblePaths:
                areasToClear.extend(option)
                path = set(option[:-1])
                if path.issubset(cleared):
                    print(f"Traveled to {choice}: {self.objLookup[choice]}. Let the battle begin.")
                    self.currPos = self.objLookup[choice]
                    self.startBattle(choice)
                    return True
                else:                                                       # Ignore paths that can't be taken
                    continue
            areasToClear =  set(areasToClear).difference(self.clearedAreas) # Removes duplicates and cleared areas
            areasToClear.remove(self.objLookup[choice])                     # Also remove choice as it isn't a preliminary area that needs to be cleared

            print(f"Cannot travel to {choice}: {self.objLookup[choice]}. Areas that can be cleared first: {areasToClear}")
            return False
        else:
            print("Not a valid area.")
            return False        
    
    
    def startBattle(self, choice):
        """
        Starts the encounter after changing positions to that location.
        Starting the encounter is composed of generating the appropriate
        enemies, placing those enemies, setting the encounter name, and
        starting the battle phase.
    
        Parameters
        ----------
        choice : String
            A string of the location that the player wants to travel to.

        Returns
        -------
        None.
        """
        enemies = self.battlefield.generateEnemies(self.objLookup, choice)   # Generate enemies
        self.battlefield.placement(enemies)                                                  # Place classes and enemies
        self.battlefield.setEncounterName(self.objLookup[choice])                                          # Set name for encounter
        print(self.battlefield)
        self.battlefield.battlePhase()                                                         # Enemies attack immediately after starting encounter
    
    
    def returnToBonfire(self):
        """
        Returns the party to the bonfire.

        Returns
        -------
        None.
        """
        if self.currPos == "Bonfire":
            print("Already at Bonfire.")
        
        possiblePaths = list(nx.all_simple_paths(self.G, source=self.currPos, target="Bonfire"))
        cleared = set(self.clearedAreas)
        for option in possiblePaths:
            if set(option).issubset(cleared):   # If possible path is made up of cleared areas, you can return to bonfire
                print("Safely returned to Bonfire.")
                self.currPos = "Bonfire"
                return
            else:                               # Ignore complex paths
                continue
        print("No safe path back to bonfire. Continue fighting enemies.") 