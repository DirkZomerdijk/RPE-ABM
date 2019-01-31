from globals import *
import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from agents import *
from utility import *
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
from heapq import nlargest



class Network(Model):

    def __init__(self, N, no_of_neighbors, network_type, beta_component, similarity_treshold, social_influence, swingers, malicious_N, echo_threshold, all_majority=False):  
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
        self.swingers = swingers
        self.malicious_N = malicious_N
        self.malistious = []
        self.echo_threshold = echo_threshold
        self.all_majority = all_majority
	   # Initialy set to 1 agreement and 1 agreement to avoid 100%/0% probability scenrarios
        nx.set_edge_attributes(self.G, 2, 'total_encounters')
        nx.set_edge_attributes(self.G, 1, 'times_agreed')
        nx.set_edge_attributes(self.G, .5, 'trust')
        
        self.place_agents()

        self.set_malicious()
        
        self.datacollector = DataCollector(
            model_reporters={
                "preferences": compute_preferences,
                "percentage_majority_opinion": compute_opinions,
                "preference_A": compute_preference_A,
                "preference_B": compute_preference_B,
                "radical_opinions": compute_radical_opinions,
                "community_no": community_no,
                "community_all": community_all,
                "silent_spiral": compute_silent_spiral,
                "echo_no": echo_no
                # "graph": return_network
            },
            agent_reporters={
                "preference": "preference",
            }) 

        self.running = True
        # return_network(self)

    # place agents on network
    def place_agents(self):
        for i in range(self.num_agents):            
            a = agent(i, self)
            self.grid.place_agent(a, self.node_list[i])
            self.schedule.add(a)

    # Update trust between nodes
    def update_edge(self, node1, node2):
        # Get opinion of agents
        opinionA = self.G.nodes()[node1]['agent'][0].opinion
        opinionB = self.G.nodes()[node2]['agent'][0].opinion   

        self.G.edges[node1, node2]['total_encounters'] += 1
        # If agents share opinion, edge strength increases
        if(opinionA == opinionB):
            self.G.edges[node1, node2]['times_agreed'] += 1

        self.G.edges[node1, node2]['trust'] = self.G.edges[node1, node2]['times_agreed'] /  self.G.edges[node1, node2]['total_encounters']      

    def step(self):
        # nx.draw(self.G, pos=nx.spring_layout(self.G))
        # plt.show()
        self.datacollector.collect(self)
        self.perturb_network()
        self.schedule.step()
        self.step_no +=1
<<<<<<< HEAD
        for a in self.malistious:
            a.opinion = 0
            a.preference = 1
            neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
            neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)
            for neighbor in neighbors:
                self.model.G.edges[self.pos,neighbor.pos]['reputation'] = 1
            
        # print(nx.get_edge_attributes(self.G, 'reputation'))
=======
        # print(nx.get_edge_attributes(self.G, 'trust'))
>>>>>>> 5ca08f3e2d9180c1f6b61c3eb7c4b90cb490ed52

    def perturb_network(self):
        agent_nodes = np.random.randint(self.num_agents, size=(1,self.swingers))
        for node in agent_nodes:
            agent = self.G.nodes()[np.random.randint(self.num_agents)]['agent'][0]
            agent.opinion = np.random.randint(2)
            agent.preference = set_rand_unifrom_preference()

    def set_malicious(self):
        centrality_dict = nx.degree_centrality(self.G)  
        most_central = nlargest(self.malicious_N, centrality_dict, key=centrality_dict.get)
        test = 0
        for a in most_central:
            self.G.nodes()[a]["agent"][0].opinion = 0
            self.G.nodes()[a]["agent"][0].preference = 1
            self.malistious.append(self.G.nodes()[a]["agent"][0])

