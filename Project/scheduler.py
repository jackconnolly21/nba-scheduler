# Main file for the CSP?
import util
from team import Team, Game

class Scheduler:
    """
    Create an object, storing all teams, distances
    """
    def __init__(self, csvFile='teams.csv'):
        self.teams = util.readTeamsCSV(csvFile)
        self.distances = util.calculateDistances(self.teams)

    def getTeams(self):
        return self.teams

    def findSchedule(self, method="SA"):
        """
        Given a schedule object (list of 30 NBA teams)
        Calculate a (hopefully) optimal schedule, satisfying hard constraints

        Call some method for doing so, default Simulate Annealing?
        """
        pass

    # Calculate a schedule by SA, minimizing certain factors
    def simulatedAnnealing(self):
        pass

    # Iterate over team.schedule and calculate total travel distance for one team
    def totalDistanceTeam(team):
        total = 0
        for game in team.schedule:
            total += self.distances[team.name][game.opponent]
        return total

    # Calculate total travel distance for all teams
    def totalDistanceAll(teams):
        total = 0
        for team in teams:
            total += self.totalDistanceTeam(team)
        return total

    def isGoalState(self):
        for team in self.teams:
            if not team.schedule.isValid():
                return False
        return True
