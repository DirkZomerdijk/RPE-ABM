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
        
        nx.set_edge_attributes(self.G, 1, 'connection_strength')


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

        for edge in self.G.edges():
            # print(edge.connection_strength)
            
            opinionA = self.G.nodes()[edge[0]]['agent'][0].opinion
            opinionB = self.G.nodes()[edge[1]]['agent'][0].opinion
            if(opinionA == opinionB):
                self.G.edges[edge[0], edge[1]]['connection_strength'] += .1
            else:
                self.G.edges[edge[0], edge[1]]['connection_strength'] -= .1

            # print(opinionA)
            
            # break


    def update_edge(node1, node2):
        # Get opinion of agents
        opinionA = self.G.nodes()[node1]['agent'][0].opinion
        opinionB = self.G.nodes()[node2]['agent'][0].opinion              
        
        # If agents share opinion, edge strength increases
        if(opinionA == opinionB):
            self.G.edges[node1, node2]['connection_strength'] += .1
        else:
            self.G.edges[node1, node2]['connection_strength'] -= .1


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



