import random

def get_rand_expectation():
	mean = 5.5
	stdev = 5.5/5.5   # 99.73% chance the sample will fall in your desired range

	return float("%.2f" % random.gauss(mean, stdev))