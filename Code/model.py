'''
Opinion Forming Model
================================
Model which aims to gain insight in the influence of comfirmation bias and social influence
on the formation of opinions. We tend to find the following stylised facts:

    Transitivity
    Majority opinion
    Echo chambers
    Radical Opinions

'''

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
    Opinion forming model
    '''
    def __init__(self, N, no_of_neighbors, network_type, beta_component, similarity_treshold, social_influence, swingers, malicious_N, all_majority, opinions, echo_limit, seed=None):  
        '''
        Create a new Opinion forming model with the given parameters.
        Args:
            N: Number of agents in network.
            no_of_neighbors: Number of neighbors for each node.
            network_type: Network type to use.
            beta_component: if network type is small world: this is the beta-component.
            similarity_treshold: The range in which similarity holds (difference in prefference if opinion is shared).
            social_influence: The influence of neighboring agents on the forming of a new preference.
            swingers: Number of agents which switches opinion, preference, and trust with each timestep.
            malicious_N: Number of malicious agents .
            all_majority: If true: all agents except malicious agents have the same opinion.
            opinions: Number of opinions.
            echo_limit: Limit for edge strenght for echo chamber calculation.
            seed: If used: determines the number of unique networks.
        '''
        super().__init__()

        self.num_agents = N
        self.seed = seed
        self.G = self.select_network_type(network_type, N, no_of_neighbors, beta_component) #nx.watts_strogatz_graph(N, no_of_neighbors, rand_neighbors, seed=None)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)
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
        
        # Place agents:
        self.place_agents()

        # Place malicious agents:
        self.set_malicious()

        # Collect data
        self.datacollector = DataCollector(
           model_reporters={
                # "preferences": compute_preferences,
                "percentage_majority_opinion": compute_majority_opinions,
                # "percentage_opinion": compute_opinions,
                # # "preference_A": compute_preference_A,
                # # "preference_B": compute_preference_B,
                "radical_opinions": compute_radical_opinions,
                "community_no": community_no,
                "silent_spiral": compute_silent_spiral,
                # "echo_no": echo_no,
                # "average_trust": average_trust,
                # "graph": return_network
                "compute_transitivity":compute_transitivity,
                "compute_echo_chamber":compute_echo_chamber,
                "echochamber_size":echochamber_size,
                "echochamber_count":echochamber_count,
                "malicious_N":compute_malicious_N,
                "self.step_no":compute_step_no

            }
        ) 

        self.running = True

    def place_agents(self):
        '''
        place agents on network
        '''

        for i in range(self.num_agents):            
            a = agent(i, self)
            self.grid.place_agent(a, self.node_list[i])
            self.schedule.add(a)

    def set_malicious(self):
        '''
        place malicious agents on network
        '''

        # Select most connected nodes
        centrality_dict = nx.degree_centrality(self.G)  
        most_central = nlargest(self.malicious_N, centrality_dict, key=centrality_dict.get)

        # For the number of malicious agents update the most connected agents switch opinion to 0 and preference to 1
        for a in most_central:
            self.G.nodes()[a]["agent"][0].opinion = 0
            self.G.nodes()[a]["agent"][0].preference = 1
            self.malicious.append(self.G.nodes()[a]["agent"][0])

    def step(self):
        '''
        A model step. 
            Collect data of model. 
            Perturb network. 
            Perform step for all agents. 
            Update Malicious agents.
        ''' 

        # collect data
        self.datacollector.collect(self)

        # perturb network
        self.perturb_network()

        # Make all agents step
        self.schedule.step()

        # Update all malicious agents
        self.update_malicious_agents()

        # Update step number
        self.step_no +=1

    def perturb_network(self):
        '''
        Perturbs the network: changes opinion, preference and trust for a number of swingers
        '''
        agent_nodes = np.random.randint(self.num_agents, size=(1,self.swingers))
        for node in agent_nodes:
            agent = self.G.nodes()[np.random.randint(self.num_agents)]['agent'][0]
            edges = self.G.edges(node)
            for edge in edges:
                self.G.edges[edge]["trust"] = set_rand_unifrom_preference()
            agent.opinion = np.random.randint(2)
            agent.preference = set_rand_unifrom_preference()

    def update_malicious_agents(self):
        if(self.malicious_N > 0):
            
            for a in self.malicious:
                a.opinion = 0
                a.preference = 1
                neigbors_nodes = self.grid.get_neighbors(a.pos, include_center = False)
                neighbors = self.grid.get_cell_list_contents(neigbors_nodes)
                
                for neighbor in neighbors:
                    self.G.edges[a.pos,neighbor.pos]['trust'] = 1    

    def select_network_type(self, network_type, N, no_of_neighbors, beta_component):
        '''
        Returns an initialized network type using: 
        network type (int)
        N (int)
        no_of_neighbors (int)
        beta_comopnent (float)
        '''
        if(network_type == 1):
            return nx.watts_strogatz_graph(N, no_of_neighbors, beta_component, seed=None)
        elif(network_type == 2):
            return nx.barabasi_albert_graph(N, no_of_neighbors, seed=None)

    def update_edge(self, node1, node2):
        '''
        Update trust between nodes based on previous encounters and times agreed (shared opinions)
        '''

        # increment total encounters
        self.G.edges[node1, node2]['total_encounters'] += 1

        # If agents share opinion, increment times agreed
        if(self.G.nodes()[node1]['agent'][0].opinion == self.G.nodes()[node2]['agent'][0].opinion ):
            self.G.edges[node1, node2]['times_agreed'] += 1

        # Calculate new trust
        self.G.edges[node1, node2]['trust'] = self.G.edges[node1, node2]['times_agreed'] /  self.G.edges[node1, node2]['total_encounters']      




