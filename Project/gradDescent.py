import util
import pickle
from scheduler import Team, Scheduler, Game
from timeit import default_timer as timer

infinity = float('inf')

def gradientDescent(s):
    cost = s.costFn()
    i = 0

    while i < 100:

        info = s.swap()

        newCost = s.costFn()

        if newCost < cost:
            cost = newCost
            i = 0
        else:
            s.undoSwap(info)
            i += 1

    return cost

if __name__ == '__main__':
    bestCost = infinity
    for i in xrange(20):
        print i
        while True:
        	sc = Scheduler()
        	sc.randomStart()
        	if sc.isValidSchedule():
        		s = sc
        		break
        new = gradientDescent(s)
        if new < bestCost:
            print "Ending Cost:", new
            bestCost = new
            bestSch = s
    bestSchFile = open('best.txt', 'wb')
    pickle.dump(bestSch, bestSchFile)
