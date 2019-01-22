from model import *  # omit this in jupyter notebooks

# network = Network(no_of_nodes, 4, 1)
# for i in range(no_of_steps):
#     network.step()

# agent_preference = network.datacollector.get_agent_vars_dataframe()
# print(agent_preference)
# print(network.datacollector.get_model_vars_dataframe())

# run
from server import server

server.port = 8224 # The default
server.launch()