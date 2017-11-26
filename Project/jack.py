import util
from scheduler import Scheduler, Team, Game
from datetime import date
import pickle
import copy

i = 0
while True:
	sc = Scheduler()
	sc.randomStart()
	if sc.isValidSchedule():
		s = sc
		break
	i += 1

d = 0
for team in s.teams.values():
    s = util.sortSchedule(team.schedule)
    for i in xrange(len(s) - 1):
        g1 = s[i].date
        g2 = s[i+1].date
        if g1 == g2:
            d += 1
            print g1
print d

# for team in s.teams.values():
#     for game in team.schedule:
#         print game



# pickleFile = open("obj.txt", "w")
# pickle.dump(s, pickleFile)
