'''
Wolf-Sheep Predation Model
================================
Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

from globals import *
from agents import *
from utility import *
from analysis import *
import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
from heapq import nlargest



class Network(Model):
    '''
    Wolf-Sheep Predation Model
    '''
    def __init__(self, N, no_of_neighbors, network_type, beta_component, similarity_treshold, social_influence, swingers, malicious_N, all_majority, opinions, echo_limit, seed=None):  
        '''
        Create a new Wolf-Sheep model with the given parameters.
        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
        '''
        super().__init__()
        # Set parameters
        self.num_agents = N
        self.seed = seed
        self.G = self.select_network_type(network_type, N, no_of_neighbors, beta_component) #nx.watts_strogatz_graph(N, no_of_neighbors, rand_neighbors, seed=None)
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
        self.malicious = []
        self.all_majority = all_majority
        self.opinions = opinions
        self.no_of_echochambers = 0
        self.sizes_of_echochambers = 0
        self.cliques = len(list(nx.enumerate_all_cliques(self.G)))
        self.echo_limit = echo_limit


	    # Initialy set to 1 agreement and 1 agreement to avoid 100%/0% probability scenrarios
        nx.set_edge_attributes(self.G, 2, 'total_encounters')
        nx.set_edge_attributes(self.G, 1, 'times_agreed')
        nx.set_edge_attributes(self.G, .5, 'trust')
        
        # Create sheep:
        self.place_agents()

        # Create sheep:
        self.set_malicious()
        
        self.datacollector = DataCollector(
           model_reporters={
                # "preferences": compute_preferences,
                "percentage_majority_opinion": compute_majority_opinions,
                # "percentage_opinion": compute_opinions,
                # # "preference_A": compute_preference_A,
                # # "preference_B": compute_preference_B,
                "radical_opinions": compute_radical_opinions,
                # "community_no": community_no,
                # "silent_spiral": compute_silent_spiral,
                # "echo_no": echo_no,
                # "average_trust": average_trust,
                # "graph": return_network
                "compute_transitivity":compute_transitivity,
                "compute_echo_chamber":compute_echo_chamber,
                "echochamber_size":echochamber_size,
                "echochamber_count":echochamber_count,
                "malicious_N":compute_malicious_N,
                "self.step_no":compute_step_no

            },
        #    agent_reporters={
        #        "preference": "preference",
        #    }
            ) 

        self.running = True

    def select_network_type(self, network_type, N, no_of_neighbors, beta_component):
        if(network_type == 1):
            # print('watts_strogatz')
            return nx.watts_strogatz_graph(N, no_of_neighbors, beta_component, seed=None)
        elif(network_type == 2):
            # print('barabasi_albert')
            return nx.barabasi_albert_graph(N, no_of_neighbors, seed=None)

    # place agents on network
    def place_agents(self):
        for i in range(self.num_agents):            
            a = agent(i, self)
            self.grid.place_agent(a, self.node_list[i])
            self.schedule.add(a)

    # Update trust between nodes
    def update_edge(self, node1, node2):
        # Get opinion of agents
        self.G.edges[node1, node2]['total_encounters'] += 1
        # If agents share opinion, edge strength increases
        if(self.G.nodes()[node1]['agent'][0].opinion == self.G.nodes()[node2]['agent'][0].opinion ):
            self.G.edges[node1, node2]['times_agreed'] += 1

        self.G.edges[node1, node2]['trust'] = self.G.edges[node1, node2]['times_agreed'] /  self.G.edges[node1, node2]['total_encounters']      

            
    def perturb_network(self):
        agent_nodes = np.random.randint(self.num_agents, size=(1,self.swingers))
        for node in agent_nodes:
            agent = self.G.nodes()[np.random.randint(self.num_agents)]['agent'][0]
            edges = self.G.edges(node)
            for edge in edges:
                self.G.edges[edge]["trust"] = set_rand_unifrom_preference()
            agent.opinion = np.random.randint(2)
            agent.preference = set_rand_unifrom_preference()

    def set_malicious(self):
        centrality_dict = nx.degree_centrality(self.G)  
        most_central = nlargest(self.malicious_N, centrality_dict, key=centrality_dict.get)
        test = 0
        for a in most_central:
            self.G.nodes()[a]["agent"][0].opinion = 0
            self.G.nodes()[a]["agent"][0].preference = 1
            self.malicious.append(self.G.nodes()[a]["agent"][0])

    def step(self):
        # collect data
        self.datacollector.collect(self)
        self.perturb_network()
        self.schedule.step()

        if(self.malicious_N > 0):
            for a in self.malicious:
                a.opinion = 0
                a.preference = 1
                neigbors_nodes = self.grid.get_neighbors(a.pos, include_center = False)
                neighbors = self.grid.get_cell_list_contents(neigbors_nodes)
                for neighbor in neighbors:
                    self.G.edges[a.pos,neighbor.pos]['trust'] = 1

        self.step_no +=1

