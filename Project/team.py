# Defining a team object
class Team:
    def __init__(self, name, conference, division, location):
        self.name = name # Simple name of the team
        self.conference = conference # Eastern or Western
        self.division = division # one of 6 divisions
        self.location = location # (lat, lng) tuple in radians
        self.schedule = [] # list of 82 game objects (see Game class)

    def getName(self):
        return self.name

    def getConference(self):
        return self.conference

    def getDivision(self):
        return self.division

    def getLocation(self):
        return self.location

    def getSchedule(self):
        return self.schedule

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
        self.opponent = opponent # name of opponent (not a team object?)
        self.isHome = isHome # boolean whether or not its a home game

    def getDate(self):
        return self.date

    def getOpponent(self):
        return self.opponent

    def getIsHome(self):
        return self.isHome

    def __str__(self):
        info = [self.date, self.opponent, self.isHome]
        return ",".join(str(i) for i in info)
