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
    t = team.duplicates()
    print t
    d += t
print d

# pickleFile = open("obj.txt", "w")
# pickle.dump(s, pickleFile)
