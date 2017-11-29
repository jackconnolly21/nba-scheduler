import pickle
import util
import sys
from scheduler import Scheduler, Game, Team
from optparse import OptionParser


def analyzePickle(fileName):
    try:
        f = 'pickles/' + fileName + '.txt'
        s = pickle.load(open(f, 'rb'))
    except IOError:
        print "Could not load file '" + fileName + ".txt'"
        return 1

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
    parser.add_option("-f", "--file", dest="fileName",
                  help="write report from FILE", metavar="FILE")
    (options, args) = parser.parse_args(argv)
    return options

if __name__ == '__main__':
    options = readCommands(sys.argv[1:])
    analyzePickle(options.fileName)
