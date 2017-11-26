import pickle
import util
from scheduler import Scheduler, Game, Team

s = pickle.load(open('best.txt', 'rb'))
print "Total Distance:", s.totalDistanceAll()
print "Back To Backs:", util.totalBackToBacks(s.teams)
print "Total Triples:", s.totalTriples()

heat = s.teams["Miami Heat"]
sch = util.sortSchedule(heat.schedule)
for g in sch:
    print g
print "Heat Triples:", heat.triples()
