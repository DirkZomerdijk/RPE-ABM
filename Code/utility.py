import numpy as np
from globals import *
import random
import networkx as nx
from scipy.stats import norm
import matplotlib.pyplot as plt
import community as com
from community.community_louvain import best_partition
from collections import Counter
from operator import itemgetter

def get_preference_list(N):
    preference_list = []
    for i in range(N):
        preference_list.append(set_trust())

    return preference_list


def mean_neighbor_preference(neighbors):
    neighbor_preference = []
    for neighbor in neighbors:
        neighbor_preference.append(neighbor.preference)
    new_preference = sum(neighbor_preference) / float(len(neighbor_preference))
    return new_preference

def set_rand_unifrom_preference():
    return np.random.uniform(0,1)

def get_rand_similarity(similarity_treshold):
    lower_treshold = 0.0
    upper_treshold = similarity_treshold*2
    sample = 10
    while sample > upper_treshold or sample < lower_treshold:
        sample = random.gauss(similarity_treshold, np.std([lower_treshold, similarity_treshold, upper_treshold]))
        
    return sample

# def set_rand_normal_preference():
#     return norm(0,1).pdf(np.random.randint(0,99))


def set_type():
    return random.choice(type_list)

def set_trust():
    return random.uniform(0,10)

def get_payoff_matrix(trustA,trustB,convincing_powerA,convincing_powerB):
    return np.array([[trustA, convincing_powerA], [trustB,convincing_powerB]])


def play_game(payoff_matrix):
    game = nash.Game(payoff_matrix)
    for eq in game.support_enumeration():
        choiceA = np.where(eq[0] == max(eq[0]))[0]
        choiceB = np.where(eq[1] == max(eq[1]))[0]

        # print(payoff_matrix[choiceA[0]][choiceB][0])


def compute_preferences(model):
    agent_preferences = [agent.preference for agent in model.schedule.agents]
    return np.mean(agent_preferences)

def compute_opinions(model):
    agent_opinions = [agent.opinion for agent in model.schedule.agents]
    return np.mean(agent_opinions)

def compute_majority_opinions(model):
    agent_opinions = [agent.opinion for agent in model.schedule.agents]

    opinionB = sum(agent_opinions)
    opinionA = model.num_agents - sum(agent_opinions)

    difference = max([opinionA,opinionB])/model.num_agents
    

    return difference

#computes average preference of agents with opinion 
def compute_preference_A(model):
    preference_A = []
    for agent in model.schedule.agents:
        if (agent.opinion == 0): preference_A.append(agent.preference)
    return np.mean(preference_A)

def compute_preference_B(model):
    preference_B = []
    for agent in model.schedule.agents:
        if (agent.opinion == 1): preference_B.append(agent.preference)
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
    trusts = list(nx.get_edge_attributes(model.G,'trust').values())
    # print(trusts)
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
    nx.draw_networkx_nodes(model.G, model.layout, node_size=1, node_color=nodes_preferences_A, nodelist=nodes_A, cmap=plt.cm.Blues)
    nx.draw_networkx_nodes(model.G, model.layout, node_size=1, node_color=nodes_preferences_B, nodelist=nodes_B, cmap=plt.cm.Reds)
    nx.draw_networkx_edges(model.G, model.layout, alpha=0.5, width=[(rep) for rep in trusts])
    plt.axis('off')



    plt.savefig('img/fig'+str(model.step_no)+'.png', dpi=800, facecolor='w', edgecolor='w',
            orientation='portrait', papertype=None, format=None,
            transparent=False, bbox_inches=None, pad_inches=0.1,
            frameon=None, metadata=None)    
    plt.show()
    # G = nx.draw_networkx(model.G, model.layout,node_color=)
    # plt.show()

def get_communities(model):
    return best_partition(model.G, weight='trust')

#From largest to smallest. Default largest community.
def community_all(model):
    community_partitions = get_communities(model)
    no = max(community_partitions.values())
    coms = []
    for i in range(no):
        value, count = Counter(community_partitions.values()).most_common(no+1)[i]
        pop_agents = []
        for a in model.G.nodes():
            if(community_partitions.get(a)==value):
                pop_agents.append(model.schedule.agents[a])

        pop_pref = 0
        pop_opi = 0
        for x in pop_agents:
            pop_opi += x.opinion
            pop_pref += x.preference
        pop_opi = pop_opi/len(pop_agents)
        pop_pref = pop_pref/len(pop_agents)
        coms.append([pop_opi, pop_pref, count])
    return coms

def echo_no(model):
    coms = community_all(model)
    counter = 0
    for c in coms:
        if(c[0]>=1-model.echo_threshold or c[0]<=model.echo_threshold): counter += 1
    return counter


def community_no(model):
    community_partitions = get_communities(model)
    return max(community_partitions.values())+1

def select_network_type(network_type, N, no_of_neighbors, beta_component):
    # print(network_type)
    if(network_type == 1):
        # print('watts_strogatz')
        return nx.watts_strogatz_graph(N, no_of_neighbors, beta_component, seed=None)
    elif(network_type == 2):
        # print('barabasi_albert')
        return nx.barabasi_albert_graph(N, no_of_neighbors, seed=None)

def set_opinion():
    if random.uniform(0,1) > 0.5:
        return 0
    else:
        return 1

def compute_silent_spiral(model):

    opinions = []
    node_information = []

    for node in model.G.nodes():
        neighbors_nodes = model.grid.get_neighbors(node, include_center = False)
        node_opinion = model.G.nodes[node]['agent'][0].opinion
        opinions.append(node_opinion)
        
        connectivity = 0        
        # connections = len(neighbors_nodes)
        

        for neighbor_node in neighbors_nodes:
            connectivity += model.G.edges[node,neighbor_node]['trust']

        # node_information.append([node, node_opinion,connectivity/connections])
        node_information.append([node, node_opinion,connectivity])


    node_information.sort(key=itemgetter(2))
    # print(node_information)
    Bs = sum(opinions)
    As = len(opinions)-Bs

    if(As > Bs):
        major = 0
    else:
        major = 1


    # print(Bs, As)
    # print(int(len(node_information)*.1))
    # print([1 if node[1] == major else 0 for node in node_information[:int(len(node_information)*.05)]])
    perc_of_major = sum([1 if node[1] == major else 0 for node in node_information[:int(len(node_information)*.05)]])/int(model.num_agents*.1)
    return perc_of_major
        # node_trusts[node]['opinion'] = node_opinion
        # if node_opinion == 0:
        #     # print()
        #     maj_min['A'].append((node,node_trusts[node]))
        # else:
        #     maj_min['B'].append((node,node_trusts[node]))

    # if len(maj_min['A']) > len(maj_min['B']):
    #     major = 'A'
    #     minor = 'B'
    # else:
    #     major = 'B'
    #     minor = 'A'

    # major_

    # print(node_trusts)
    # print()
    # print(maj_min)
    # print()
    # print(connectivities)


        # print(nx.average_degree_connectivity(model.G, weight = 'weight'))
    # no_A = len(maj_min['A']) 
    # no_B = len(maj_min['B'])



    # print(no_A, no_B, no_A/no_B)
    # print(maj_min)
