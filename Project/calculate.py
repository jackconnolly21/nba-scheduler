import csv
import util
from collections import defaultdict

teams = dict()
with open('teams.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        name = row[0]
        conference = row[1]
        division = row[2]
        lat = float(row[3])
        lng = float(row[4])
        teams[name] = (conference, division, (lat, lng))

distances = defaultdict(dict)
for t1 in teams.keys():
    for t2 in teams.keys():
        distances[t1][t2] = util.latLongDistance(teams[t1][2], teams[t2][2])
