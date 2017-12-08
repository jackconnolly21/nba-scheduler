import util
from scheduler import Scheduler, Team, Game
from datetime import date
from localSearch import hillClimbing, simulatedAnnealing
import pickle
import copy
import random
import csv
from math import e, log
import os
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

s = Scheduler()
s.randomStart()
s.removeTriples()

HCtraces = []
SAtraces = []

for i in xrange(20):
    hcsch = deepcopy(s)
    sasch = deepcopy(s)
    hcCost = hillClimbing(hcsch, 100)
    saCost = simulatedAnnealing(sasch, times=100)

    HCtraces.append(hcsch.trace)
    SAtraces.append(sasch.trace)

hcAvg = []
saAvg = []
for i in xrange(len(HCtraces[0])):
    hc = []
    sa = []
    for trial in xrange(len(HCtraces)):
        hc.append(HCtraces[trial][i])
        sa.append(SAtraces[trial][i])
    hcAvg.append(sum(hc)/len(hc))
    saAvg.append(sum(sa)/len(sa))

pickle.dump(hcAvg, open("hc.txt", 'wb'))
pickle.dump(saAvg, open("sa.txt", 'wb'))

plt.plot(hcAvg, label="Hill Climbing")
plt.plot(saAvg, label="Simulated Annealing")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)
plt.show()
