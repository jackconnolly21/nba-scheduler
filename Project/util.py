from math import cos, sin, acos
import csv
from collections import defaultdict
from team import Team

"""
t1 and t2 are (lat, lng) tuples for 2 teams

Calculates closest distance over the Earth using
spherical law of cosines as described here:
https://www.movable-type.co.uk/scripts/latlong.html
"""
def latLongDistance(t1, t2):
    earthRadius = 3959 # miles
    lat1, lng1 = t1 # lat, lng of first team
    lat2, lng2 = t2 # and of second team
    dLng = lng2 - lng1 # change in longitude

    y = sin(lat1) * sin(lat2)
    x = cos(lat1) * cos(lat2) * cos(dLng)

    if (x + y) > 1:
        return 0

    distance = acos(x + y) * earthRadius

    return distance

def readTeamsCSV(teamsCSV):
    teams = list()
    with open(teamsCSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name = row[0]
            conference = row[1]
            division = row[2]
            lat = float(row[3])
            lng = float(row[4])
            teams.append(Team(name, conference, division, (lat, lng)))

    return teams

def calculateDistances(teams):
    distances = defaultdict(dict)
    for t1 in teams:
        for t2 in teams:
            distances[t1.name][t2.name] = latLongDistance(t1.location, t2.location)

    return distances
