'''
Script for running model on server
'''
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import NetworkModule
from model import Network
from utility import *

def network_portrayal(G):
  '''
  Function returns portrayal for network
  '''
  colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33']
  edge_color = '#000000'

  portrayal = dict()
  portrayal['nodes'] = [{ 'id': node_id,
                          'Shape': 'circle',
                          'size': 0.2 ,
                          'color': colors[agents[0].opinion],
                          'label': 'opinion:{0:.2f}'.format(agents[0].opinion),
                        }
                        for (node_id, agents) in G.nodes.data('agent')]

  portrayal['edges'] = [{ 'id': edge_id,
                          'source': source,
                          'target': target,
                          'color': edge_color,
                        }
                        for edge_id, (source, target) in enumerate(G.edges)]

  return portrayal


# Initilize grid and chart
grid = NetworkModule(network_portrayal, 400, 600, library='sigma')
chart = ChartModule([{"Label": "percentage_majority_opinion",
                      "Color": "Black"
                    }], data_collector_name='datacollector')


# Initilize sliders controling paramteres
agents_slider = UserSettableParameter('slider', "Number of Agents", 1000, 2, 1000, 1)
neighbors_slider = UserSettableParameter('slider', "Number of Neighbors", 3, 2, 10, 1)
network_slider = UserSettableParameter('slider', "Network Type", 1,1,2,1)
beta_slider = UserSettableParameter('slider', "Beta Component (Only for Watts-Strogatz [1])", 0.3, 0,1,0.01)
similarity_slider = UserSettableParameter('slider', "Similarity Treshold", 0.025, 0,0.1,0.001)
social_influence_slider = UserSettableParameter('slider', "Social Influence", 0.01, 0,0.1,0.01)
swingers_slider = UserSettableParameter('slider', "Swingers p Timestep", 4, 0,100,2)
malicious_slider = UserSettableParameter('slider', "Number of Malicious Agents", 0, 0,20,1)
echo_slider = UserSettableParameter('slider', "Threshold for Echo Chamber Classification", .25, 0, 0.5, 0.01)
opinion_slider = UserSettableParameter('slider', "Number of opinions", 2, 2, 10, 1)

model_params = {
    "N": agents_slider,
    "no_of_neighbors": neighbors_slider,
    "network_type": network_slider, 
    "beta_component": beta_slider,
    "similarity_treshold":similarity_slider,
    "social_influence":social_influence_slider,
    "swingers": swingers_slider,
    "malicious_N": malicious_slider,
    "echo_limit": echo_slider,
    "all_majority":False,
    "opinions": opinion_slider
}  

# run model on server
server = ModularServer(Network, [grid,chart], "NetworkModel", model_params) 
