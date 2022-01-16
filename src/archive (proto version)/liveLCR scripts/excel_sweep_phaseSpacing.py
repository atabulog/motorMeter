"""
Author: Austin Tabulog
Date: 01/16/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Execute sweep called by excel sheet. Return data as a new test sheet.
           ONLY WORKS FOR TEST PARAMETER STYLE WORKBOOKS.
"""

#imports
import dsmutil
from sys import argv
from os import getcwd, path, remove
from time import sleep, time
from datetime import datetime
import numpy as np
import pandas as pd


#local functions
def config_meter(meter):
    """ Configure meter settings based on excel file inputs.
    Args:
        meter (LCRMeter): meter object holding connection.
    Returns:
        None.
    """
    # set mesurement function
    try:
        meter.comms.write(
            f"MEAS:FUNC {meter.data.primary.upper()}{meter.data.secondary.upper()}")
    except UnicodeEncodeError:
        #convert secondary meas to "TH" as only theta will be thrown here.
        meter.data.secondary = "TH"
        meter.comms.write(
            f"MEAS:FUNC {meter.data.primary.upper()}{meter.data.secondary.upper()}")


    sleep(0.1)
    #set measurement level
    meter.comms.write(f"LEV:AC {meter.data.level}")
    sleep(0.1)
    meter.comms.write("MEAS:SPEE 2")
    sleep(0.1)


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


if __name__ == '__main__':
    #clear any existing log
    logPath = f"{getcwd()}\\exec_log.txt"
    if path.isfile(logPath):
        remove(logPath)

    #init meter object
    meter = dsmutil.LCRMeter(excelPath=argv[2], idPhrase="B&K Precision")
    meter.data.to_log("meter initiated.")

    #Set meter settings
    config_meter(meter=meter)
    meter.data.to_log("meter configuration set.")

    #set loop variables
    data = list()
    testID = str(meter.data.motorID) + " " + meter.data.channel + " " + argv[1]
    #execute test routine
    meter.data.to_log("Starting loop.")
    freq = meter.data.start

    while freq < meter.data.stop:
        #set frequency
        meter.comms.write(f"FREQ {freq}")
        #wait for update
        sleep(meter.data.dwell)

        #read current data and separate unit from value
        vals = meter.comms.query("FETC?").rstrip().split(",")
        prim_val = float(vals[0].lstrip().rstrip().split(" ")[0])
        prim_unit = vals[0].lstrip().rstrip().split(" ")[-1]
        sec_val = float(vals[1].lstrip().rstrip().split(" ")[0])
        sec_unit = vals[1].lstrip().rstrip().split(" ")[-1]

        #format all values to same base unit
        prim_val = dsmutil.scale_unit(
                    given=prim_unit, desired=meter.data.unit_primary)*prim_val
        #append data in proper format
        try:
            data.append([freq, float(prim_val), float(sec_val)])
        except:
            data.append([freq, prim_val, sec_val])

        #Update frequency value
        meter.data.step = phaseSampling(sec_val)
        freq += meter.data.step

        if freq > meter.data.stop:
            freq = meter.data.stop


    #format data to df
    meter.data.to_log("Formatting data.")
    meter.data.df = pd.DataFrame(data=data,
                                 columns=["Frequency", "Primary", "Secondary"])

    #create new excel sheet and push data from df to worksheet
    meter.data.to_log("writing data.")
    dsmutil.excel.write_sheet(wb=meter.data.wb, data=meter.data.df,
                              sheetname=testID)

    #write new summary line to "Sweep" sheet
    meter.data.write_summary(argv[1])
