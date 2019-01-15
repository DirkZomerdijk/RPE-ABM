from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random

class agent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.expectation = set_rand_expectation()
        self.type = set_type()
        self.convincing_power = type_dict[self.type]
        self.reputation = set_reputation()


    def talk(self):
        # Get neighbours
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)

        # Share expecatition with neighbors
        for neighbor in neighbors:
            play_game(get_payoff_matrix(self.reputation, neighbor.reputation, self.convincing_power, neighbor.convincing_power))



    def step(self):
        # self.expectation += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():
