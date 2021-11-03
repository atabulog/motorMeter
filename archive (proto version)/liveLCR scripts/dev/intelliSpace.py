"""
Author: Austin Tabulog
Date: 02/04/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Script to test different sampling methods for given datasets.
"""

#imports
from csv import reader
from matplotlib import pyplot as plt
import pandas as pd

#sampling functions
def slopeSampling(value, prev_val):
    pass

def phaseSampling(value):
    sparseThresh = -87
    sparseRate = 50

    normalThresh = -80
    normalRate = 20
    fineRate = 10

    if value > sparseThresh:
        if value > normalThresh:
            samplingRate = fineRate
        else:
            samplingRate = normalRate
    else:
        samplingRate = sparseRate

    return samplingRate


#main
if __name__ == '__main__':
    #constants
    path = "C:\\Users\\atabulog\\Desktop\\Rotor comparison - Copy.csv"
    #create saved data information
    readData = list()
    #plotting variables
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(f"Phase sampling data")
    ax.set_xlabel('Frequency')
    ax.set_ylabel('impedance, Z [\u03A9]')
    #loop starting values
    counter = 0
    prevRate = 50
    targetFreq = 0
    #go through data as if it were a data stream
    with open(path) as csv_file:
        #import sample data
        streamData = reader(path, delimiter=",")
        for row in csv_file:
            #skip first line
            if counter != 0:
                currentFreq = int(row.split(",")[0])
                amp = float(row.split(",")[1])
                phase = float(row.split(",")[2].rstrip())
                samplingRate = phaseSampling(phase)

                if counter == 1:
                    targetFreq = currentFreq

                if currentFreq == targetFreq:
                    readData.append([currentFreq, amp, phase])
                    targetFreq += samplingRate

            counter += 1

        #format data and plot results
        fileDf = pd.read_csv(path, delimiter=",", dtype="float")
        df = pd.DataFrame(data=readData, columns=["Freq", "Amp", "Phase"])
        plt.grid()
        plt.plot(fileDf.Freq, fileDf.Amp, "-")
        plt.plot(df.Freq, df.Amp, "ko")
        import pdb; pdb.set_trace()
        plt.show()
