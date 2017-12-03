import pickle
import util
import sys
import os
from scheduler import Scheduler, Game, Team
from optparse import OptionParser
import numpy as np
import matplotlib.pyplot as plt

def analyzePickle(fileName):
    # Try to open the pickle file passed in
    try:
        f = 'pickles/' + fileName
        s = pickle.load(open(f, 'rb'))
    except IOError:
        print "Could not load file '" + fileName
        return 1

    print
    print "File:", fileName
    print "Cost:", s.costFn()

    # Just in case something messes up, print if any team
    # has something other than 82 games in their schedule
    for team in s.teams.values():
        if len(team.schedule) != 82: print len(team.schedule)

    # Print some info that the cost function considers
    print "Total Distance:", s.totalDistanceAll()
    print "Total Back To Backs:", util.totalBackToBacks(s.teams)
    print "Triples:", s.totalTriples()

    # Find most and least back to backs
    most = 0
    least = 100
    for team in s.teams.values():
        most = max(most, team.backToBacks())
        least = min(least, team.backToBacks())
    print "Most Back to Backs:", most
    print "Least Back to Backs:", least

    try:
        plt.plot(s.trace)
        plt.show()
    except AttributeError:
        print "This schedule doesn't have a trace."

def readCommands(argv):
    # Allow fileNames to be passed in command line
    parser = OptionParser()
    parser.add_option("-f", "--files", dest="fileNames",
                  help="write report from FILES (comma separated list)", metavar="FILES")
    (options, args) = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    # Read command line
    options = readCommands(sys.argv[1:])
    files = []

    # Allow options of "all" files being passed in
    if options.fileNames == 'all':
        for f in os.listdir(os.getcwd() + '/pickles'):
            if f.endswith('.txt'):
                files.append(f)
    elif options.fileNames == None:
        print "Use -f option to pass in pickle file(s) to analyze."
    else:
        files = options.fileNames.split(',')

    # Analyze every file passed in
    for f in files:
        analyzePickle(f)
