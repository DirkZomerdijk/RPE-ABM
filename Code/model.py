from globals import *
import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from agents import *
from utility import *
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector




class Network(Model):

    def __init__(self, N, no_of_neighbors, network_type, beta_component, similarity_treshold, social_influence):  
        self.num_agents = N
        self.G = select_network_type(network_type, N, no_of_neighbors, beta_component) #nx.watts_strogatz_graph(N, no_of_neighbors, rand_neighbors, seed=None)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
        # self.node_positions = nx.spring_layout(self.G)
        self.node_list = self.random.sample(self.G.nodes(), self.num_agents)
        self.layout = nx.spring_layout(self.G, dim=2)
        self.step_no = 0
        self.similarity_treshold = similarity_treshold
        self.social_influence = social_influence
	   # Initialy set to 1 agreement and 1 agreement to avoid 100%/0% probability scenrarios
        nx.set_edge_attributes(self.G, 2, 'total_encounters')
        nx.set_edge_attributes(self.G, 1, 'times_agreed')
        nx.set_edge_attributes(self.G, .5, 'reputation')
        
        self.place_agents()
        
        self.datacollector = DataCollector(
            model_reporters={
                "preferences": compute_preferences,
                "opinions": compute_opinions,
                "preference_A": compute_preference_A,
                "preference_B": compute_preference_B,
                "radical_opinions": compute_radical_opinions,
                # "graph": return_network
            },
            agent_reporters={
                "preference": "preference",
            }) 

        self.running = True


    # place agents on network
    def place_agents(self):
        for i in range(self.num_agents):            
            a = agent(i, self)
            self.grid.place_agent(a, self.node_list[i])
            self.schedule.add(a)

    # Update reputation between nodes
    def update_edge(self, node1, node2):
        # Get opinion of agents
        opinionA = self.G.nodes()[node1]['agent'][0].opinion
        opinionB = self.G.nodes()[node2]['agent'][0].opinion   

        total_encounters = self.G.edges[node1, node2]['total_encounters']      
        times_agreed = self.G.edges[node1, node2]['times_agreed']

        total_encounters += 1
        # If agents share opinion, edge strength increases
        if(opinionA == opinionB):
            times_agreed += 1

        self.G.edges[node1, node2]['reputation'] = times_agreed /  total_encounters

    def step(self):
        # nx.draw(self.G, pos=nx.spring_layout(self.G))
        # plt.show()
        self.datacollector.collect(self)
        self.schedule.step()
        self.step_no +=1


