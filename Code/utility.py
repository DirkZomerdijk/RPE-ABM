import numpy as np
import random
import networkx as nx
from scipy.stats import norm

def get_expectation_list(N):
    expectation_list = []
    for i in range(N):
        expectation_list.append(set_reputation())

    return expectation_list

def mean_neighbor_expectation(neighbors):
    neighbor_expectation = []
    for neighbor in neighbors:
        neighbor_expectation.append(neighbor.expectation)
    new_expectation = sum(neighbor_expectation) / float(len(neighbor_expectation))
    return new_expectation

def set_rand_unifrom_expectation():
    return np.random.uniform(0,1)

def set_rand_normal_expectation():
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


def compute_expectations(model):
    agent_expectations = [agent.expectation for agent in model.schedule.agents]
    return np.mean(agent_expectations)

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