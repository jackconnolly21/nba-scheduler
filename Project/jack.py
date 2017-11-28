import util
from scheduler import Scheduler, Team, Game
from datetime import date
import pickle
import copy
import random
from math import e

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

s = Scheduler(testSchedule=True)
schFile = open('pickles/nba16_17.txt', 'wb')
pickle.dump(s, schFile)


# for team in s.teams.values():
# 	sch = util.sortSchedule(team.schedule)
# 	for i in xrange(len(sch) - 1):
# 		if (sch[i].date - sch[i+1].date).days == 0 and sch[i].opponent.name == sch[i+1].opponent.name:
# 			print "Duplicate!", team.name, sch[i].date, sch[i].opponent.name




# t = s.teams["Miami Heat"]
# randomGame = random.choice(t.schedule)
# opp = randomGame.opponent
#
# for game in opp.schedule:
#     print game
# print "First Game:", randomGame

# temp = 100000
# while True:
# 	if temp <= 0:
# 		break
# 	else:
# 		deltaCost = 10000
# 		constant = -(deltaCost*0.5)/temp
# 		p = e**constant
# 		temp -= 0.5
# 		if temp % 100 == 0: print p


# pickleFile = open("obj.txt", "w")
# pickle.dump(s, pickleFile)
