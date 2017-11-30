import pickle
import util
import sys
import os
from scheduler import Scheduler, Game, Team
from optparse import OptionParser

def analyzePickle(fileName):
    try:
        f = 'pickles/' + fileName
        s = pickle.load(open(f, 'rb'))
    except IOError:
        print "Could not load file '" + fileName
        return 1

    print
    print "File:", fileName

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

def readCommands(argv):
    parser = OptionParser()
    parser.add_option("-f", "--files", dest="fileNames",
                  help="write report from FILES (comma separated list)", metavar="FILES")
    (options, args) = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    options = readCommands(sys.argv[1:])
    files = []
    if options.fileNames == 'all':
        for f in os.listdir(os.getcwd() + '/pickles'):
            if f.endswith('.txt'):
                files.append(f)
    else:
        files = options.fileNames.split(',')

    for f in files:
        analyzePickle(f)
