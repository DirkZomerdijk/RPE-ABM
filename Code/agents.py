from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random

class node():

    def get_rand_expectation():
        mean = 5.5
        stdev = 5.5/5.5   # 99.73% chance the sample will fall in your desired range

        return float("%.2f" % random.gauss(mean, stdev))