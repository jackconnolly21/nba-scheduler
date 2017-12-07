import util
from scheduler import Scheduler, Team, Game
from datetime import date
import pickle
import copy
import random
import csv
from math import e, log
import os
import numpy as np
import matplotlib.pyplot as plt


dates = Counter()
with open('270.txt', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        d = row[0]
        year = int(d[:4])
        month = int(d[5:7])
        day = int(d[8:])
        dateObj = date(year, month, day)
        dates[dateObj] += 1

dates = sorted(dates)
print dates
