import numpy as np
from globals import *
import random
import networkx as nx
from scipy.stats import norm
import matplotlib.pyplot as plt

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

#computes average preference of agents with opinion 
def compute_preference_A(model):
    preference_A = []
    for agent in model.schedule.agents:
        if (agent.opinion == 0): preference_A.append(agent.preference)
    return np.mean(preference_A)

def compute_preference_B(model):
    preference_B = []
    for agent in model.schedule.agents:
        if (agent.opinion == 0): preference_B.append(agent.preference)
    return np.mean(preference_B)

#Computes percentage of those holding radical opinions (>0.8)
def compute_radical_opinions(model):
    radical_counter = 0
    for agent in model.schedule.agents:
        if (agent.preference >0.8): radical_counter += 1
    return radical_counter/model.num_agents

def return_network(model):
    nodes_A = []
    nodes_B = []
    nodes_preferences_A = []
    nodes_preferences_B = []
    reputations = list(nx.get_edge_attributes(model.G,'reputation').values())
    # print(reputations)
    # model.layout = nx.spring_layout(model.G, dim=2)

    for node in model.G.nodes():
        model.G.nodes()[node]['opinion'] = model.G.nodes()[node]["agent"][0].opinion
        model.G.nodes()[node]['preference'] = model.G.nodes()[node]["agent"][0].preference
        model.G.nodes()[node]['id'] = node

        if model.G.nodes()[node]['opinion'] == 0:
            nodes_A.append(node)
            nodes_preferences_A.append(model.G.nodes()[node]["agent"][0].preference)

        else:
            nodes_B.append(node)
            nodes_preferences_B.append(model.G.nodes()[node]["agent"][0].preference)

    fig = plt.figure(dpi=500)
    nx.draw_networkx_nodes(model.G, model.layout, node_size=50, node_color=nodes_preferences_A, nodelist=nodes_A, cmap=plt.cm.Blues)
    nx.draw_networkx_nodes(model.G, model.layout, node_size=50, node_color=nodes_preferences_B, nodelist=nodes_B, cmap=plt.cm.Reds)
    nx.draw_networkx_edges(model.G, model.layout, alpha=0.5, width=[(rep*10) for rep in reputations])
    plt.axis('off')
    # plt.show()
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image
    # G = nx.draw_networkx(model.G, model.layout,node_color=)
    # plt.show()

#def community_no(model):
#    commuity_partitions = community.best_partition(model.G, weight='weight')


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