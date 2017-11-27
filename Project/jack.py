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
# t = s.teams["Miami Heat"]
# randomGame = random.choice(t.schedule)
# opp = randomGame.opponent
#
# for game in opp.schedule:
#     print game
# print "First Game:", randomGame

temp = 10000
while True:
	if temp <= 0:
		break
	else:
		deltaCost = 2000
		constant = -deltaCost/temp
		p = e**constant
		temp -= 0.8
		print p


# pickleFile = open("obj.txt", "w")
# pickle.dump(s, pickleFile)
