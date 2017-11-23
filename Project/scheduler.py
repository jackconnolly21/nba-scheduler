# Main file for the CSP?
import util
from datetime import date
import random

class Scheduler:
    """
    Create an object, storing all teams, distances
    """
    def __init__(self, csvFile='teams.csv', testSchedule=False):
        self.teams, self.conferences, self.divisions = util.readTeamsCSV(csvFile)
        self.distances = util.calculateDistances(self.teams)
        self.startDate = date(2017, 10, 17)
        self.seasonCalendar = util.getCalendarCSV('schedule.csv')
        if testSchedule:
            util.readScheduleCSV('schedule.csv', self.teams)

    # Iterate over team.schedule and calculate total travel distance for one team
    # Have to account for if home/away and where going to next/from
    def totalDistanceTeam(self, team):
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
    def totalDistanceAll(self, teams):
        total = 0
        for team in teams.values():
            total += self.totalDistanceTeam(team)
        return total

    def isGoalState(self, teams):
        for team in teams.values():
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

    def numHomeGames(self, team):
        homeGames = 0
        for game in team.schedule:
            if game.isHome:
                homeGames += 1
        return homeGames

    def costFn(self, a, b):
        totalDistance = self.totalDistanceAll(self.teams)
        totalBTB = util.totalBackToBacks(self.teams)
        cost = a * totalDistance + b * totalBTB
        return cost

    """
        Create a random initial schedule satisfying constraints
    """
    def randomStart(self):
        """
            Maybe keep track of a list of open dates for each team?
            Also maybe keep track of a list of teams that we already assigned schedules to
                --> So we don't assign more games to them
                --> Like theoretically last team should have full schedule
                    before we even assign it
        """
        for team in self.teams.values():

            if team.conference == "Eastern":
                otherConf = "Western"
            else:
                otherConf = "Eastern"

            # generates 8 home games
            for divOpp in self.divisions[team.division]:
                if team.name != divOpp.name:
                    # Randomly choose 2 open dates and assign home games
                    i = 0
                    while i < 2:
                        randomDate = random.choice(team.teamCalendar.keys())
                        # make sure game isn't already played on that date
                        if not team.teamCalendar[randomDate]:
                            # add game to schedule of both teams
                            team.schedule.append(Game(randomDate, divOpp, True))
                            divOpp.schedule.append(Game(randomDate, team, False))
                            # turn value to True
                            team.teamCalendar[randomDate] = True
                            divOpp.teamCalendar[randomDate] = True
                            # increment i
                            i += 1

            # generates 15 home games
            for nonConfOpp in self.conferences[otherConf]:
                # Randomly choose 1 open date and assign home game
                i = 0
                while i < 1:
                    randomDate = random.choice(team.teamCalendar.keys())
                    # make sure game isn't already played on that date
                    if not team.teamCalendar[randomDate]:
                        # add game to schedule of both teams
                        team.schedule.append(Game(randomDate, nonConfOpp, True))
                        nonConfOpp.schedule.append(Game(randomDate, team, False))
                        # turn update calendar
                        team.teamCalendar[randomDate] = True
                        nonConfOpp.teamCalendar[randomDate] = True
                        # increment i
                        i += 1

            # # generates 20 home games
            # for confOpp in self.conferences[team.conference]:
            #     if confOpp not in self.divisions[team.division]:
            #     # Randomly choose 1 or 2?
            #     # starting with 2
            #         i = 0
            #         while i < 2:
            #             randomDate = random.choice(team.teamCalendar.keys())
            #             # make sure game isn't already played on that date
            #             if not team.teamCalendar[randomDate]:
            #                 # add game to schedule of both teams
            #                 team.schedule.append(Game(randomDate, confOpp, True))
            #                 confOpp.schedule.append(Game(randomDate, team, False))
            #                 # turn value to True
            #                 team.teamCalendar[randomDate] = True
            #                 confOpp.teamCalendar[randomDate] = True
            #                 # increment i
            #                 i += 1

            # randomly pick 6 confOpps to play 4 times
            # play the other 4 3 times,
            nonDivOpps = []
            for confOpp in self.conferences[team.conference]:
                if confOpp not in self.divisions[team.division]:
                    nonDivOpps.append(confOpp)

            # getting stuck in this loop
            while len(team.commonNonDivOpps) < 6:
                print len(team.commonNonDivOpps)
                randIndex = random.randint(0, 9)
                randNonDivOpp = nonDivOpps[randIndex]
                # getting stuck at this if statement
                # this part is a CSP in itself. Need to find better way to solve this
                if randNonDivOpp not in team.commonNonDivOpps and len(randNonDivOpp.commonNonDivOpps) < 6:
                    team.commonNonDivOpps.append(randNonDivOpp)
                    randNonDivOpp.commonNonDivOpps.append(team)
                    print
                    for t in team.commonNonDivOpps:
                        print t.name



            # generates 12 home games
            for commonNonDivOpp in team.commonNonDivOpps:
                i = 0
                while i < 2:
                    randomDate = random.choice(team.teamCalendar.keys())
                    # make sure game isn't already played on that date
                    if not team.teamCalendar[randomDate]:
                        # add game to schedule of both teams
                        team.schedule.append(Game(randomDate, commonNonDivOpp, True))
                        commonNonDivOpp.schedule.append(Game(randomDate, team, False))
                        # turn value to True
                        team.teamCalendar[randomDate] = True
                        commonNonDivOpp.teamCalendar[randomDate] = True
                        # increment i
                        i += 1




        # Set self.teams with new schedules
        return True

    """
        Move one game to another random date
    """
    def swap(self, teams):
        randomTeam = random.choice(teams.keys())
        randomGame = random.choice(randomTeam.schedule)

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
        self.teamCalendar = util.getCalendarCSV('schedule.csv')
        self.commonNonDivOpps = []
    # Iterate over self.schedule and calculate number of back to backToBacks
    def backToBacks(self):
        btb = 0
        for i in xrange(len(self.schedule) - 1):
            g1 = self.schedule[i]
            g2 = self.schedule[i + 1]
            timeDelta = g2.date - g1.date
            if timeDelta.days == 1:
                btb += 1
        return btb

    def __str__(self):
        info = [self.name, self.conference, self.division, self.location]
        string = ",".join(str(i) for i in info)
        return string

# Defines game object for schedule
class Game:
    def __init__(self, date, opponent, isHome):
        self.date = date # Date time object
        self.opponent = opponent # name of opponent
        self.isHome = isHome # boolean whether or not its a home game

    def __str__(self):
        info = [self.date, self.opponent, self.isHome]
        return ",".join(str(i) for i in info)

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
