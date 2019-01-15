
import random
import numpy as np
import nashpy as nash

type_list = ['convincing', 'normal', 'unconvincing']
type_dict = {'convincing':5, 'normal':3, 'unconvincing':1}

def get_expectation_list(N):
    expectation_list = []
    for i in range(N):
        expectation_list.append(set_rand_expectation())

    return expectation_list


def set_rand_expectation():
    mean = 5.5
    stdev = 5.5/5.5   # 99.73% chance the sample will fall in your desired range

    return float("%.2f" % random.gauss(mean, stdev))

def set_type():
    return random.choice(type_list)

def set_reputation():
    return random.uniform(0,5)

def get_payoff_matrix(reputationA,reputationB,convincing_powerA,convincing_powerB):
    # return np.array([[ [reputationA, convincing_powerA], [reputationB,convincing_powerB]],
 #             [[convincing_powerA, reputationB], [convincing_powerA, convincing_powerB]] ] )
    return np.array([[reputationA, convincing_powerA], [reputationB,convincing_powerB]])

def play_game(payoff_matrix):
    game = nash.Game(payoff_matrix)
    for eq in game.support_enumeration():
        choiceA = np.where(eq[0] == max(eq[0]))[0]
        choiceB = np.where(eq[1] == max(eq[1]))[0]

        print(payoff_matrix[choiceA[0]][choiceB][0])
        break
