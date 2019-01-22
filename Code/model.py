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
        # self.node_positions = nx.spring_layout(self.G)
        self.node_list = self.random.sample(self.G.nodes(), self.num_agents)
        
	   # Initialy set to 1 agreement and 1 agreement to avoid 100%/0% probability scenrarios
        nx.set_edge_attributes(self.G, 2, 'total_encounters')
        nx.set_edge_attributes(self.G, 1, 'times_agreed')
        
        self.place_agents()
        self.set_edges()


        self.datacollector = DataCollector(
            model_reporters={
                "preferences": compute_opinions
            },
            agent_reporters={
                "preference": "preference",
            }) 

        self.running = True

    # initialize edge strenghts
    def set_edges(self):
        for edge in self.G.edges():
            
            opinionA = self.G.nodes()[edge[0]]['agent'][0].opinion
            opinionB = self.G.nodes()[edge[1]]['agent'][0].opinion
    
            self.G.edges[edge[0], edge[1]]['total_encounters'] += 1
    
            if(opinionA == opinionB):
                self.G.edges[edge[0], edge[1]]['times_agreed'] += 1

    # place agents on network
    def place_agents(self):
        for i in range(self.num_agents):            
            a = agent(i, self)
            self.grid.place_agent(a, self.node_list[i])
            self.schedule.add(a)

    # Update reputation between nodes
    def update_edge(node1, node2):
        # Get opinion of agents
        opinionA = self.G.nodes()[node1]['agent'][0].opinion
        opinionB = self.G.nodes()[node2]['agent'][0].opinion              
        self.G.edges[node1, node2]['total_encounters'] += 1

        # If agents share opinion, edge strength increases
        if(opinionA == opinionB):
            self.G.edges[node1, node2]['times_agreed'] += 1

    def step(self):
        # nx.draw(self.G, pos=nx.spring_layout(self.G))
        # plt.show()
        self.datacollector.collect(self)
        self.schedule.step()


