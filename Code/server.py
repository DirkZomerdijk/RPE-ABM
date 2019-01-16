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
  portrayal['nodes'] = [{ 'id': node_id,
                          'Shape': 'circle',
                          'size': 0.2 ,
                          'color': '#CC0000' if not agents or agents[0].opinion == 0 else '#007959',
                          # 'label': 'Agent:{} expectation:{}'.format(agents[0].unique_id, agents[0].expectation),
                          'label': 'expectation:{0:.2f}'.format(agents[0].expectation),

                        }
                        for (node_id, agents) in G.nodes.data('agent')]

  portrayal['edges'] = [{ 'id': edge_id,
                          'source': source,
                          'target': target,
                          'color': edge_color,
                        }
                        for edge_id, (source, target) in enumerate(G.edges)]

  return portrayal


grid = NetworkModule(network_portrayal, 400, 600, library='sigma')
chart = ChartModule([{"Label": "expectations",
                      "Color": "Black"}],
                    data_collector_name='datacollector')


agents_slider = UserSettableParameter('slider', "Number of Agents", 10, 2, 800, 1)
neighbors_slider = UserSettableParameter('slider', "Number of Neighbors", 3, 2, 10, 1)
network_slider = UserSettableParameter('slider', "Network Type", 1,1,2,1)
beta_slider = UserSettableParameter('slider', "Beta Component (Only for Watts-Strogatz [1])", 0.5, 0,1,0.01)

model_params = {
    "N": agents_slider,
    "no_of_neighbors": neighbors_slider,
    "network_type": network_slider, 
    "beta_component": beta_slider,
}  


server = ModularServer(Network, [grid,chart], "NetworkModel", model_params) 
