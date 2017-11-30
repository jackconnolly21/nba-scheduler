import util
import pickle
import sys
from scheduler import Team, Scheduler, Game
from timeit import default_timer as timer
from optparse import OptionParser
from math import e

infinity = float('inf')

"""
    Perform greedy gradientDescent on the schedule
"""
def gradientDescent(s, numIters=200):
    cost = s.costFn()
    i = 0
    iterations = 0

    while i < numIters:

        info = s.swap()

        newCost = s.costFn()

        if newCost < cost:
            cost = newCost
            i = 0
        else:
            s.undoSwap(info)
            i += 1
        iterations += 1

    print "Iterations:", iterations
    return cost

"""
    Perform simulatedAnnealing on the schedule, accepting
    worse solutions with probability exp(-deltaCost/temp)
"""
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
            constant = -(deltaCost*0.8)/temp

            if newCost < cost:
                cost = newCost
            elif util.flipCoin(e**constant):
                cost = newCost
            else:
                s.undoSwap(info)
            t += 1

def readCommands(argv):

    parser = OptionParser()
    parser.add_option("-m", "--method", dest="method",
                  help="use METHOD to conduct local search (GD or SA)",
                  default="GD")
    parser.add_option("-n", "--numIters", dest="numIters",
                    help="specify the number of iterations to run for", type="int",
                    default=1000)
    parser.add_option("-t", "--numTimes", dest="numTimes",
                    help="number of times to run algorithm", type="int",
                    default=1)
    (options, args) = parser.parse_args(argv)
    return options

if __name__ == '__main__':

    options = readCommands(sys.argv[1:])
    method = options.method
    numIters = options.numIters
    numTimes = options.numTimes

    bestCost = infinity
    for i in xrange(numTimes):
        while True:
        	sc = Scheduler()
        	sc.randomStart()
        	if sc.isValidSchedule():
        		s = sc
        		break
        if method == 'SA':
            new = stochasticGradDesc(s, times=numIters)
        if method == 'GD':
            new = gradientDescent(s, numIters)
        print "Ending Cost:", new
        print
        if new < bestCost:
            bestCost = new
            bestSch = s

    print "Best Cost:", bestCost

    numbtb = util.totalBackToBacks(bestSch.teams)
    filename = 'pickles/' + str(numbtb) + method + '.txt'

    bestSchFile = open(filename, 'wb')
    pickle.dump(bestSch, bestSchFile)
