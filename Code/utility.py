'''
Utility functions for the model
'''

import numpy as np
import random
import networkx as nx
from scipy.stats import norm
import matplotlib.pyplot as plt
from operator import itemgetter



def set_rand_unifrom_preference():
    '''
    Returns a random preference between [0, 1]
    '''
    return np.random.uniform(0,1)

def get_rand_similarity(similarity_treshold):
    '''
    Returns a sample from gaussian distribution with mean = similarity_treshold
    '''
    lower_treshold = 0.0
    upper_treshold = similarity_treshold*2
    sample = 10
    while sample > upper_treshold or sample < lower_treshold:
        sample = random.gauss(similarity_treshold, np.std([lower_treshold, similarity_treshold, upper_treshold]))
        
    return sample
