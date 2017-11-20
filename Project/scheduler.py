# Main file for the CSP?
import util
from team import Team, Game

class Scheduler:
    """
    Create an object, storing all teams, distances
    """
    def __init__(self, csvFile='teams.csv'):
        self.teams, self.conferences, self.divisions = util.readTeamsCSV(csvFile)
        self.distances = util.calculateDistances(self.teams)

    def getTeams(self):
        return self.teams

    # Iterate over team.schedule and calculate total travel distance for one team
    def totalDistanceTeam(team):
        # total = 0
        # for game in team.schedule:
        #     total += self.distances[team.name][game.opponent]
        # return total
        pass

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
