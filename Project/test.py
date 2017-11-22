import util
from scheduler import Scheduler, Team, Game

s = Scheduler(testSchedule=True)
team = s.teams["Portland Trail Blazers"]
sch = team.schedule
print "num homeGames", s.numHomeGames(team)
print len(team.teamCalendar)
