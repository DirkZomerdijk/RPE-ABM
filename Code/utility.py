import numpy as np
from globals import *
import random
import networkx as nx
from scipy.stats import norm
import matplotlib.pyplot as plt
from operator import itemgetter

def get_preference_list(N):
    preference_list = []
    for i in range(N):
        preference_list.append(set_trust())

    return preference_list

def mean_neighbor_preference(neighbors):
    neighbor_preference = []
    for neighbor in neighbors:
        neighbor_preference.append(neighbor.preference)
    new_preference = sum(neighbor_preference) / float(len(neighbor_preference))
    return new_preference

def set_rand_unifrom_preference():
    return np.random.uniform(0,1)

def get_rand_similarity(similarity_treshold):
    lower_treshold = 0.0
    upper_treshold = similarity_treshold*2
    sample = 10
    while sample > upper_treshold or sample < lower_treshold:
        sample = random.gauss(similarity_treshold, np.std([lower_treshold, similarity_treshold, upper_treshold]))
        
    return sample

def set_trust():
    return random.uniform(0,10)

# def set_opinion(model):
#     return list(range(0,))
