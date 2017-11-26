import util
import copy
from scheduler import Team, Scheduler, Game
from timeit import default_timer as timer

def gradientDescent(s):
    cost = s.costFn()
    i = 0

    while i < 50:
        # Its the copy that takes almost all of the time 
        beforeCopy = timer()
        temp = copy.deepcopy(s)
        afterCopy = timer()
        temp.swap()
        afterSwap = timer()
        newCost = temp.costFn()
        afterCostFn = timer()
        if newCost < cost:
            cost = newCost
            s = temp
        i += 1
        print "Copy:", afterCopy - beforeCopy
        print "Swap:", afterSwap - afterCopy
        print "CostFn:", afterCostFn - afterSwap
        print


    return cost

if __name__ == '__main__':
    while True:
    	sc = Scheduler()
    	sc.randomStart()
    	if sc.isValidSchedule():
    		s = sc
    		break
    print "Starting Cost:", s.costFn()
    new = gradientDescent(s)
    print "Ending Cost:", new
