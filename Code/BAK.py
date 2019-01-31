from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random
import nashpy as nash
import numpy as np

class agent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.preference = get_rand_preference()
        self.type = get_type()
        self.convincing_power = type_dict[self.type]
        self.trust = set_trust()


    def talk(self):
        # Get neighbours
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)

        # Share expecatition with neighbors
        for neighbor in neighbors:

            payoff_matrix = get_payoff_matrix(self.trust, neighbor.trust, self.convincing_power, neighbor.convincing_power)
            game = nash.Game(payoff_matrix)

            print(payoff_matrix)
            for eq in game.support_enumeration():
                choiceA = np.where(eq[0] == max(eq[0]))[0]
                choiceB = np.where(eq[1] == max(eq[1]))[0]

                print(payoff_matrix[choiceA[0]][choiceB][0])
                break


    def step(self):
        # self.preference += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():





import random
import numpy as np

type_list = ['convincing', 'normal', 'unconvincing']
type_dict = {'convincing':5, 'normal':3, 'unconvincing':1}

def get_preference_list(N):
    preference_list = []
    for i in range(N):
        preference_list.append(get_rand_preference())

    return preference_list


def get_rand_preference():
    mean = 5.5
    stdev = 5.5/5.5   # 99.73% chance the sample will fall in your desired range

    return float("%.2f" % random.gauss(mean, stdev))

def get_type():
    return random.choice(type_list)

def set_trust():
    return random.uniform(0,5)

def get_payoff_matrix(trustA,trustB,convincing_powerA,convincing_powerB):
    # return np.array([[ [trustA, convincing_powerA], [trustB,convincing_powerB]],
 #             [[convincing_powerA, trustB], [convincing_powerA, convincing_powerB]] ] )
    return np.array([[trustA, convincing_powerA], [trustB,convincing_powerB]])


import networkx as nx
from mesa import Agent, Model
from mesa.time import RandomActivation
from agents import *
from utility import *
from mesa.space import NetworkGrid

class Network(Model):

    def __init__(self, N):  
        self.num_agents = N
        self.G = nx.watts_strogatz_graph(N, 2, 0, seed=None)
        self.grid = NetworkGrid(self.G)
        self.schedule = RandomActivation(self)

        node_list = self.random.sample(self.G.nodes(), self.num_agents)

        for i in range(self.num_agents):            
            a = agent(i, self)
            self.grid.place_agent(a, node_list[i])
            self.schedule.add(a)

    def step(self):
        self.schedule.step()

    def run_model(self, n):
        for i in range(n):
            self.step()


    # def step(self):
    #   self.schedule.step()
    #   self.datacollector.collect(self)





network = Network(4)
network.step()
# network.fill_network()

# print(vars(network.G.node[0]['agent'][0]))
# print(vars(network.G.node[2]['agent'][0]))
# print(vars(network.G.node[4]['agent'][0]))



