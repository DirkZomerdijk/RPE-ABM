from model import *  # omit this in jupyter notebooks

network = Network(N=100, no_of_neighbors=3, network_type=2, beta_component=.3, similarity_treshold=.025, social_influence=0.01, swingers=1, malicious_N=0, echo_threshold=0.25)

# for i in range(10):
	# network.step()
network.step()
# network.step()
# network.step()



agent_preference = network.datacollector.get_model_vars_dataframe()
print(agent_preference)
# print(network.datacollector.get_model_vars_dataframe())

# # run
# from server import server
# server.port = 8260 # The default
# server.launch()