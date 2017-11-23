import util
from scheduler import Scheduler, Team, Game

s = Scheduler(testSchedule=True)
team = s.teams["Portland Trail Blazers"]
sch = team.schedule
print "num homeGames", s.numHomeGames(team)
print len(team.teamCalendar)

s1 = Scheduler()
s1.randomStart()
blazers = s1.teams["Portland Trail Blazers"]
print s1.numHomeGames(blazers)
print len(blazers.schedule)

