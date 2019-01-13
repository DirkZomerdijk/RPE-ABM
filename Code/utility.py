import random
def get_expectation_list(N):
	expectation_list = []
	for i in range(N):
		expectation_list.append(get_rand_expectation())

	return expectation_list


def get_rand_expectation():
    mean = 5.5
    stdev = 5.5/5.5   # 99.73% chance the sample will fall in your desired range

    return float("%.2f" % random.gauss(mean, stdev))