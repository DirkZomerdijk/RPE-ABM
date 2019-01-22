import numpy as np
from globals import *
import random
import networkx as nx
from scipy.stats import norm

def get_preference_list(N):
    preference_list = []
    for i in range(N):
        preference_list.append(set_reputation())

    return preference_list

def update_preference(my_preference, neighbors_preference):
    my_preference = my_preference + (K* sum([(neighbor - my_preference) for neighbor in neighbors_preference]))

def mean_neighbor_preference(neighbors):
    neighbor_preference = []
    for neighbor in neighbors:
        neighbor_preference.append(neighbor.preference)
    new_preference = sum(neighbor_preference) / float(len(neighbor_preference))
    return new_preference

def set_rand_unifrom_preference():
    return np.random.uniform(0,1)

def set_rand_normal_preference():
    return norm(0,1).pdf(np.random.randint(0,99))


def set_type():
    return random.choice(type_list)

def set_reputation():
    return random.uniform(0,10)

def get_payoff_matrix(reputationA,reputationB,convincing_powerA,convincing_powerB):
    return np.array([[reputationA, convincing_powerA], [reputationB,convincing_powerB]])


def play_game(payoff_matrix):
    game = nash.Game(payoff_matrix)
    for eq in game.support_enumeration():
        choiceA = np.where(eq[0] == max(eq[0]))[0]
        choiceB = np.where(eq[1] == max(eq[1]))[0]

        print(payoff_matrix[choiceA[0]][choiceB][0])


def compute_preferences(model):
    agent_preferences = [agent.preference for agent in model.schedule.agents]
    return np.mean(agent_preferences)

def compute_opinions(model):
    agent_opinions = [agent.opinion for agent in model.schedule.agents]
    return np.mean(agent_opinions)


def select_network_type(network_type, N, no_of_neighbors, beta_component):
    print(network_type)
    if(network_type == 1):
        print('watts_strogatz')
        return nx.watts_strogatz_graph(N, no_of_neighbors, beta_component, seed=None)
    elif(network_type == 2):
        print('barabasi_albert')
        return nx.barabasi_albert_graph(N, no_of_neighbors, seed=None)

def set_opinion():
    if random.uniform(0,1) > 0.5:
        return 0
    else:
        return 1