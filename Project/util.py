from math import cos, sin, acos
import csv
from collections import defaultdict
from scheduler import Team, Scheduler, Game
from datetime import date
import random

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
    teams = dict()
    conferences = {"Western": list(), "Eastern": list()}
    divisions = {"Atlantic": list(), "Central": list(),
                "Southeast": list(), "Southwest": list(),
                "Northwest": list(), "Pacific": list()}
    with open(teamsCSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name = row[0]
            conference = row[1]
            division = row[2]
            lat = float(row[3])
            lng = float(row[4])
            teams[name] = Team(name, conference, division, (lat, lng))
            # changed these to be lists of team objects instead of team names
            conferences[conference].append(teams[name])
            divisions[division].append(teams[name])

    return (teams, conferences, divisions)

"""
    Reads in a .csv file of the NBA schedule and puts into teams list
    Not working because we need opponent to be a game object
"""
def readScheduleCSV(scheduleCSV, teams):
    with open(scheduleCSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            d = row[0]
            year = int(d[6:])
            month = int(d[3:5])
            day = int(d[:2])
            dateObj = date(year, month, day)
            homeTeam = row[1]
            awayTeam = row[2]
            teams[homeTeam].schedule.append(Game(dateObj, teams[awayTeam], True))
            teams[awayTeam].schedule.append(Game(dateObj, teams[homeTeam], False))

    return True

def getCalendarCSV(scheduleCSV):
    with open(scheduleCSV, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        calendar = {}
        for row in reader:
            d = row[0]
            year = int(d[6:])
            month = int(d[3:5])
            day = int(d[:2])
            dateObj = date(year, month, day)
            if dateObj not in calendar:
                calendar[dateObj] = False

    return calendar

def calculateDistances(teams):
    distances = defaultdict(dict)
    for t1 in teams.keys():
        for t2 in teams.keys():
            if t1 == t2:
                distances[t1][t2] = 0
            else:
                distances[t1][t2] = latLongDistance(teams[t1].location, teams[t2].location)
    return distances

def totalBackToBacks(teams):
    btb = 0
    for team in teams.values():
        btb += team.backToBacks()
    return btb

def flipCoin(p):
    r = random.random()
    return r < p

# Return a new schedule list sorted by date
def sortSchedule(schedule):
    s = sorted(schedule, key=lambda game: game.date)
    return s
