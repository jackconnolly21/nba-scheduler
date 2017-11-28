import pickle
import util
from scheduler import Scheduler, Game, Team

s = pickle.load(open('pickles/best.txt', 'rb'))
for team in s.teams.values():
    if len(team.schedule) != 82: print len(team.schedule)

print "Total Distance:", s.totalDistanceAll()
print "Total Back To Backs:", util.totalBackToBacks(s.teams)
print "Triples:", s.totalTriples()

most = 0
least = 100
for team in s.teams.values():
    most = max(most, team.backToBacks())
    least = min(least, team.backToBacks())
print "Most Back to Backs:", most
print "Least Back to Backs:", least
