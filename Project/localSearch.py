import util
import sys
import pickle

from math import e
from scheduler import Team, Scheduler, Game
from timeit import default_timer as timer
from optparse import OptionParser


infinity = float('inf')

# in an earlier version of our project we incorrectly called our hill climbing algorithm
# gradient descent, so GD.txt pickle files were created using the hill climbing algorithm

"""
    Perform greedy hillClimbing on the schedule
"""
def hillClimbing(s, numIters=200, numSwaps=1):

    # Remove all triples from the schedule (3 games in a row)
    rmTrips = s.removeTriples()
    print "Removed Triples: " + str(rmTrips[0]) + " iterations."

    # Intiailize cost
    cost = s.costFn()

    # Track iterations and iterations without improvement (i)
    i = 0
    iterations = 0
    successes = 0

    # store trace for plotting
    s.trace = []

    # Perform hillClimbing until numIters iterations doesn't produce a cost decrease
    while iterations < numIters:

        # Perform random swap (random game to new random date)
        infos = s.multiSwap(numSwaps)

        # Cost after swap
        newCost = s.costFn()

        # Check if newCost is better, reset i=0 if so
        if newCost < cost:
            cost = newCost
            i = 0
            successes += 1
        else:
            s.undoMultiSwap(infos)
            i += 1

        iterations += 1
        if iterations % 100000 == 0:
            print iterations, cost

        # Add cost to trace to track progress
        s.trace.append(cost)

    # Print some useful information
    print "Iterations:", iterations
    print "Back to Backs:", util.totalBackToBacks(s.teams)
    print "Successes Percentage:", successes/float(iterations)
    return cost

"""
    Perform simulatedAnnealing on the schedule, accepting
    worse solutions with probability exp(-deltaCost/temp)
"""
def simulatedAnnealing(s, times=50000, alpha=0.2):

    # Remove triples from the schedule
    rmTrips = s.removeTriples()
    print "Removed Triples: " + str(rmTrips[0]) + " iterations."

    # Initialize cost and time
    cost = s.costFn()
    t = 0
    alpha1 = 5000./float(times)
    iterations = 0

    # Define a schedule function, takes in temperature
    def schedule(t):
        temp = 5000.- alpha1*t
        return temp


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
            constant = -(deltaCost)/(temp**2)
            if newCost < cost:
                cost = newCost
            elif util.flipCoin(e**constant):
                cost = newCost
            else:
                s.undoSwap(info)
            s.trace.append(cost)
            t += 1

        # Track progress
        iterations += 1
        if iterations % 100000 == 0:
            print iterations, cost

# Make testing easier --> gives us options so we don't have to change code
def readCommands(argv):
    # Create OptionParser
    parser = OptionParser()
    # Add some options for what we can pass in command line
    parser.add_option("-m", "--method", dest="method",
                  help="use METHOD to conduct local search (HC or SA)",
                  default="HC")
    parser.add_option("-n", "--numIters", dest="numIters",
                    help="specify the number of iterations to run for", type="int",
                    default=1000)
    parser.add_option("-t", "--numTimes", dest="numTimes",
                    help="number of times to run algorithm", type="int",
                    default=1)
    parser.add_option("-f", "--fileName", dest="fileName",
                    help="pickle FILE to run hillClimbing on", default="")
    parser.add_option("-s", "--numSwaps", dest="numSwaps", type="int",
                    help="numSwaps per iteration, usually just 1", default=1)
    (options, args) = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    # Time the method
    start = timer()

    # Get the options and make variables with them
    options = readCommands(sys.argv[1:])
    method = options.method
    numIters = options.numIters
    numTimes = options.numTimes
    fileName = options.fileName
    numSwaps = options.numSwaps

    bestCost = infinity
    # Run chosen method numTimes number of times
    for i in xrange(numTimes):

        # Get a valid initialization
        if fileName != "":
            try:
                s = pickle.load(open("pickles/" + fileName, 'rb'))
            except IOError:
                print "Could not open file: " + fileName
        else:
        	s = Scheduler()
        	s.randomStart()

        # Run chosen method
        if method == 'SA':
            new = simulatedAnnealing(s, times=numIters)
            end = timer()
        elif method == 'HC':
            new = hillClimbing(s, numIters, numSwaps)
            end = timer()


        print "Ending Cost:", new
        print

        # Update bestCost and schedule if better
        if new < bestCost:
            bestCost = new
            bestSch = s

    print "Best Cost:", bestCost
    print "Total time:", end - start

    # Create a filename
    numbtb = util.totalBackToBacks(bestSch.teams)
    filename = 'pickles/' + str(numbtb) + method + '.txt'

    # Dump into a pickle file to analyze later
    bestSchFile = open(filename, 'wb')
    pickle.dump(bestSch, bestSchFile)
