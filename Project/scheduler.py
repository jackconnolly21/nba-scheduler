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

    def numHomeGames(self, team):
        homeGames = 0
        for game in team.schedule:
            if game.isHome:
                homeGames += 1
        return homeGames

    def costFn(self, a=1, b=3000):
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


            self.getCommonNonDivOpps(team)
            # generates 12 home games
            # this is working
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

            self.getRareNonDivOpps(team)

            for rareNonDivOpp in team.rareNonDivOpps:
                i = 0
                while i < 1:
                    randomDate = random.choice(team.teamCalendar.keys())
                    # make sure game isn't already played on that date
                    if not team.teamCalendar[randomDate]:
                        # add game to schedule of both teams
                        team.schedule.append(Game(randomDate, rareNonDivOpp, True))
                        rareNonDivOpp.schedule.append(Game(randomDate, team, False))
                        # turn value to True
                        team.teamCalendar[randomDate] = True
                        rareNonDivOpp.teamCalendar[randomDate] = True
                        # increment i
                        i += 1

        
        # makes all teams have HA lists of rndo
        for team in self.teams.values():
            self.initializeHA(team)
        
        for team in self.teams.values():
            self.makeHAConsistent(team)

        for team in self.teams.values():
            # NEEDS TO PRINT IN TWICE TO BE CORRECT
            # if self.teams["Milwaukee Bucks"] in team.HA[1]:
            #         print "in"
                
            for h in team.HA[0]:
                i = 0
                while i < 1:
                    randomDate = random.choice(team.teamCalendar.keys())
                    # make sure game isn't already played on that date
                    if not team.teamCalendar[randomDate]:
                        # add game to schedule of both teams
                        team.schedule.append(Game(randomDate, h, True))
                        h.schedule.append(Game(randomDate, team, False))
                        # turn value to True
                        team.teamCalendar[randomDate] = True
                        h.teamCalendar[randomDate] = True
                        # increment i
                        i += 1

        # for t in self.teams["Boston Celtics"].rareNonDivOpps:
        #     if self.teams["Milwaukee Bucks"] in t.rareNonDivOpps:
        #         print t

        # Set self.teams with new schedules
        return True

    def getNonDivOpps(self, team):
        nonDivOpps = []
        for confOpp in self.conferences[team.conference]:
            if confOpp not in self.divisions[team.division]:
                nonDivOpps.append(confOpp)
        return nonDivOpps

    # problem with this function
    def getCommonNonDivOpps(self, team):
        cndo = team.commonNonDivOpps
        nonDivOpps = self.getNonDivOpps(team)
        if len(cndo) > 6:
            rand = random.choice(cndo)
            cndo.remove(rand)
            rand.commonNonDivOpps.remove(team)
            self.getCommonNonDivOpps(team)
            self.getCommonNonDivOpps(rand)
        elif len(cndo) < 6:
            frontier = []
            for t in nonDivOpps:
                if t not in cndo:
                    frontier.append((t, len(t.commonNonDivOpps)))
            minlen = 100
            minindex = -1
            # picking the team with the fewest commonNonDivOpps to add
            # need I need to introduce more randomness
            for f in xrange(len(frontier)):
                if frontier[f][1] <= minlen:
                    minlen = frontier[f][1]
                    minindex = f
            rand1 = frontier[minindex][0]
            cndo.append(rand1)
            rand1.commonNonDivOpps.append(team)
            self.getCommonNonDivOpps(team)
            self.getCommonNonDivOpps(rand1)

    def getRareNonDivOpps(self, team):
        cndo = team.commonNonDivOpps
        rndo = team.rareNonDivOpps
        for rareNonDivOpp in self.getNonDivOpps(team):
            if rareNonDivOpp not in cndo:
                rndo.append(rareNonDivOpp)
                # rareNonDivOpp.rareNonDivOpps.append(team)

   

    # this is what I need to get working
    def getRareNonDivOppsHT(self, team):
        rndo = team.rareNonDivOpps
        if len(team.HA[0]) == 2 and len(team.schedule) > 82:
            print "here"
            # never going in here
            # frontier = []
            # for t in team.HA[0]:
            #     frontier.append((t, len(t.HA[1])))
            # maxlen = -1
            # maxindex = -1
            # for f in xrange(len(frontier)):
            #     if frontier[f][1] >= maxlen:
            #         maxlen = frontier[f][1]
            #         maxindex = f
            # rand2 = frontier[maxindex][0]
            rand2 = random.choice(team.HA[1])
            team.HA[1].remove(rand2)
            rand2.HA[0].remove(team)
            self.getRareNonDivOppsHT(team)
        elif len(team.HA[0]) < 2:
            frontier = []
            for t in rndo:
                if t not in team.HA[0]:
                    frontier.append((t, len(t.HA[1])))
            minlen = 100
            minindex = -1
            for f in xrange(len(frontier)):
                if frontier[f][1] <= minlen:
                    minlen = frontier[f][1]
                    minindex = f
            rand1 = frontier[minindex][0]
            team.HA[0].append(rand1)
            rand1.HA[1].append(team)
            self.getRareNonDivOppsHT(team)
        # elif len(team.HA[0]) == 2 and len(team.schedule) < 82:
        #     rand2 = random.choice(rndo)
        #     team.HA[1].append(rand2)
        #     rand2.HA[0].append(team)
        #     self.getRareNonDivOppsHT(team)
        #     self.getRareNonDivOppsHT(rand2)   

    
    def initializeHA(self, team):
        team.HA[0] = random.sample(team.rareNonDivOpps, 2)
        team.HA[1] = [i for i in team.rareNonDivOpps if i not in team.HA[0]]

    def swapHA (self, tm1, tm2):
        # if tm2 is in tm1.HA[0] then tm1 needs to be in tm2.HA[1]
        while tm2 in tm1.HA[0] and tm1 not in tm2.HA[1]:
            # swaps position of tm1
            tm2.HA[1].append(tm1)
            tm2.HA[0].remove(tm1)
            # balances sizes of HA[1] and HA[2]
            r = random.choice(tm2.HA[1])
            tm2.HA[1].remove(r)
            tm2.HA[0].append(r)
        while tm2 in tm1.HA[1] and tm1 not in tm2.HA[0]:
            tm2.HA[0].append(tm1)
            tm2.HA[1].remove(tm1)
            r = random.choice(tm2.HA[0])
            tm2.HA[0].remove(r)
            tm2.HA[1].append(r)



    def makeHAConsistent(self, team):
        for tm2 in team.HA[0]:
            self.swapHA(team, tm2)
        for tm3 in team.HA[1]:
            self.swapHA(team, tm3)
        i = 0
        for tm4 in self.teams.values():
            if self.teams["Los Angeles Lakers"] in tm4.HA[1]:
                i += 1
        if i != 2: 
            print "prob"




        # elif len(team.HA[1]) > 2:
        #     randH = random.choice(team.HA[1]) 
        #     team.HA[1].remove(randH)
        #     randH.HA[0].remove(team)
        #     self.getRareNonDivOppsHT(team)
        #     self.getRareNonDivOppsHT(randH)
        # elif len(team.HA[1]) < 2:
        #     frontier = []
        #     for t in rndo:
        #         if t not in team.HA[1]:
        #             frontier.append((t, len(t.HA[0])))
        #     minlen = 100
        #     minindex = -1
        #     # picking the team with the fewest commonNonDivOpps to add
        #     # need I need to introduce more randomness
        #     for f in xrange(len(frontier)):
        #         if frontier[f][1] <= minlen:
        #             minlen = frontier[f][1]
        #             minindex = f
        #     rand1 = frontier[minindex][0]
        #     team.HA[1].append(rand1)
        #     rand1.HA[0].append(team)
        #     self.getRareNonDivOppsHT(team)
        #     self.getRareNonDivOppsHT(rand1)

            # for tm1 in randH:
            #     tm1.HA[1].append(team)
            # randA = [i for i in rndo if i not in team.HA[0]]
            # team.HA[1] = randA
            # for tm0 in randA:
            #     tm0.HA[0].append(team)
            # i = 0
            # for tm2 in self.teams.values():
            #     if team in tm2.HA[0]:
            #         print "here"
            #         i += 1
            # if i > 2:
            #     print team.name
            #     randT = random.choice(team.HA[0])
            #     team.HA[0].remove(randT)
            #     randT.HA[1].remove(team)
            #     self.getRareNonDivOppsHT(team)
            #     self.getRareNonDivOppsHT(randT)


        # if len(team.HA[0]) > 2:
        #     randT = random.choice(team.HA[0])
        #     team.HA[0].remove(randT)
        #     randT.HA[1].remove(team)
        #     self.getRareNonDivOppsHT(team)
        #     self.getRareNonDivOppsHT(randT)
        # elif len(team.HA[0]) < 2:
        #     randT = random.choice(team.HA[0])
        #     team.HA[0].append(randT)
        #     randT.HA[1].append(team)
        #     self.getRareNonDivOppsHT(team)
        #     self.getRareNonDivOppsHT(randT)









    """
        Move one game to another random date
    """
    def swap(self, teams):
        randomTeam = random.choice(teams.keys())
        randomGame = random.choice(randomTeam.schedule)
        pass

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
        self.rareNonDivOpps = []
        self.HA = [[],[]] # ([rareNonDivOpps that will be played extra time at home], [extra on road])
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
