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
from mesa.batchrunner import BatchRunner
fixed_params = {"no_of_neighbors": 2,
                "network_type": 1,
                "beta_component": .15,
                "N": 1000,
                "similarity_treshold": 0.025,
                "social_influence": 0.025,
                "malicious_N":0,
                "echo_threshold":0.25
               }
vari_params = {"swingers": [1, 2, 3]}


batch_run = BatchRunner(Network,
                        iterations=1,
                        fixed_parameters=fixed_params,
                        variable_parameters= vari_params,
                        max_steps=100,
                        model_reporters={
                                "radical_opinions": compute_radical_opinions,
                                "community_no": community_no,
                                "compute_majority":compute_majority_opinions,
                                "echo_no":echo_no,
                                "spiral":compute_silent_spiral
                        })
batch_run.run_all()
run_data = batch_run.get_model_vars_dataframe()
print(run_data)