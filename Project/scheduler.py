# Main file for the CSP?
import util

class Scheduler:
    """
    Create an object, storing all teams, distances
    """
    def init(self, csvFile='teams.csv'):
        self.teams = util.readTeamsCSV(csvFile)
        self.distances = calculateDistances(self.teams)


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
