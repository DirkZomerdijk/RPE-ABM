from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random
from globals import *
class agent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.expectation = set_rand_unifrom_expectation()
        self.opinion = set_opinion()
        # print(self.expectation)


    def form_opinion(self, neighbors):
        #function 
        neighbor_expectation = []
        A_expectation = []
        B_expectation = []

        for neighbor in neighbors:
            neighbor_expectation.append(neighbor.expectation)
            if neighbor.opinion == 0:
                A_expectation.append(neighbor.expectation)
            else:
                B_expectation.append(neighbor.expectation)
                
        if(len(neighbor_expectation)!=0):
            probability_rate_A = sum(A_expectation)/sum(neighbor_expectation)
            probability_rate_B = sum(B_expectation)/sum(neighbor_expectation)

            if random.uniform(0,1) < probability_rate_A:
                self.opinion = 0
                # self.expectation = probability_rate_A
            else:
                self.opinion = 1
                # self.expectation = probability_rate_B

    def choose_neighbors(self, neighbors):
        selected_neighbors = []
        for neighbor in neighbors:
            connection_strength = self.model.G.edges[self.pos, neighbor.pos]['connection_strength']

            if( connection_strength > np.random.uniform(0,1)):
                selected_neighbors.append(neighbor)
                connection_strength += edge_strength_chance
            else: 
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

        # new_expectation = mean_neighbor_expectation(neighbors)
        # self.expectation = new_expectation
        # print(self.expectation)

    def step(self):
        # self.expectation += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():
