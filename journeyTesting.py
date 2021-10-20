import networkx as nx
import pandas as pd

journey = pd.read_json("./data/journies/DS3_hard.json",orient="index")
G = nx.from_pandas_edgelist(journey, source = "from", target = "to")
nx.draw(G, with_labels=True)

