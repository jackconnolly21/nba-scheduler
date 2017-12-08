import util
from scheduler import Scheduler, Team, Game
import numpy as np
import matplotlib.pyplot as plt
import pickle

hc = pickle.load(open("pickles/274HC.txt", "rb"))
sa = pickle.load(open("pickles/271SA.txt", 'rb'))

hctrace = hc.trace
satrace = sa.trace

plt.plot(hctrace, label="Hill Climbing")
plt.plot(satrace, label="Simulated Annealing")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)
plt.show()


# s1 = Scheduler()
# s1.randomStart()
# blazers = s1.teams["Portland Trail Blazers"]
# print s1.numHomeGames(blazers)
# print len(blazers.schedule)
# cavs = s1.teams["Cleveland Cavaliers"]
# print s1.numHomeGames(cavs)
# print len(cavs.schedule)
# dubs = s1.teams["Golden State Warriors"]
# print s1.numHomeGames(dubs)
# print len(dubs.schedule)
# jazz = s1.teams["Utah Jazz"]
# print s1.numHomeGames(jazz)
# print len(jazz.schedule)
# celts = s1.teams["Boston Celtics"]
# print s1.numHomeGames(celts)
# print len(celts.schedule)
# knicks = s1.teams["New York Knicks"]
# print s1.numHomeGames(knicks)
# print len(knicks.schedule)
# nets = s1.teams["Brooklyn Nets"]
# print s1.numHomeGames(nets)
# print len(nets.schedule)
#
#
# i = 0
# while True:
# 	sched = Scheduler()
# 	sched.randomStart()
# 	if sched.isValidSchedule():
# 		goodSched = sched
# 		break
# 	i += 1
# print i
#
#
#
#
# for team in goodSched.teams.values():
# 	if len(team.schedule) != 82 or s1.numHomeGames(team) != 41:
# 		print team, s1.numHomeGames(team), len(team.schedule)

# for team1 in s1.teams:
# 	for team2 in s1.teams:
# 		dist = util.latLongDistance(s1.teams[team1].location, s1.teams[team2].location)
# 		print team1, team2, dist
