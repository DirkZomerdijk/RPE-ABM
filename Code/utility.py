
import random
def get_expectation_list(N):
    expectation_list = []
    for i in range(N):
        expectation_list.append(get_rand_expectation())

    return expectation_list


def get_rand_expectation():
    mean = 5.5
    stdev = 5.5/5.5   # 99.73% chance the sample will fall in your desired range

<<<<<<< HEAD
    return float("%.2f" % random.gauss(mean, stdev))
=======
    return float("%.2f" % random.gauss(mean, stdev))

def get_type():
    return random.choice(type_list)

def set_reputation():
    return random.uniform(0,5)

def get_payoff_matrix(reputationA,reputationB,convincing_powerA,convincing_powerB):
    # return np.array([[ [reputationA, convincing_powerA], [reputationB,convincing_powerB]],
 #             [[convincing_powerA, reputationB], [convincing_powerA, convincing_powerB]] ] )
    return np.array([[reputationA, convincing_powerA], [reputationB,convincing_powerB]])

>>>>>>> 479059b9b13cde3ae3645a8217bd82b53f138ece
