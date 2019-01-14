from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random

class agent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.expectation = get_rand_expectation()




    def talk(self):
        neighbor_nodes = self.get_neighbor_nodes()
        # [print(i) for i in neighbor_nodes]


    def step(self):
        # self.expectation += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():
