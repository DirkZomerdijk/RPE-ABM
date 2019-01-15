from model import *  # omit this in jupyter notebooks

# network = Network(5)
# for i in range(10):
#     network.step()

# agent_expectation = network.datacollector.get_agent_vars_dataframe()
# print(agent_expectation)

# run.py
from server import server
server.port = 8521 # The default
server.launch()