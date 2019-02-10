'''
Functions for model analysis.
Used for computing:
    Preferences (mean)
    Opinions (mean)
    Transitivity
    Majority opinion
    Number of echo chambers
    Sizes of echo chambers
    Radical Opinions
'''

import networkx as nx
import community as com
from community.community_louvain import best_partition
from collections import Counter
import numpy as np
from operator import itemgetter
import copy

def compute_preferences(model):
    '''
    Computes mean preference if number of opinions == 2
    '''
    agent_preferences = [agent.preference for agent in model.schedule.agents]
    return np.mean(agent_preferences)

def compute_opinions(model):
    '''
    Computes mean opinion if number of opinions == 2
    '''
    if(model.opinions <=2):
        agent_opinions = [agent.opinion for agent in model.schedule.agents]
        return np.mean(agent_opinions)
    else:
        return 'opinions>2'

def compute_transitivity(model):
    '''
    Computes transitivity using networkx average clustering
    '''    
    return nx.average_clustering(model.G, nodes=None, weight="trust", count_zeros=True)

def compute_majority_opinions(model):
    '''
    Computes majority opinion after model run
    '''    
    agent_opinions = [agent.opinion for agent in model.schedule.agents]
    agent_opinions = Counter(agent_opinions)
    opinion_sizes = [agent_opinions[key] for key in agent_opinions.keys()]

    difference = max(opinion_sizes)/model.num_agents  

    return difference

def compute_majority_opinion(agents):
    '''
    Computes majority opinion during model run
    '''    
    agent_opinions = [agent.opinion for agent in agents]
    agent_opinions = Counter(agent_opinions)
    opinion_sizes = [agent_opinions[key] for key in agent_opinions.keys()]

    difference = max(opinion_sizes)/len(agents) 

    return difference

def compute_echo_chamber(model):
    '''
    Computes sizes and number of echo chambers
    '''    

    # hides edges based on threshold (echo_limit)
    hidden = hide_edges(model)

    # calculate cliques
    cliques = list(nx.enumerate_all_cliques(hidden.G))

    # select cliques where size >= 3
    cliques = [[model.G.nodes()[node]["agent"][0].opinion for node in clique] for clique in cliques if len(clique)>2]
    echo_chambers = [echo for echo in cliques if len(set(echo)) == 1]

    if len(echo_chambers)>0:
        model.sizes_of_echochambers = Counter([len(chamber) for chamber in echo_chambers])
        model.no_of_echochambers = len(echo_chambers)/model.cliques
    
    return len(cliques)

def echochamber_size(model):
    return model.sizes_of_echochambers

def echochamber_count(model):
    return model.no_of_echochambers

def hide_edges(input):
    '''
    hides edges based on threshold (echo_limit)
    '''
    model = copy.deepcopy(input)
    edges = []
    for edge in model.G.edges():
        if model.G.edges[edge]["trust"] < model.echo_limit:
            edges.append(edge)
    model.G.remove_edges_from(edges)
    return model

def compute_malicious_N(model):
    return model.malicious_N

def compute_step_no(model):
    return model.step_no

def compute_radical_opinions(model):
    '''
    Computes percentage of agents holding radical opinions (preference > 0.8)
    '''
    radical_counter = 0
    for agent in model.schedule.agents:
        if (agent.preference > 0.8): radical_counter += 1
    return radical_counter/model.num_agents

def get_communities(model):
    '''
    Computes communities using community louvain's best partition
    '''
    return best_partition(model.G, weight='trust')

def community_no(model):
    '''
    Computes largest community
    '''
    community_partitions = get_communities(model)
    return max(community_partitions.values())+1

def compute_silent_spiral(model):
    '''
    Computes 5% least connected (trust) agents. Returns the percentage of least connected agents with majority opinion 
    '''
    opinions = []
    node_information = []

    # select all nodes and calculate their connectivity
    for node in model.G.nodes():
        neighbors_nodes = model.grid.get_neighbors(node, include_center = False)
        node_opinion = model.G.nodes[node]['agent'][0].opinion
        opinions.append(node_opinion)
        connectivity = 0        
        for neighbor_node in neighbors_nodes:
            connectivity += model.G.edges[node,neighbor_node]['trust']

        node_information.append([node, node_opinion, connectivity])

    # Sort based on connectivity
    node_information.sort(key=itemgetter(2))

    # calculate majority opinion
    opinion_count = Counter(opinions)
    opinion_freq = [opinion_count[i] for i in opinion_count]
    majority_opinion = opinion_freq.index(max(opinion_freq))

    # calculate percentage of silent spiral nodes having majority opinion
    silent_spiral_nodes = [1 if node[1] == majority_opinion else 0 for node in node_information[:int(len(node_information)*.05)]]
    groupsize = len(silent_spiral_nodes)
    perc_of_major = sum(silent_spiral_nodes)/groupsize

    return perc_of_major
    
def average_trust(model):
    '''
    Computes average trust (edge strength)
    '''    
    return np.mean(list(nx.get_edge_attributes(model.G,'trust').values()))

def return_network(model):
    '''
    Returns figure of model.
    '''        
    nodes_A = []
    nodes_B = []
    nodes_preferences_A = []
    nodes_preferences_B = []
    trusts = list(nx.get_edge_attributes(model.G,'trust').values())

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