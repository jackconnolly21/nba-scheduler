import util
from scheduler import Scheduler, Team, Game
from datetime import date
import pickle
import copy
import random

i = 0
while True:
	sc = Scheduler()
	sc.randomStart()
	if sc.isValidSchedule():
		s = sc
		break
	i += 1

t = s.teams["Miami Heat"]
randomGame = random.choice(t.schedule)
opp = randomGame.opponent

for game in opp.schedule:
    print game
print "First Game:", randomGame


# pickleFile = open("obj.txt", "w")
# pickle.dump(s, pickleFile)
