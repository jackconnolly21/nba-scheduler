import pickle
import util
from scheduler import Scheduler, Game, Team

s = pickle.load(open('best.txt', 'rb'))
for team in s.teams.values():
    print len(team.schedule)
