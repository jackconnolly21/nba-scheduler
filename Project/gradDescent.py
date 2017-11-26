import util
import copy
from scheduler import Team, Scheduler, Game

def gradientDescent(s):
    cost = s.costFn()
    i = 0
    print "Starting Cost:", cost

    while i < 1000:
        temp = copy.deepcopy(s)
        temp.swap()
        newCost = temp.costFn()
        if newCost < cost:
            cost = newCost
            s = temp
            i = 0
        else:
            i += 1

    return cost

if __name__ == '__main__':
    while True:
    	sc = Scheduler()
    	sc.randomStart()
    	if sc.isValidSchedule():
    		s = sc
    		break
    print "Starting Cost:", s.costFn
    print "Ending Cost:", gradientDescent(s)
