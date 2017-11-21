# Main file for the CSP?
import util

class Scheduler:
    """
    Create an object, storing all teams, distances
    """
    def __init__(self, csvFile='teams.csv'):
        self.teams, self.conferences, self.divisions = util.readTeamsCSV(csvFile)
        self.distances = util.calculateDistances(self.teams)

    # Iterate over team.schedule and calculate total travel distance for one team
    # Have to account for if home/away and where going to next/from
    def totalDistanceTeam(team):
        total = 0
        sch = team.schedule
        for i in xrange(len(sch) - 1):
            # Two home games in a row = no travel
            if sch[i].isHome and sch[i+1].isHome:
                total += 0
            # Two away games in a row = between opponent cities
            elif not sch[i].isHome and not sch[i+1].isHome:
                total += self.distances[sch[i].opponent][sch[i+1].opponent]
            # Away then home = opponent i --> home distance
            elif not sch[i].isHome and sch[i+1].isHome:
                total += self.distances[sch[i].opponent][team.name]
            # Otherwise home then away = home --> opponent i+1 distance
            else:
                total += self.distances[team.name][sch[i+1].opponent]
        return total

    # Calculate total travel distance for all teams
    def totalDistanceAll(teams):
        total = 0
        for team in teams:
            total += self.totalDistanceTeam(team)
        return total

    def isGoalState(teams):
        for team in teams:
            if not self.scheduleIsValid(team):
                return False
        return True

    def scheduleIsValid(self, team):
        if len(schedule) != 82:
            return False
        if schedule.numHomeGames() != 41:
            return False
        for team in self.conferences:
            # idk we gotta check somehow
            pass
        return True

# Defining a team object
class Team:
    def __init__(self, name, conference, division, location):
        self.name = name # Simple name of the team
        self.conference = conference # Eastern or Western
        self.division = division # one of 6 divisions
        self.location = location # (lat, lng) tuple in radians
        self.schedule = [] # list of 82 game objects (see Game class)
        # idk if we'll need this, probably not, but might help
        self.opponents = util.Counter() # holds counts of games v. each opponent

    # Iterate over self.schedule and calculate number of back to backToBacks
    def backToBacks(self):
        btb = 0
        for i in xrange(len(self.schedule) - 1):
            g1 = self.schedule[i]
            g2 = self.schedule[i + 1]
            if g2.date - g1.date == 1:
                btb += 1
        return btb

    def __str__(self):
        info = [self.name, self.conference, self.division, self.location]
        string = ",".join(str(i) for i in info)
        return string

# Defines game object for schedule
class Game:
    def __init__(self, date, opponent, isHome):
        self.date = date # Date time object? Idk?
        self.opponent = opponent # name of opponent
        self.isHome = isHome # boolean whether or not its a home game

    def __str__(self):
        info = [self.date, self.opponent, self.isHome]
        return ",".join(str(i) for i in info)

class Schedule:
    def __init__(self):
        self.schedule = [] # Going to be a list of game objects

    def numHomeGames(self):
        homeGames = 0
        for game in self.schedule:
            if game.isHome:
                homeGames += 1
        return homeGames

"""
    Finding initialization of a schedule to do local search on
    NOT DONE (I've made changes but definitely not at all working)
"""
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
