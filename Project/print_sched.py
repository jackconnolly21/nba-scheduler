import pickle
import util
import sys
import os
from scheduler import Scheduler, Game, Team
from optparse import OptionParser

def print_sched(fileName):
    # Try to open the pickle file passed in
    lst = []
    try:
        f = 'pickles/' + fileName
        s = pickle.load(open(f, 'rb'))
    except IOError:
        print "Could not load file '" + fileName
        return 1
    for team in s.teams:
    	for game in s.teams[team].schedule:
    		lst.append((game.date, team, game.opponent.name))
    		lst.sort()
    btbs = util.totalBackToBacks(s.teams)
    fileout = str(btbs) + '.txt'
    fout = open(fileout, 'w')
    for game in lst:
        info = [game[0], game[1], game[2]]
        gameString = ",".join(str(i) for i in info) + "\n"
    	fout.write(gameString)

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
        print_sched(f)
