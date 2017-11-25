import util
from scheduler import Scheduler, Team, Game

s = Scheduler()
s.randomStart()


print s.totalDistanceAll(s.teams)
print util.totalBackToBacks(s.teams)
