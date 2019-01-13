import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from agents import *

class Network(Model):
    def __init__(self, N):
        self.num_agents = N
        self.G = nx.watts_strogatz_graph(20, 2, 0, seed=None)
        print(self.G.nodes)

        self.num_agents = N
        self.num_nodes = num_nodes if num_nodes >= self.num_agents else self.num_agents
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=0.5)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)

    def fill_network(self):
        nx.set_node_attributes(self.G, [node.get_rand_expectation()]*self.num_agents, 'expectation')


test = Network(20)
