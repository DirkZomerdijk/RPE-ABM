import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation

class NetworkModel(Model):
    def __init__(self, N):
        self.num_agents = N

        G = nx.watts_strogatz_graph(20, 2, 0, seed=None)
        print(G.nodes)

test = NetworkModel(20)
