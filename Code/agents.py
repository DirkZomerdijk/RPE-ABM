from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random

class agent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.expectation = set_rand_normal_expectation()
        self.opinion = set_opinion()
        print(self.expectation)


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

        probability_rate_A = sum(A_expectation)/sum(neighbor_expectation)
        probability_rate_B = sum(B_expectation)/sum(neighbor_expectation)
        if random.uniform(0,1) < probability_rate_A:
            self.opinion = 0
            # self.expectation = probability_rate_A
        else:
            self.opinion = 1
            # self.expectation = probability_rate_B

    def talk(self):
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)

        self.form_opinion(neighbors)

        # new_expectation = mean_neighbor_expectation(neighbors)
        # self.expectation = new_expectation
        # print(self.expectation)

    def step(self):
        # self.expectation += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():
