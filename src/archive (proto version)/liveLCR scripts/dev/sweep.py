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



style.use("fivethirtyeight")
fig = plt.figure()
ax = fig.add_subplot(111)

freqRange = np.linspace(48, 50.0, 100)
#start connection
#create device instance
meter = dsmutil.LCRMeter()
#clear buffer, and set timeout
meter.comms.clear()
meter.comms.timeout = 5000 #5s

# call animation
fig.show()
#for freq in freqRange:
#meter.data.freq = freq
meter.comms.write(f"FREQ {48.25*(1e3)}")
for i in range(100):
    sleep(0.01)
    #meter.data.cap.append(meter.comms.query("FETC?").rstrip().split(",")[0])
    print(meter.comms.query("FETC?").rstrip().split(",")[0])
