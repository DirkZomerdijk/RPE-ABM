from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random
from itertools import groupby
import operator

class agent(Agent):
    '''
    An agent that talks; select his neighbors based on similarity and trust, and updates opinion and preference accordingly.
    '''

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.opinion = random.randint(0,self.model.opinions-1)
        self.preference = set_rand_unifrom_preference()

    def step(self):
        '''
        A model step. Agent talks to other agents
        ''' 
        self.talk()

    def talk(self):
        '''
        Agent sees neighbors. Chooses neighbors to talk with.
        Start talk with seleced neighbors and form opinion.
        '''
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)
        selected_neighbors = self.choose_neighbors(neighbors)
        self.form_opinion(selected_neighbors)

    def choose_neighbors(self, neighbors):
        '''
        Choose neighbors to talk with. 
        If opinion and preference is similar: selection based on similarity.
        Else selection on trust.
        If neighbors are similar only talk with these. Else talk based on trust.
        '''
        selected_neighbors = []
        similar_neighbors = []
        for neighbor in neighbors:
            trust = self.model.G.edges[self.pos,neighbor.pos]['trust']
            if((neighbor.opinion == self.opinion) and (abs(neighbor.preference - self.preference) < get_rand_similarity(self.model.similarity_treshold))):
                similar_neighbors.append(neighbor)
                self.update_trust(neighbor.pos)
            else:
                if(trust > np.random.uniform(0,1)):
                    selected_neighbors.append(neighbor)
                    self.update_trust(neighbor.pos)

        if(len(similar_neighbors) != 0):
            return similar_neighbors
        else:
            return selected_neighbors

    def form_opinion(self, neighbors):

        '''
        An agent forming opinion. Calculate the probability to change opinion. 
        If probability is high enough select new opinion.
        '''        

        # Get neighbor preferences
        neighbor_preferences = [neighbor.preference for neighbor in neighbors]

        # Initialize array containing preferences for each opinion
        neighbor_opinion_preferences = [[] for i in range(self.model.opinions)]

        # Initialize array containing probabilities
        probability_rates = []

        # All opinions
        opinions = list(range(self.model.opinions))

        # Append all neighbors preferences based on opinion
        for neighbor in neighbors:
            for opinion in range(self.model.opinions):
                if neighbor.opinion == opinion:
                    neighbor_opinion_preferences[opinion].append(neighbor.preference)

        # Calculate the probability of being chosen for each opinion
        for opinion in range(self.model.opinions):
            if len(neighbor_opinion_preferences[opinion])!=0:
                probability_rates.append(sum(neighbor_opinion_preferences[opinion])/sum(neighbor_preferences))
            else:
                probability_rates.append(0)
        
        # select opinion with highest probability
        max_opinion_idx = probability_rates.index(max(probability_rates))            

        # Only switch opinion if the probability for other opinions is higher than the preference for agents own opinion.
        if (probability_rates[max_opinion_idx]  < (self.preference*2)/self.model.opinions) and self.opinion != max_opinion_idx:
            return self.select_opinion(neighbor_opinion_preferences[self.opinion], switch_opinion = False, new_opinion = self.opinion)

        # If so: Role dice and select new opinion
        else:
            dice = random.uniform(0,1)
            for idx, prob in enumerate(probability_rates):
                dice = dice - prob
                if dice <= 0:
                    return self.select_opinion(neighbor_opinion_preferences[idx], switch_opinion = True, new_opinion = idx)

    def select_opinion(self, preferences, switch_opinion, new_opinion):
        '''
        An agent opinion selection. If agent switches opinion, switch preference.
        '''

        # if agent switches opinion; switch preference
        if switch_opinion:
            self.preference = 1 - self.preference
            
        self.opinion = new_opinion
        self.update_preference(preferences)

    def update_preference(self, neighbors_preference):
        '''
        Update agents preference using the neighbors with shared opinions preferences
        '''
        self.preference = self.preference + (self.model.social_influence * sum([(neighbor - self.preference) for neighbor in neighbors_preference]))

    def update_trust(self, neighbor_position):
        '''
        Update trust between agents by updating edge strenghts
        '''
        self.model.update_edge(self.pos, neighbor_position)


