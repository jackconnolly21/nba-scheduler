# Main file for the CSP?
import util
from datetime import date, timedelta
import random

class Scheduler:
    """
    Create an object, storing all teams, distances
    """
    def __init__(self, csvFile='data/teams.csv', testSchedule=False):
        self.teams, self.conferences, self.divisions = util.readTeamsCSV(csvFile)
        self.distances = util.calculateDistances(self.teams)
        if testSchedule:
            util.readScheduleCSV('data/schedule.csv', self.teams)
        self.trace = []

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
            if not self.teams[team1.name].teamCalendar[newDate] and not self.teams[team2.name].teamCalendar[newDate]:
                found = True
        return newDate

    # Remove game in team's schedule on date against opponent
    def removeGameAtDate(self, date, team, opponent):
        for game in self.teams[team].schedule:
            if (game.date - date).days == 0 and game.opponent.name == opponent:
                self.teams[team].schedule.remove(game)
                self.teams[team].teamCalendar[date] = False
                return True
        return False

    def getStandardDevs(self):
        btbs = [team.backToBacks() for team in self.teams.values()]
        dists = [self.totalDistanceTeam(team) for team in self.teams.values()]
        btbSTD = util.standardDev(btbs)
        distSTD = util.standardDev(dists)
        return (btbSTD, distSTD)

    def costFn(self, a=1, b=3000, c=10000, d=10):
        totalDistance = self.totalDistanceAll()
        totalBTB = util.totalBackToBacks(self.teams)
        totalTriples = self.totalTriples()
        btbSTD, distSTD = self.getStandardDevs()
        cost = a * totalDistance + b * totalBTB + c * (totalTriples**2) + d * (btbSTD * 4000 + distSTD)
        return cost

    def multiSwap(self, numSwaps):
        infos = []
        for i in xrange(numSwaps):
            infos.append(self.swap())
        return infos

    def undoMultiSwap(self, infos):
        for i in xrange(len(infos) - 1, -1, -1):
            self.undoSwap(infos[i])
        return True

    """
        Move one game to another random date
    """
    def swap(self):
        # Generate random team, game, newDate
        randomTeam = random.choice(self.teams.values())
        randomGame = random.choice(randomTeam.schedule)
        opponent = randomGame.opponent
        oldDate = randomGame.date
        newDate = self.getRandomDate(randomTeam, opponent)

        # Remove the old game in both teams schedules
        self.removeGameAtDate(oldDate, randomTeam.name, opponent.name)
        self.removeGameAtDate(oldDate, opponent.name, randomTeam.name)

        # Add the game, but on new date
        self.teams[randomTeam.name].schedule.append(Game(newDate, self.teams[opponent.name], randomGame.isHome))
        self.teams[randomTeam.name].teamCalendar[newDate] = True

        self.teams[opponent.name].schedule.append(Game(newDate, self.teams[randomTeam.name], not randomGame.isHome))
        self.teams[opponent.name].teamCalendar[newDate] = True

        # Return stuff so the swap can be undone if necessary
        return (oldDate, newDate, randomTeam.name, opponent.name, randomGame.isHome)

    """
        Undo the swap done by swap()
    """
    def undoSwap(self, info):

        # Unpack info returned from swap
        oldDate, newDate, team1, team2, team1IsHome = info

        # Remove the new games
        self.removeGameAtDate(newDate, team1, team2)
        self.removeGameAtDate(newDate, team2, team1)

        # Add back the old games
        self.teams[team1].schedule.append(Game(oldDate, self.teams[team2], team1IsHome))
        self.teams[team1].teamCalendar[oldDate] = True

        self.teams[team2].schedule.append(Game(oldDate, self.teams[team1], not team1IsHome))
        self.teams[team2].teamCalendar[oldDate] = True

        return True

    def tripcheck(self, team, date):
        previous = date - timedelta(days=1)
        previous2 = previous - timedelta(days=1)
        nextday = date + timedelta(days=1)
        nextday2 = nextday + timedelta(days=1)
        if nextday in team.teamCalendar and nextday2 in team.teamCalendar:
            if team.teamCalendar[nextday] and team.teamCalendar[nextday2]:
                return False
        if nextday in team.teamCalendar and previous in team.teamCalendar:
            if team.teamCalendar[nextday] and team.teamCalendar[previous]:
                return False
        if previous in team.teamCalendar and previous2 in team.teamCalendar:
            if team.teamCalendar[previous2] and team.teamCalendar[previous]:
                return False
        return True

    def removeTriples(self):
        trips = self.totalTriples()
        iterations = 0
        successes = 0
        while trips > 0:
            info = self.swap()
            newTrips = self.totalTriples()
            if newTrips < trips:
                trips = newTrips
                iterations += 1
                successes += 1
            else:
                self.undoSwap(info)
                iterations += 1
        return (iterations, successes)

    """
        Create a random initial schedule satisfying constraints
    """
    def randomStart(self):
        """
           This function creates random schedules. It generally creates a valid 
           schedule every about 5 attempts and doesn't take too much time to run.
           To guarantee the product of a valid schedule, it should be used in a while
           loop with isValidSchedule function (see test.py for example).
        """
        # iterate through all teams
        for team in self.teams.values():

            # store which conference each team is in
            if team.conference == "Eastern":
                otherConf = "Western"
            else:
                otherConf = "Eastern"

            # generates 8 home games, 2 against each divisional opponent
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

            # generates 15 home games, 1 against each non conference opponent
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

            # this function chooses which teams a team will play 4 games against
            self.setCommonNonDivOpps(team)
            # generates 12 home games, 2 against each commonNonDivOpp
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

            # stores the teams in the conference that aren't commonNonDivOpps
            self.setRareNonDivOpps(team)
            # generates 4 home games, 1 home against each rareNonDivOpp
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


        # makes all teams have HA lists of rareNonDivOpps
        for team in self.teams.values():
            self.initializeHA(team)
        # go through each team and make sure these games fit with previous set values
        for team in self.teams.values():
            self.makeHAConsistent(team)
        # if HA values have been messed up try to fix them
        for team in self.teams.values():
            i = 0
            for tm2 in self.teams.values():
                if team in tm2.HA[1]:
                    i += 1
            if i != 2:
                self.makeHAConsistent(team)

        # generates 2 home games, 1 each each team in team.HA[0]
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
        return True

    def getNonDivOpps(self, team):
        nonDivOpps = []
        for confOpp in self.conferences[team.conference]:
            if confOpp not in self.divisions[team.division]:
                nonDivOpps.append(confOpp)
        return nonDivOpps

    def setCommonNonDivOpps(self, team):
        cndo = team.commonNonDivOpps
        nonDivOpps = self.getNonDivOpps(team)
        if len(cndo) > 6:
            rand = random.choice(cndo)
            cndo.remove(rand)
            rand.commonNonDivOpps.remove(team)
            self.setCommonNonDivOpps(team)
            self.setCommonNonDivOpps(rand)
        elif len(cndo) < 6:
            frontier = []
            for t in nonDivOpps:
                if t not in cndo:
                    frontier.append((t, len(t.commonNonDivOpps)))
            minlen = 100
            minindex = -1
            # picking the team with the fewest commonNonDivOpps to add
            for f in xrange(len(frontier)):
                if frontier[f][1] <= minlen:
                    minlen = frontier[f][1]
                    minindex = f
            rand1 = frontier[minindex][0]
            cndo.append(rand1)
            rand1.commonNonDivOpps.append(team)
            self.setCommonNonDivOpps(team)
            self.setCommonNonDivOpps(rand1)

    def setRareNonDivOpps(self, team):
        cndo = team.commonNonDivOpps
        rndo = team.rareNonDivOpps
        for rareNonDivOpp in self.getNonDivOpps(team):
            if rareNonDivOpp not in cndo:
                rndo.append(rareNonDivOpp)

    # HA represents two groups of teams for each team
    # HA[0] is the group of rareNonDivOpps that a team should play 2 home games against
    # HA[1] is the group that a team should play 2 away games against, (and 1 home game)
    def initializeHA(self, team):
        team.HA[0] = random.sample(team.rareNonDivOpps, 2)
        team.HA[1] = [i for i in team.rareNonDivOpps if i not in team.HA[0]]

    # function moves a team from HA[0] to HA[1] or vice versa, and balances the size
    # of the lists
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

    # if team1 is in HA[1] of team2, team1 must be in HA[0] of team2
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

    # checks that each team has 82 games and 41 home games
    def isValidSchedule(self):
        for team in self.teams.values():
            if len(team.schedule) != 82 or self.numHomeGames(team) != 41:
                return False
        return True

# Defining a team object
class Team:
    def __init__(self, name, conference, division, location):
        self.name = name # Simple name of the team
        self.conference = conference # Eastern or Western
        self.division = division # one of 6 divisions
        self.location = location # (lat, lng) tuple in radians
        self.schedule = [] # list of 82 game objects (see Game class)
        self.teamCalendar = util.getCalendarCSV('data/schedule.csv')
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
