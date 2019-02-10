'''
Runs the model normal, or by using server
'''

from model import *  

# Initialize network
network = Network(N=100, no_of_neighbors=3, network_type=2, beta_component=.3, similarity_treshold=.006, social_influence=0.16, swingers=5, malicious_N=2, all_majority=False,opinions=2, echo_limit = 0.95, seed=2)

# Set number of steps
no_of_steps = 1

# Run model
for i in range(no_of_steps):
	network.step()


# Print data
agent_preference = network.datacollector.get_model_vars_dataframe()
print(network.datacollector.get_model_vars_dataframe())


# # run on server
# from server import server
# server.port = 8262 
# server.launch()   
