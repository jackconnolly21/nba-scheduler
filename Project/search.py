import util
from scheduler import Scheduler
from team import Team, Game, Schedule

# TRYING TO DO DFS TO FIND ALLOWABLE SCHEDULE 

def dfsSchedule(scheduler):
    # initialize frontier as stack, visited as dict
    frontier = util.Stack()
    # visited = dict()
    # push start state into frontier with empty list of actions and pathcost of 0
    frontier.push(scheduler.teams)
    # while the frontier is not empty, search
    while not frontier.isEmpty():
        # get leaf
        leaf = frontier.pop()
        # check if state of leaf is goal state
        if Scheduler.isGoalState(leaf):
            # if yes, return schedule, backToBacks
            return leaf
        # add leaf state to dict mapped to path cost
        # visited[leaf[0]] = leaf[1]
        # get children of node
        successors = Scheduler.getSuccessors(leaf)
        # iterate through children
        for successor in successors:
            # check if succesor is in visited
            # inVisited = successor[0] in visited
            # if not, then update child and push to frontier
            # if not inVisited:
            frontier.push(teams)
    # if no solution is found, return none
    return None
