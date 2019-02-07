from model import *  # omit this in jupyter notebooks

network = Network(N=1000, no_of_neighbors=4, network_type=2, beta_component=.3, similarity_treshold=.006, social_influence=0.16, swingers=5, malicious_N=2, echo_threshold=0.25, all_majority=False,opinions=2, echo_limit = 0.95, seed=2)

for i in range(2):
	network.step()
# network.step()
# network.step()
# network.step()



agent_preference = network.datacollector.get_model_vars_dataframe()
# print(agent_preference)
print(network.datacollector.get_model_vars_dataframe())


# # run
# from server import server
# server.port = 8261 # The default
# server.launch()   
