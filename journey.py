import networkx as nx
import pandas as pd

class Journey:
    def __init__(self, journey):
        self.journey = pd.read_json(f"./{journey}.json",orient="index")
        self.G = nx.from_pandas_edgelist(self.journey, source = "from", target = "to")
        self.areas = list(self.G.nodes())
        self.currPos = "bonfire"
        self.clearedAreas = ["bonfire"] # For simplicity, "bonfire" is considered a cleared area
        
    def routeOptions(self): # List options from current position
        options = []
        edges = list(nx.edges(self.G,self.currPos))
        for pair in edges:
            options.append(pair[1])
        
        return options
    
    def cleared(self, encounter):
        print("Area cleared")
        self.clearedAreas.append(encounter)
    
    def changePos(self, choice):
        # TODO: Need to implement checks for areas that haven't been visited yet,
        # i.e., a player can't visit a boss without going through normal areas first.
        if choice in self.areas:
            print("Position Changed")
            self.currPos = choice
            return
        
    def returnToBonfire(self): # Returns party to bonfire
        possiblePaths = list(nx.all_simple_paths(self.G,source=self.currPos,target="bonfire"))
        cleared = set(self.clearedAreas)
        for option in possiblePaths:
            if set(option).issubset(cleared):
                print("Safely returned to bonfire.")
                self.currPos = "bonfire"
                return
            else:
                continue
        print("No safe path back to bonfire. Continue fighting enemies.") 