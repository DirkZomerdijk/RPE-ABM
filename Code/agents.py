from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random
from globals import *
class agent(Agent):
    """ An agent with fixed initial preference and opinion."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.preference = set_rand_unifrom_preference()
        self.opinion = set_opinion()
        # print(self.preference)

    
    def select_A(self, A_preference):
        """ Adapt preference score and opinion to A"""
        if self.opinion == 1:
            self.preference = 1 - self.preference
        
        self.opinion = 0
        self.update_preference(A_preference)

    def select_B(self, B_preference):
        """ Adapt preference score and opinion to A"""
        if self.opinion == 0:
            self.preference = 1 - self.preference

        self.opinion = 1
        self.update_preference(B_preference)

    def form_opinion(self, neighbors):
        """ Function to determine if opninion needs to be adapted based on neighbors""" 
        neighbor_preference = []
        A_preference = []
        B_preference = []


        for neighbor in neighbors:
            neighbor_preference.append(neighbor.preference)
            if neighbor.opinion == 0:
                A_preference.append(neighbor.preference)
            else:
                B_preference.append(neighbor.preference)

        if( len(neighbor_preference) != 0):
            probability_rate_A = sum(A_preference)/sum(neighbor_preference)
            probability_rate_B = sum(B_preference)/sum(neighbor_preference)

            if (self.opinion == 0) and (probability_rate_B < self.preference):
                self.select_A(A_preference)
            
            elif (self.opinion == 1) and (probability_rate_A < self.preference):
                self.select_B(B_preference)

            elif random.uniform(0,1) < probability_rate_A:
                self.select_A(A_preference)
            else:
                self.select_B(B_preference)


    def choose_neighbors(self, neighbors):
        """ Choose whitch neighbors to talk with based on trust"""
        selected_neighbors = []
        similar_neighbors = []
        for neighbor in neighbors:
            # trust = self.model.G.edges[self.pos,neighbor.pos]['times_agreed']/self.model.G.edges[self.pos,neighbor.pos]['total_encounters']
            # neighbor_preference = neighbor.preference
            # own_preference = self.preference
            
            # neighbor_opinion = neighbor.opinion
            # own_opinion = self.opinion

            # neighbor_position  = neighbor.pos
            # own_position = self.pos

            trust = self.model.G.edges[self.pos,neighbor.pos]['trust']

            if((neighbor.opinion == self.opinion) and (abs(neighbor.preference - self.preference) < get_rand_similarity(self.model.similarity_treshold))):
                similar_neighbors.append(neighbor)
                self.update_trust(neighbor.pos)
            else:
                # print('dissimilar')
                # print('different opinion')
                if(trust > np.random.uniform(0,1)):
                    selected_neighbors.append(neighbor)
                    self.update_trust(neighbor.pos)

        if(len(similar_neighbors) != 0):
            return similar_neighbors
        else:
            return selected_neighbors

    def update_trust(self, neighbor_position):
        # print('update preference')
        self.model.update_edge(self.pos, neighbor_position)

        # print('rep of node ' +str(self.pos)+' and '+str(neighbor.pos)+': ' +str(self.model.G.edges[self.pos, neighbor.pos]['trust']))

    def update_preference(self, neighbors_preference):
        self.preference = self.preference + (self.model.social_influence * sum([(neighbor - self.preference) for neighbor in neighbors_preference]))

    def talk(self):
        '''
        Agent sees neighbors. Select neighbors to talk with (based on edge strenght). Increase connection strength if shared opinion. 
        Start Discussion, chance opinion according to probabilitiy function
        '''
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)
        selected_neighbors = self.choose_neighbors(neighbors)
        self.form_opinion(selected_neighbors)
        # self.update_neigboring_trusts(selected_neighbors)

        # new_preference = mean_neighbor_preference(neighbors)
        # self.preference = new_preference
        # print(self.preference)

    def step(self):
        # self.preference += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():
