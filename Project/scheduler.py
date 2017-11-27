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
        sch = util.sortSchedule(team.schedule)

        for i in xrange(len(sch) - 1):
            # Two home games in a row = no travel
            if sch[i].isHome and sch[i+1].isHome:
                total += 0
            # Two away games in a row = between opponent cities
            elif not sch[i].isHome and not sch[i+1].isHome:
                total += self.distances[sch[i].opponent.name][sch[i+1].opponent.name]
            # Away then home = opponent i --> home distance
            elif not sch[i].isHome and sch[i+1].isHome:
                total += self.distances[sch[i].opponent.name][team.name]
            # Otherwise home then away = home --> opponent i+1 distance
            else:
                total += self.distances[team.name][sch[i+1].opponent.name]
        return total

    # Calculate total travel distance for all teams
    def totalDistanceAll(self):
        total = 0
        for team in self.teams.values():
            total += self.totalDistanceTeam(team)
        return total

    def totalTriples(self):
        total = 0
        for team in self.teams.values():
            total += team.triples()
        return total

    def numHomeGames(self, team):
        homeGames = 0
        for game in team.schedule:
            if game.isHome:
                homeGames += 1
        return homeGames

    # Gets random new date that is open for both teams
    def getRandomDate(self, team1, team2):
        found = False
        while not found:
            newDate = random.choice(team1.teamCalendar.keys())
            if not team1.teamCalendar[newDate] and not team2.teamCalendar[newDate]:
                found = True
        return newDate

    def removeGameAtDate(self, date, team):
        for game in self.teams[team].schedule:
            if (game.date - date).days == 0:
                self.teams[team].schedule.remove(game)

    def costFn(self, a=1, b=3000, c=10000):
        totalDistance = self.totalDistanceAll()
        totalBTB = util.totalBackToBacks(self.teams)
        totalTriples = self.totalTriples()
        cost = a * totalDistance + b * totalBTB + c * totalTriples
        return cost

    """
        Move one game to another random date
    """
    def swap(self):
        randomTeam = random.choice(self.teams.values())
        randomGame = random.choice(randomTeam.schedule)
        opponent = randomGame.opponent
        oldDate = randomGame.date
        newDate = self.getRandomDate(randomTeam, opponent)
        # Remove the old game in both teams schedules
        self.removeGameAtDate(oldDate, randomTeam.name)
        self.removeGameAtDate(oldDate, opponent.name)
        # Add the game, but on new date
        self.teams[randomTeam.name].schedule.append(Game(newDate, self.teams[opponent.name], randomGame.isHome))
        self.teams[opponent.name].schedule.append(Game(newDate, self.teams[randomTeam.name], not randomGame.isHome))
        # Return stuff so the swap can be undone if necessary
        return (oldDate, newDate, randomTeam.name, opponent.name, randomGame.isHome)

    """
        Undo the swap done by swap()
    """
    def undoSwap(self, info):
        oldDate, newDate, team1, team2, team1IsHome = info
        # Remove the new games
        self.removeGameAtDate(newDate, team1)
        self.removeGameAtDate(newDate, team2)
        # Add back the old games
        self.teams[team1].schedule.append(Game(oldDate, self.teams[team2], team1IsHome))
        self.teams[team2].schedule.append(Game(oldDate, self.teams[team1], not team1IsHome))
        return True

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
                        if not team.teamCalendar[randomDate] and not divOpp.teamCalendar[randomDate]:
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
                    if not team.teamCalendar[randomDate] and not nonConfOpp.teamCalendar[randomDate]:
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
                    if not team.teamCalendar[randomDate] and not commonNonDivOpp.teamCalendar[randomDate]:
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
                    if not team.teamCalendar[randomDate] and not rareNonDivOpp.teamCalendar[randomDate]:
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
            i = 0
            # NEEDS TO PRINT IN TWICE TO BE CORRECT
            for tm2 in self.teams.values():
                if team in tm2.HA[1]:
                    i += 1
            if i != 2:
                self.makeHAConsistent(team)

        for team in self.teams.values():
            for h in team.HA[0]:
                i = 0
                while i < 1:
                    randomDate = random.choice(team.teamCalendar.keys())
                    # make sure game isn't already played on that date
                    if not team.teamCalendar[randomDate] and not h.teamCalendar[randomDate]:
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



    # not being used
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



    # think this is making previous teams' HAs inconsistent
    def makeHAConsistent(self, team):
        for tm2 in team.HA[0]:
            self.swapHA(team, tm2)
        for tm3 in team.HA[1]:
            self.swapHA(team, tm3)
        i = 0
        for tm4 in self.teams.values():
            if tm4 in team.HA[0]:
                i += 1
        if i != 2:
            print team.name

    def isValidSchedule(self):
        for team in self.teams.values():
            if len(team.schedule) != 82 or self.numHomeGames(team) != 41:
                return False
        return True


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

# Defining a team object
class Team:
    def __init__(self, name, conference, division, location):
        self.name = name # Simple name of the team
        self.conference = conference # Eastern or Western
        self.division = division # one of 6 divisions
        self.location = location # (lat, lng) tuple in radians
        self.schedule = [] # list of 82 game objects (see Game class)
        self.teamCalendar = util.getCalendarCSV('schedule.csv')
        self.commonNonDivOpps = []
        self.rareNonDivOpps = []
        self.HA = [[],[]] # ([rareNonDivOpps that will be played extra time at home], [extra on road])

    # Iterate over self.schedule and calculate number of back to backToBacks
    def backToBacks(self):
        btb = 0
        self.schedule = util.sortSchedule(self.schedule)
        for i in xrange(len(self.schedule) - 1):
            g1 = self.schedule[i]
            g2 = self.schedule[i + 1]
            timeDelta = g2.date - g1.date
            if timeDelta.days == 1:
                btb += 1
        return btb

    # Iterate over self.schedule and calculate number of back to backToBacks
    def triples(self):
        trip = 0
        self.schedule = util.sortSchedule(self.schedule)
        for i in xrange(len(self.schedule) - 2):
            g1 = self.schedule[i].date
            g2 = self.schedule[i+2].date
            timeDelta = g2 - g1
            if timeDelta.days == 2:
                trip += 1
        return trip

    def __str__(self):
        info = [self.name, self.conference, self.division, self.location]
        string = ",".join(str(i) for i in info)
        return string

# Defines game object for schedule
class Game:
    def __init__(self, date, opponent, isHome):
        self.date = date # Date time object
        self.opponent = opponent # object of opponent
        self.isHome = isHome # boolean whether or not its a home game

    def __str__(self):
        info = [self.date, self.opponent, self.isHome]
        return ",".join(str(i) for i in info)
