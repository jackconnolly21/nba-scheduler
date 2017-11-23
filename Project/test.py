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
