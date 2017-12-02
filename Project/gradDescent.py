import util
import pickle
import sys
from scheduler import Team, Scheduler, Game
from timeit import default_timer as timer
from optparse import OptionParser
from math import e, log10
import numpy as np
import matplotlib.pyplot as plt


infinity = float('inf')

"""
    Perform greedy gradientDescent on the schedule
"""
def gradientDescent(s, numIters=200):
    # Intiailize cost
    cost = s.costFn()
    # Track iterations and iterations without improvement (i)
    i = 0
    iterations = 0
    # store trace for plotting
    s.trace = []

    # Perform gradientDescent until numIters iterations doesn't produce a cost decrease
    while i < numIters:

        # Perform random swap (random game to new random date)
        info = s.swap()
        # Cost after swap
        newCost = s.costFn()
        # Check if newCost is better, reset i=0 if so
        if newCost < cost:
            cost = newCost
            i = 0
        else:
            s.undoSwap(info)
            i += 1
        iterations += 1
        s.trace.append(log10(cost))

    # Return the cost of the new solution
    print "Iterations:", iterations
    print "Back to Backs:", util.totalBackToBacks(s.teams)
    return cost

"""
    Perform simulatedAnnealing on the schedule, accepting
    worse solutions with probability exp(-deltaCost/temp)
"""
def simulatedAnnealing(s, times=50000, alpha=0.2):
    # Initialize cost and time
    cost = s.costFn()
    t = 0

    # Define a schedule function, takes in temperature
    def schedule(t):
        temp = times - alpha*t
        return temp

    iterations = 0
    # Run until temp <= 0
    # store trace for plotting
    s.trace = []
    while True:
        # Perform swap, update cost and temperature
        info = s.swap()
        newCost = s.costFn()
        temp = schedule(t)

        # If temp <= 0, return bestCost
        if temp <= 0:
            print "Iterations:", iterations
            print "Back to Backs:", util.totalBackToBacks(s.teams)
            return min(cost, newCost)
        # Otherwise accept if better
        # If worse, accept w/ prob = exp(-deltaCost/temp)
        else:
            deltaCost = newCost - cost
            constant = -(deltaCost*3)/temp

            if newCost < cost:
                cost = newCost
            elif util.flipCoin(e**constant):
                cost = newCost
            else:
                s.undoSwap(info)
            s.trace.append(log10(cost))
            t += 1
        iterations += 1


def readCommands(argv):
    # Create OptionParser
    parser = OptionParser()
    # Add some options for what we can pass in command line
    parser.add_option("-m", "--method", dest="method",
                  help="use METHOD to conduct local search (GD or SA)",
                  default="GD")
    parser.add_option("-n", "--numIters", dest="numIters",
                    help="specify the number of iterations to run for", type="int",
                    default=1000)
    parser.add_option("-t", "--numTimes", dest="numTimes",
                    help="number of times to run algorithm", type="int",
                    default=1)
    parser.add_option("-f", "--fileName", dest="fileName",
                    help="pickle FILE to run gradientDescent on", default="")
    (options, args) = parser.parse_args(argv)
    return options

if __name__ == '__main__':

    # Get the options and make variable with them
    options = readCommands(sys.argv[1:])
    method = options.method
    numIters = options.numIters
    numTimes = options.numTimes
    fileName = options.fileName

    bestCost = infinity
    # Run chosen method numTimes number of times
    for i in xrange(numTimes):
        # Get a valid initialization
        if fileName != "":
            s = pickle.load(open("pickles/" + fileName, 'rb'))
        else:
            while True:
            	sc = Scheduler()
            	sc.randomStart()
            	if sc.isValidSchedule():
            		s = sc
            		break
        # Run chosen method
        if method == 'SA':
            new = simulatedAnnealing(s, times=numIters)
        if method == 'GD':
            new = gradientDescent(s, numIters)


        print "Ending Cost:", new

        # Update bestCost and schedule if better
        if new < bestCost:
            bestCost = new
            bestSch = s

    print "Best Cost:", bestCost

    # Create a filename
    numbtb = util.totalBackToBacks(bestSch.teams)
    filename = 'pickles/' + str(numbtb) + method + '.txt'

    # Dump into a pickle file to analyze later
    bestSchFile = open(filename, 'wb')
    pickle.dump(bestSch, bestSchFile)

    plt.plot(bestSch.trace, label=method)
    plt.show()
