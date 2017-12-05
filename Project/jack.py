import util
from scheduler import Scheduler, Team, Game
from datetime import date
import pickle
import copy
import random
from math import e, log
import os
import numpy as np
import matplotlib.pyplot as plt

# i = 0
# while True:
# 	sc = Scheduler()
# 	sc.randomStart()
# 	if sc.isValidSchedule():
# 		s = sc
# 		break
# 	i += 1
#
# for i in xrange(1000):
# 	info = s.swap()

# s = Scheduler(testSchedule=True)
# schFile = open('pickles/nba16_17.txt', 'wb')
# pickle.dump(s, schFile)


# print os.getcwd()



# for team in s.teams.values():
# 	sch = util.sortSchedule(team.schedule)
# 	for i in xrange(len(sch) - 1):
# 		if (sch[i].date - sch[i+1].date).days == 0 and sch[i].opponent.name == sch[i+1].opponent.name:
# 			print "Duplicate!", team.name, sch[i].date, sch[i].opponent.name
#
# sched = pickle.load(open('pickles/321GD.txt', 'rb'))
# stds = sched.getStandardDevs()
# print stds



# t = s.teams["Miami Heat"]
# randomGame = random.choice(t.schedule)
# opp = randomGame.opponent
#
# for game in opp.schedule:
#     print game
# print "First Game:", randomGame

temp = 10000
trace = []
while True:
	if temp <= 0:
		break
	else:
		deltaCost = 50000
		constant = -((deltaCost))/(temp)
		p = 100*(e**constant)
		temp -= 0.2
		trace.append(p)
		print p
plt.plot(trace)
plt.show()


# pickleFile = open("obj.txt", "w")
# pickle.dump(s, pickleFile)
