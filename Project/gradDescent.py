import util
import pickle
from scheduler import Team, Scheduler, Game
from timeit import default_timer as timer
from math import e

infinity = float('inf')

"""
    I think the swap or undoSwap methods aren't working
    The number of games in each schedule is changing from 82 somehow
"""

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

def stochasticGradDesc(s, times=10000, alpha=0.8):
    cost = s.costFn()
    t = 0

    def schedule(t):
        temp = times - alpha*t
        return temp

    while True:

        info = s.swap()

        newCost = s.costFn()

        temp = schedule(t)

        if temp <= 0:
            return min(cost, newCost)
        else:
            deltaCost = newCost - cost
            constant = -deltaCost/temp

            if newCost < cost:
                cost = newCost
            elif util.flipCoin(e**constant):
                cost = newCost
            else:
                s.undoSwap(info)
            t += 1

if __name__ == '__main__':
    bestCost = infinity
    for i in xrange(3):
        print i
        while True:
        	sc = Scheduler()
        	sc.randomStart()
        	if sc.isValidSchedule():
        		s = sc
        		break
        new = stochasticGradDesc(s)
        # new = gradientDescent(s)
        print "Ending Cost:", new
        if new < bestCost:
            # print "Ending Cost:", new
            bestCost = new
            bestSch = s
    print "Best Cost:", bestCost
    bestSchFile = open('best.txt', 'wb')
    pickle.dump(bestSch, bestSchFile)
