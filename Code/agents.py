from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random
from globals import *
from itertools import groupby
import operator

class agent(Agent):
    '''
    A sheep that walks around, reproduces (asexually) and gets eaten.
    The init is the same as the RandomWalker.
    '''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.opinion = random.randint(0,self.model.opinions-1)
        self.preference = set_rand_unifrom_preference()


    def select_opinion(self, preferences, switch_opinion, new_opinion):
        """ Adapt preference score and opinion to A"""

        if switch_opinion:
            self.preference = 1 - self.preference

        self.opinion = new_opinion
        self.update_preference(preferences)

    def form_opinion(self, neighbors):

        """ Function to determine if opninion needs to be adapted based on neighbors""" 
        neighbor_preferences = [neighbor.preference for neighbor in neighbors]
        neighbor_opinion_preferences = [[] for i in range(self.model.opinions)]
        probability_rates = []
        opinions = list(range(self.model.opinions))


        # get_attr = operator.attrgetter('opinion')
        # neighbor_opinion_preferences = [[i.preference for i in list(g)] for k, g in groupby(sorted(neighbors, key=get_attr), get_attr)]
        
        for neighbor in neighbors:
            for opinion in range(self.model.opinions):
                if neighbor.opinion == opinion:
                    neighbor_opinion_preferences[opinion].append(neighbor.preference)

        for opinion in range(self.model.opinions):

            if len(neighbor_opinion_preferences[opinion])!=0:
                probability_rates.append(sum(neighbor_opinion_preferences[opinion])/sum(neighbor_preferences))
            else:
                probability_rates.append(0)
        
        max_opinion_idx = probability_rates.index(max(probability_rates))            

        if (probability_rates[max_opinion_idx]  < (self.preference*2)/self.model.opinions) and self.opinion != max_opinion_idx:
            return self.select_opinion(neighbor_opinion_preferences[self.opinion], switch_opinion = False, new_opinion = self.opinion)
        else:
            dice = random.uniform(0,1)
            for idx, prob in enumerate(probability_rates):
                dice = dice - prob
                if dice <= 0:
                    return self.select_opinion(neighbor_opinion_preferences[idx], switch_opinion = True, new_opinion = idx)

    def choose_neighbors(self, neighbors):
        """ Choose whitch neighbors to talk with based on trust"""
        selected_neighbors = []
        similar_neighbors = []
        for neighbor in neighbors:

            trust = self.model.G.edges[self.pos,neighbor.pos]['trust']

            if((neighbor.opinion == self.opinion) and (abs(neighbor.preference - self.preference) < get_rand_similarity(self.model.similarity_treshold))):
                similar_neighbors.append(neighbor)
                self.update_trust(neighbor.pos)
            else:
                # print('dissimilar')
                # print('different opinion')
                if(trust > np.random.uniform(0,1)):
                    selected_neighbors.append(neighbor)
                    self.update_trust(neighbor.pos)

        if(len(similar_neighbors) != 0):
            return similar_neighbors
        else:
            return selected_neighbors

    def update_trust(self, neighbor_position):
        self.model.update_edge(self.pos, neighbor_position)

    def update_preference(self, neighbors_preference):
        self.preference = self.preference + (self.model.social_influence * sum([(neighbor - self.preference) for neighbor in neighbors_preference]))

    def talk(self):
        '''
        Agent sees neighbors. Select neighbors to talk with (based on edge strenght). Increase connection strength if shared opinion. 
        Start Discussion, chance opinion according to probabilitiy function
        '''
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)
        selected_neighbors = self.choose_neighbors(neighbors)
        self.form_opinion(selected_neighbors)

    def step(self):
        self.talk()
