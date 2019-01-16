from globals import *
import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from agents import *
from utility import *
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector



class Network(Model):

    def __init__(self, N, no_of_neighbors, network_type, beta_component):  
        self.num_agents = N
        self.G = select_network_type(network_type, N, no_of_neighbors, beta_component) #nx.watts_strogatz_graph(N, no_of_neighbors, rand_neighbors, seed=None)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)

        self.node_list = self.random.sample(self.G.nodes(), self.num_agents)

        for i in range(self.num_agents):            
            a = agent(i, self)
            self.grid.place_agent(a, self.node_list[i])
            self.schedule.add(a)

        self.datacollector = DataCollector(
            model_reporters={
                "expectations": compute_opinions
            },
            agent_reporters={
                "expectation": "expectation",
            }) 

        self.running = True
    

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        # print("new step")

    # def run_model(self, n):
    #     for i in range(n):
    #         self.step()


    # def step(self):
    #   self.schedule.step()
    #   self.datacollector.collect(self)






# network.fill_network()

# print(vars(network.G.node[0]['agent'][0]))
# print(vars(network.G.node[2]['agent'][0]))
# print(vars(network.G.node[4]['agent'][0]))



