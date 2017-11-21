import util
from scheduler import Scheduler, Team, Game

s = Scheduler()
sch = s.teams["Boston Celtics"].schedule
print "Total btbs:", util.totalBackToBacks(s.teams)
