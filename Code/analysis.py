import networkx as nx
import community as com
from community.community_louvain import best_partition
from collections import Counter
import numpy as np
from operator import itemgetter
import copy

def compute_preferences(model):
    agent_preferences = [agent.preference for agent in model.schedule.agents]
    return np.mean(agent_preferences)

def compute_opinions(model):
    if(model.opinions <=2):
        agent_opinions = [agent.opinion for agent in model.schedule.agents]
        return np.mean(agent_opinions)
    else:
        return 'opinions>2'

def compute_transitivity(model):
    print(nx.average_clustering(model.G, nodes=None, weight="trust", count_zeros=True))
    return nx.average_clustering(model.G, nodes=None, weight="trust", count_zeros=True)

def compute_majority_opinions(model):
    agent_opinions = [agent.opinion for agent in model.schedule.agents]
    agent_opinions = Counter(agent_opinions)
    opinion_sizes = [agent_opinions[key] for key in agent_opinions.keys()]

    difference = max(opinion_sizes)/model.num_agents  

    return difference

def compute_majority_opinion(agents):
    agent_opinions = [agent.opinion for agent in agents]
    agent_opinions = Counter(agent_opinions)
    opinion_sizes = [agent_opinions[key] for key in agent_opinions.keys()]

    difference = max(opinion_sizes)/len(agents) 

    return difference

def compute_echo_chamber(model):
    # print("compute_echo_chamber")
    # print(nx.is_directed(model.G))
    hidden = hide_edges(model)
    # print(nx.enumerate_all_cliques(hidden.G))

    cliques = list(nx.enumerate_all_cliques(hidden.G))
    # print(vars(model.G.nodes[0]))
    cliques = [[model.G.nodes()[node]["agent"][0].opinion for node in clique] for clique in cliques if len(clique)>2]
    echo_chambers = [echo for echo in cliques if len(set(echo)) == 1]
    if len(echo_chambers)>0:
        model.sizes_of_echochambers = Counter([len(chamber) for chamber in echo_chambers])
        model.no_of_echochambers = len(echo_chambers)/model.cliques
    print(model.sizes_of_echochambers)
    
    return len(cliques)

def echochamber_size(model):
    return model.sizes_of_echochambers

def echochamber_count(model):
    return model.no_of_echochambers

def hide_edges(input):
    model = copy.deepcopy(input)
    # print(model)
    # print(input)
    # print(len(model.G.edges()))
    edges = []
    for edge in model.G.edges():
        # print(model.G.edges[edge])
        if model.G.edges[edge]["trust"] < model.echo_limit:
            edges.append(edge)
    # print(edges)
    model.G.remove_edges_from(edges)
    return model




# #computes average preference of agents with opinion 
# def compute_preference_A(model):
#     preference_A = []
#     for agent in model.schedule.agents:
#         if (agent.opinion == 0): preference_A.append(agent.preference)
#     return np.mean(preference_A)

# def compute_preference_B(model):
#     preference_B = []
#     for agent in model.schedule.agents:
#         if (agent.opinion == 1): preference_B.append(agent.preference)
#     return np.mean(preference_B)

#Computes percentage of those holding radical opinions (>0.8)
def compute_radical_opinions(model):
    radical_counter = 0
    for agent in model.schedule.agents:
        if (agent.preference >0.8): radical_counter += 1
    return radical_counter/model.num_agents


def get_communities(model):
    return best_partition(model.G, weight='trust')

# From largest to smallest. Default largest community.
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
        pop_opi = []
        for x in pop_agents:
            # pop_opi.append(x.opinion)
            pop_pref += x.preference
        pop_opi = compute_majority_opinion(pop_agents)
        pop_pref = pop_pref/len(pop_agents)
        # pop_opi = Counter(pop_opi)
        coms.append([pop_opi, pop_pref, count])
        # pop_pref = 0
        # pop_opi = 0
        # for x in pop_agents:
        #     pop_opi += x.opinion
        #     pop_pref += x.preference
        # pop_opi = pop_opi/len(pop_agents)
        # pop_pref = pop_pref/len(pop_agents)
        # coms.append([pop_opi, pop_pref, count])
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

def compute_silent_spiral(model):

    opinions = []
    node_information = []

    for node in model.G.nodes():
    
        neighbors_nodes = model.grid.get_neighbors(node, include_center = False)
        node_opinion = model.G.nodes[node]['agent'][0].opinion
        opinions.append(node_opinion)
        connectivity = 0        

        for neighbor_node in neighbors_nodes:
            connectivity += model.G.edges[node,neighbor_node]['trust']

        node_information.append([node, node_opinion, connectivity])


    node_information.sort(key=itemgetter(2))

    opinion_count = Counter(opinions)
    opinion_freq = [opinion_count[i] for i in opinion_count]
    majority_opinion = opinion_freq.index(max(opinion_freq))
    silent_spiral_nodes = [1 if node[1] == majority_opinion else 0 for node in node_information[:int(len(node_information)*.05)]]
    groupsize = len(silent_spiral_nodes)
    perc_of_major = sum(silent_spiral_nodes)/groupsize

    return perc_of_major
    
def average_trust(model):
    return np.mean(list(nx.get_edge_attributes(model.G,'trust').values()))

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