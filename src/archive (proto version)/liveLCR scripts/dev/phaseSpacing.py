"""
Author: Austin Tabulog
Date: 02/04/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Dev function for sampling motor impedance curves based on phase data.
"""
import dsmutil

def run_sweep(start, stop, step):
    pass

#create sample distribution
sample_distrib = [10, 20, 50]
start = 46000
stop = 50000

#run coarse scan at distrib, max
coarseStep = max(sample_distrib)
data = run_sweep()

#create normalized phase data
normPhase = data/max(data)

if len(data) > 5:
    pass
elif len(data) <3:
    pass
else:
    pass


#set percentage limits for resampling
#find frequency thresholds for different limits
#resample between frequency thresholds
#order data in ascending frequency
