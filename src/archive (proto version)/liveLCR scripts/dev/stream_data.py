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

#start connection
#create device instance
meter = dsmutil.LCRMeter()
#clear buffer, and set timeout
meter.comms.clear()
meter.comms.timeout = 5000 #5s

#while loop
while True:
    data = meter.comms.query("FETC?").rstrip().split(",")
    print(f"Cp: {data[0]}       D:{data[1]}")
    sleep(0.1)
