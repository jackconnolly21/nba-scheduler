import util
from scheduler import Scheduler
from localSearch import hillClimbing, simulatedAnnealing
import pickle
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
    hcCost = hillClimbing(hcsch, 100000)
    saCost = simulatedAnnealing(sasch, times=100000)

    HCtraces.append(hcsch.trace)
    SAtraces.append(sasch.trace)

hcAvg = []
hcStd = []
saAvg = []
saStd = []
for i in xrange(len(HCtraces[0])):
    hc = []
    sa = []
    for trial in xrange(len(HCtraces)):
        hc.append(HCtraces[trial][i])
        sa.append(SAtraces[trial][i])
    hcAvg.append(sum(hc)/len(hc))
    saAvg.append(sum(sa)/len(sa))
    hcStd.append(util.standardDev(hc))
    saStd.append(util.standardDev(sa))

pickle.dump((hcAvg, hcStd), open("hc.txt", 'wb'))
pickle.dump((saAvg, saStd), open("sa.txt", 'wb'))

iterations = range(len(hcAvg))

plt.figure()
plt.errorbar(iterations, hcAvg, yerr=hcStd, ecolor='c', label="Hill Climbing")
plt.errorbar(iterations, saAvg, yerr=saStd, ecolor='y', label="Simulated Annealing")

plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
       ncol=2, mode="expand", borderaxespad=0.)
plt.show()
