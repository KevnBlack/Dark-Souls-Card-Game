import networkx as nx
import pandas as pd
import random
from battlefield import Battlefield

class Journey:
    def __init__(self, journey, classChoices, resources):
        self.journey = pd.read_json(f"./data/journies/{journey}.json",orient="index")
        self.G = nx.from_pandas_edgelist(self.journey, source = "from", target = "to")
        self.rawAreas, self.setAreas = list(self.G.nodes()), list(self.G.nodes())
        self.currPos = "Bonfire"
        self.clearedAreas = ["Bonfire"] # For simplicity, "bonfire" is always considered a cleared area
        self.mapping = {} # For relabeling graph G
        self.battlefield = Battlefield()
        self.classChoices = classChoices
        self.resources = resources
        
    def routeOptions(self): # List options from current position
        options = []
        edges = list(nx.edges(self.G,self.currPos))
        for pair in edges:
            options.append(pair[1])
        
        return options
    
    def setEncounters(self, resources):
        level1Encounters, level2Encounters, level3Encounters = [], [], []
        for name,encounter in resources.encounterDatabase.items(): # Sort encounters by level
            if encounter.level == 1:
                level1Encounters.append(encounter)
            elif encounter.level == 2:
                level2Encounters.append(encounter)
            else:
                level3Encounters.append(encounter)
        
        for index,area in enumerate(self.setAreas):         # Set up battlefield with random encounters
            if "Area 1" in area:
                choice = random.choice(level1Encounters)    # Select a random encounter
                level1Encounters.remove(choice)             # Remove to prevent duplicate encounters
                self.setAreas[index] = choice               # Replace placeholder with encounter object
                self.mapping[area] = choice                 # Mapping for relabeling graph
                
            elif "Area 2" in area:
                choice = random.choice(level2Encounters)
                level2Encounters.remove(choice)
                self.setAreas[index] = choice
                self.mapping[area] = choice
                
            elif "Area 3" in area:
                choice = random.choice(level3Encounters)
                level3Encounters.remove(choice)
                self.setAreas[index] = choice
                self.mapping[area] = choice

        self.G = nx.relabel_nodes(self.G, self.mapping) # Relabel graph with encounters
        self.objLookup = dict(zip(self.rawAreas, self.setAreas)) # For ease of looking up areas
        #nx.draw(self.G, with_labels=True) # For testing purposes, remove later
    
    def cleared(self, encounter):
        print(f"{encounter}: {self.objLookup[encounter]} cleared.")
        self.clearedAreas.append(self.objLookup[encounter])
    
    def changePos(self, choice):
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
                    print(f"Traveled to {choice}: {self.objLookup[choice]}.")
                    print("Let the battle begin.")
                    self.currPos = self.objLookup[choice]
                    self.startBattle(choice)
                    return True
                else: # Ignore paths that can't be taken
                    continue
            areasToClear =  set(areasToClear).difference(self.clearedAreas) # Removes duplicates and cleared areas
            areasToClear.remove(self.objLookup[choice]) # Also remove choice as it isn't a preliminary area that needs to be cleared

            print(f"Cannot travel to {choice}: {self.objLookup[choice]}. Areas that can be cleared first: {areasToClear}")
            return False
        else:
            print("Not a valid area.")
            return False        
    
    def startBattle(self, choice):
        enemies = self.battlefield.generateEnemies(self.objLookup, self.resources, self.classChoices, choice)
        self.battlefield.placement(self.classChoices,enemies)
        print(self.battlefield)
        self.battlefield.enemyAttack()
    
    def returnToBonfire(self): # Returns party to bonfire
        if self.currPos == "Bonfire":
            print("Already at Bonfire.")
        
        possiblePaths = list(nx.all_simple_paths(self.G, source=self.currPos, target="Bonfire"))
        cleared = set(self.clearedAreas)
        for option in possiblePaths:
            if set(option).issubset(cleared): # If possible path is made up of cleared areas, you can return to bonfire
                print("Safely returned to Bonfire.")
                self.currPos = "Bonfire"
                return
            else: # Ignore complex paths
                continue
        print("No safe path back to bonfire. Continue fighting enemies.") 