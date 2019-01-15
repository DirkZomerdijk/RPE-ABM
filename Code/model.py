import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from agents import *
from utility import *
from mesa.space import NetworkGrid

class Network(Model):

    def __init__(self, N):  
        self.num_agents = N
        self.G = nx.watts_strogatz_graph(N, 2, 0, seed=None)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)

        node_list = self.random.sample(self.G.nodes(), self.num_agents)

        for i in range(self.num_agents):            
            a = agent(i, self)
            self.grid.place_agent(a, node_list[i])
            self.schedule.add(a)

    def step(self):
        self.schedule.step()

    def run_model(no_of_agents, steps):
    	network = Network(no_of_agents)
    	for i in range(steps):
            network.step()

    # def step(self):
    #   self.schedule.step()
    #   self.datacollector.collect(self)




Network.run_model(no_of_agents = 4, steps = 1)
# network.fill_network()

# print(vars(network.G.node[0]['agent'][0]))
# print(vars(network.G.node[2]['agent'][0]))
# print(vars(network.G.node[4]['agent'][0]))



