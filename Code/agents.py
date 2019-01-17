from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random
from globals import *
class agent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.preference = set_rand_unifrom_preference()
        self.opinion = set_opinion()
        # print(self.preference)


    def form_opinion(self, neighbors):
        #function 
        neighbor_preference = []
        A_preference = []
        B_preference = []

        for neighbor in neighbors:
            neighbor_preference.append(neighbor.preference)
            if neighbor.opinion == 0:
                A_preference.append(neighbor.preference)
            else:
                B_preference.append(neighbor.preference)

        if(len(neighbor_preference)!=0):
            probability_rate_A = sum(A_preference)/sum(neighbor_preference)
            probability_rate_B = sum(B_preference)/sum(neighbor_preference)

            if random.uniform(0,1) < probability_rate_A:
                self.opinion = 0
                # self.preference = probability_rate_A
            else:
                self.opinion = 1
                # self.preference = probability_rate_B

    def choose_neighbors(self, neighbors):
        selected_neighbors = []
        for neighbor in neighbors:
            connection_strength = self.model.G.edges[self.pos, neighbor.pos]['connection_strength']

            if( connection_strength > np.random.uniform(0,1)):
                selected_neighbors.append(neighbor)
                if(connection_strength < high_edge_strength):
                    connection_strength += edge_strength_chance
            else: 
                if(connection_strength > low_edge_strength):
                    connection_strength -= edge_strength_chance

        return selected_neighbors

    def talk(self):
        '''
        Agent sees neighbors. Select neighbors to talk with (based on edge strenght). Increase connection strength if shared opinion. 
        Start Discussion, chance opinion according to probabilitiy function
        '''
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)
        selected_neighbors = self.choose_neighbors(neighbors)

        self.form_opinion(selected_neighbors)

        # new_preference = mean_neighbor_preference(neighbors)
        # self.preference = new_preference
        # print(self.preference)

    def step(self):
        # self.preference += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():
