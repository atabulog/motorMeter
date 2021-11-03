"""
Author: Austin Tabulog
Date: 01/09/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Live data stream from BK Precision 891.
"""

#imports
import dsmutil
import pandas as pd
from time import sleep
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

#start connection
#create device instance
meter = dsmutil.LCRMeter()
#clear buffer, and set timeout
meter.comms.clear()
meter.comms.timeout = 5000 #5s

# set freq range
numPoints = 100
freqRange = np.linspace(48,49,numPoints)
i = 0
data = list()
for freq in freqRange:
    meter.comms.write(f"FREQ {freq*(1e3)}")
    sleep(0.1)
    data.append([freq*1e3] + meter.comms.query("FETC?").rstrip().split(","))
    dsmutil.progressBar(iteration=i, total=numPoints)
    i += 1

import pdb; pdb.set_trace()
dataDf = pd.DataFrame(data=data, columns=["Frequency", "Capacitance", "DF"])
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(df.Frequency, df.Capacitance, "-")
plt.show()
