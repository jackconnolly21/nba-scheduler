

# Defining a team object
class Team:
    def init(self, name, conference, division, location):
        self.name = name # Simple name of the team
        self.conference = conference # Eastern or Western
        self.division = division # one of 6 divisions
        self.location = location # (lat, lng) tuple in radians
        self.schedule = [] # list of 82 game objects (see game.py)

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

    # Iterate over self.schedule and calculate total travel distance
    def totalDistance(self):
        pass

    # Iterate over self.schedule and calculate number of back to backToBacks
    def backToBacks(self):
        pass

# Defines game object for schedule
class Game:
    def init(self, date, opponent, isHome):
        self.date = date # Date time object? Idk?
        self.opponent = opponent # name of opponent (not a team object?)
        self.isHome = isHome # boolean whether or not its a home game

    def getDate(self):
        return self.date

    def getOpponent(self):
        return self.opponent

    def getIsHome(self):
        return self.isHome
