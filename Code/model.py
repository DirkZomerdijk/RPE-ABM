import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from agents import *

class Network(Model):
    def __init__(self, N):
        self.num_agents = N
        self.G = nx.watts_strogatz_graph(20, 2, 0, seed=None)
        print(G.nodes)

    def fill_network(self, node):
        nx.set_node_attributes(self.G, [node.get_rand_expectation()]*self.num_agents, 'expectation')


test = Network(20)
