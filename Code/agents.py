from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random
import nashpy as nash
import numpy as np

class agent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.expectation = get_rand_expectation()
        self.type = get_type()
        self.convincing_power = type_dict[self.type]
        self.reputation = set_reputation()

<<<<<<< HEAD
    def talk(self):
        neighbor_nodes = self.get_neighbor_nodes()
        # [print(i) for i in neighbor_nodes]
=======

    def talk(self):
        # Get neighbours
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)

        # Share expecatition with neighbors
        for neighbor in neighbors:

            payoff_matrix = get_payoff_matrix(self.reputation, neighbor.reputation, self.convincing_power, neighbor.convincing_power)
            game = nash.Game(payoff_matrix)

            print(payoff_matrix)
            for eq in game.support_enumeration():
                choiceA = np.where(eq[0] == max(eq[0]))[0]
                choiceB = np.where(eq[1] == max(eq[1]))[0]

                print(payoff_matrix[choiceA[0]][choiceB][0])
                break
>>>>>>> 9b744d7105a81cf9a38b8bf534c470e8e0d47989


    def step(self):
        # self.expectation += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():



