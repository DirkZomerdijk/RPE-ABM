# server.py
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from model import Network
from utility import *
from globals import *


def network_portrayal(G):

    portrayal = dict()
    portrayal['nodes'] = [{'id': node_id,
                           'size': 3 ,
                           'color': '#007959',
                           'label': 'Agent:{} expectation:{}'.format(agents[0].unique_id, agents[0].expectation),
                           }
                          for (node_id, agents) in G.nodes.data('agent')]

    portrayal['edges'] = [{'id': edge_id,
                           'source': source,
                           'target': target,
                           'color': '#000000',
                           }
                          for edge_id, (source, target) in enumerate(G.edges)]

    return portrayal

grid = NetworkModule(network_portrayal, 500, 500, library='sigma')
server = ModularServer(Network,
                       [grid],
                       "NetworkModel",
                       {"N": no_of_nodes})
