from model import *  # omit this in jupyter notebooks

network = Network(N=10, no_of_neighbors=5, network_type=2, beta_component=.15, similarity_treshold=.025, social_influence=0.01, swingers=1)
for i in range(50):
	network.step()

# agent_preference = network.datacollector.get_agent_vars_dataframe()
# print(agent_preference)
# print(network.datacollector.get_model_vars_dataframe())

# # run
from server import server
server.port = 8253 # The default
server.launch()