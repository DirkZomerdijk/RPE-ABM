from model import *  # omit this in jupyter notebooks

# network = Network(10,5, 2, .15)
# for i in range(100):
# 	network.step()

# agent_preference = network.datacollector.get_agent_vars_dataframe()
# print(agent_preference)
# print(network.datacollector.get_model_vars_dataframe())

# run
from server import server

server.port = 8244 # The default
server.launch()