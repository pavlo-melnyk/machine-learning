'''
An implementation of the Optimistic Initial Values algorithm - 
a solution to the explore-exploit dilemma.


'''

import numpy as np 
import matplotlib.pyplot as plt

from epsilon_greedy import run_experiment as run_epsilon_greedy

class Bandit:
	def __init__(self, m, optimistic_value):
		self.m = m # the true mean - 
				   # it's like we are the manufacturers and we set it!
		self.mean = optimistic_value # our optimisticly high estimates of the Bandit's mean
		self.N = 1 # number of experiments

	def pull(self):
		# every Bandit's reward will be a Gaussian with unit-variance
		# (i.e. the Standard Normal Distribution):
		return np.random.randn() + self.m 

	def update(self, x):
		# update the running mean - the win rate:
		self.N += 1
		self.mean = (1 - 1.0/self.N) * self.mean + 1.0/self.N * x


def run_optimistic_init_value(m1, m2, m3, N, optimistic_value=10):
	# create a few bandits and set their true mean:
	bandits = [Bandit(m1, optimistic_value), Bandit(m2, optimistic_value), Bandit(m3, optimistic_value)]

	# create a storage for data we're to collect:
	data = np.empty(N)

	# optimistic_value:
	for i in range(N):
		# play the bandit with the maximum winning rate so far:
		# the more we play, the less the running means will be -
		# settled around their true values
		# (remember, the winning rate is a bandit's running mean of rewards)
		bandit = bandits[ np.argmax([bandit.mean for bandit in bandits]) ]	
		# play the selected bandit = pull the arm and get a reward:
		x = bandit.pull()
		# update the bandit's stats - number of times it was played and the win rate:
		bandit.update(x)

		# collect data - all the rewards we received:
		data[i] = x

	# calculate the cumulative average after every play:
	# https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.cumsum.html#numpy-cumsum
	# e.g. data = [0.5, 0.11, 0.98], then 
	# cum_sum(data) = [0.5, 0.5+0.11, 0.5+0.11+0.98];
	# to get the cum_avg, we simply divide every entry of cum_sum 
	# by the number of the plays done so far, i.e.
	# cum_avg = [0.5/1, (0.5+0.11)/2, (0.5+0.11+0.98)/3]:
	cumulative_average = np.cumsum(data) / (np.arange(N) + 1) # of shape (N, )

	# plot the moving averages:
	plt.plot(cumulative_average)
	plt.plot(np.ones(N)*m1)
	plt.plot(np.ones(N)*m2)
	plt.plot(np.ones(N)*m3)
	plt.xscale('log')
	plt.show()

	for bandit in bandits:
		print(bandit.mean)

	return cumulative_average


if __name__ == '__main__':
	# optimistic initial value for every bandit:
	optimistic_value = 10
	# the true means of every bandit:
	m1, m2, m3 = 1.0, 2.0, 3.0
	# number of plays:
	N = 100000

	# make 3 experiments for different :
	ex_1 = run_optimistic_init_value(m1, m2, m3, N, optimistic_value)
	ex_2 = run_epsilon_greedy(m1, m2, m3, 0.1, N)

	# log-scale plot:
	plt.plot(ex_1, label='optimistic_value = 10')
	plt.plot(ex_2, label='eps = 0.1')
	plt.legend()
	plt.xscale('log')
	plt.ylabel('average reward')
	plt.xlabel('plays')
	plt.title('Cumulative Averages - Log-Scale Plot')
	plt.show()

	# linear plot:
	plt.plot(ex_1, label='optimistic_value = 10')
	plt.plot(ex_2, label='eps = 0.1')
	plt.legend()
	plt.ylabel('average reward')
	plt.xlabel('plays')
	plt.title('Cumulative Averages - Linear Plot')
	plt.show()







