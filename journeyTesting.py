import networkx as nx
import pandas as pd

DS3_Easy = pd.read_json("./Dark Souls 3 (Easy).json",orient="index")
G = nx.from_pandas_edgelist(DS3_Easy, source = "from", target = "to")
nx.draw(G, with_labels=True)

areas = list(G.nodes()) # All areas in journey
currPos = "bonfire" # Current position, start at bonfire

def routeOptions(currPos, G):
    options = []
    edges = list(nx.edges(G,currPos))
    for pair in edges:
        options.append(pair[1])
    return options

def changePos(choice, areas):
    if choice in areas:
        return choice

def returnToBonfire(currPos, cleared, G):
    possiblePaths = list(nx.all_simple_paths(G,source=currPos,target="bonfire"))
    cleared = set(cleared)
    for option in possiblePaths:
        if set(option).issubset(cleared):
            print("Safely returned to bonfire.")
            currPos = changePos("bonfire", areas)
            return
        else:
            continue
    
    print("No safe path back to bonfire. Continue fighting enemies.") 

currPos = changePos("area 2a", areas)

cleared = ["bonfire","area 1b","boss 1","area 3a","area 2a"]

#print(routeOptions(currPos, G))
returnToBonfire(currPos, cleared, G)