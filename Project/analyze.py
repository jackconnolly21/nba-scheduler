import pickle
import util
import sys
import os
from scheduler import Scheduler, Game, Team
from optparse import OptionParser
import numpy as np
import matplotlib.pyplot as plt

"""
    This python script is used to analyze a previously created pickle file

    It reads in a saved pickle file of a Scheduler instance, and calculates
    a variety of information about the schedule

    Use like:
        python analyze.py -f fileName

    Where the actual file opened is "pickles/" + fileName

    Can also pass in a list of files, which will all be analyzed separately and graphed together

"""

def analyzePickles(fileNameList):
    # Try to open the pickle file passed in
    for fileName in fileNameList:
        try:
            f = "pickles/" + fileName
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
        print "Standard Deviations:"
        print "     BTB:", s.getStandardDevs()[0]
        print "     Distance:", s.getStandardDevs()[1]

        # Find most and least back to backs
        most = 0
        least = 100
        for team in s.teams.values():
            most = max(most, team.backToBacks())
            least = min(least, team.backToBacks())
        print "Most Back to Backs:", most
        print "Least Back to Backs:", least

        try:
            plt.plot(s.trace, label=fileName)
        except AttributeError:
            print "This schedule doesn't have a trace."
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
    plt.show()

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
    analyzePickles(files)
