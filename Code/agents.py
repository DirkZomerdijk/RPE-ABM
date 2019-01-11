from mesa import Agent
from utility import *
import matplotlib.pyplot as plt

class Person():

    def __init__(self, node_id):
        self.node_id = node_id
        self.expectation = get_rand_expectation()


