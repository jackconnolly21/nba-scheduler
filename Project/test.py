import util
from scheduler import Scheduler, Team, Game
import numpy as np
import matplotlib.pyplot as plt


s1 = Scheduler()
s1.randomStart()
blazers = s1.teams["Portland Trail Blazers"]
print s1.numHomeGames(blazers)
print len(blazers.schedule)
cavs = s1.teams["Cleveland Cavaliers"]
print s1.numHomeGames(cavs)
print len(cavs.schedule)
dubs = s1.teams["Golden State Warriors"]
print s1.numHomeGames(dubs)
print len(dubs.schedule)
jazz = s1.teams["Utah Jazz"]
print s1.numHomeGames(jazz)
print len(jazz.schedule)
celts = s1.teams["Boston Celtics"]
print s1.numHomeGames(celts)
print len(celts.schedule)
knicks = s1.teams["New York Knicks"]
print s1.numHomeGames(knicks)
print len(knicks.schedule)
nets = s1.teams["Brooklyn Nets"]
print s1.numHomeGames(nets)
print len(nets.schedule)

print

print 

i = 0
while True:
	sched = Scheduler()
	sched.randomStart()
	if sched.isValidSchedule():
		goodSched = sched
		break
	i += 1
print i

for team in goodSched.teams.values():
	if len(team.schedule) != 82 or s1.numHomeGames(team) != 41:
		print team, s1.numHomeGames(team), len(team.schedule)

x = np.linspace(0, 2, 100)

plt.plot(x, x, label='linear')
plt.plot(x, x**2, label='quadratic')
plt.plot(x, x**3, label='cubic')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()