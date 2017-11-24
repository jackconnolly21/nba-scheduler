import util
from scheduler import Team, Scheduler, Game

def gradientDescent(s):
    cost = s.costFn()
    i = 0

    while i < 1000:
        temp = s.copy()
        temp.swap(temp.teams)
        newCost = temp.costFn()
        if newCost < cost:
            cost = newCost
            s = temp
            i = 0
        else:
            i += 1

    return cost

        # elif util.flipCoin()

if __name__ == '__main__':
    s = Scheduler()
    s.randomStart()
    gradientDescent(s)
