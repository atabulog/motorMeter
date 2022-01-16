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
           All program errors will report to the local error log for debugging.
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


def write_summary(meter, sheet="Sweep"):
    """Writes summary row to 'Sweep' sheet
    Args:
        meter (LCRMeter): meter connection referenced.
    Returns:
        None.
    """
    #create summary sheet ref and start row count at 17
    sumSheet = meter.data.wb.Sheets[sheet]
    row = 17
    #step through row numbers until empty value found
    while sumSheet.Range(f"B{row}").Value != None:
        row += 1
    #write test settings to empty row
    sumSheet.Range(f"B{row}").Value = argv[1]
    sumSheet.Range(f"C{row}").Value = meter.data.primary
    sumSheet.Range(f"D{row}").Value = meter.data.secondary
    sumSheet.Range(f"E{row}").Value = meter.data.level
    sumSheet.Range(f"F{row}").Value = meter.data.start
    sumSheet.Range(f"G{row}").Value = meter.data.stop
    sumSheet.Range(f"H{row}").Value = meter.data.step
    sumSheet.Range(f"I{row}").Value = meter.data.dwell
    #save changes
    meter.data.wb.Save()


def to_log(msg):
    """ Writes given message to exec_log.txt file in current working directory.
    Args:
        msg (str): message to write.
    Returns:
        None.
    """
    with open(f"{getcwd()}\\exec_log.txt", "a+") as f:
        t = time()
        dt = datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M:%S")
        f.write(dt+"\n" + msg + "\n\n")
        f.close()

if __name__ == '__main__':
    #clear any existing log
    logPath = f"{getcwd()}\\exec_log.txt"
    if path.isfile(logPath):
        remove(logPath)

    #init meter object
    meter = dsmutil.LCRMeter(excelPath=argv[2])
    to_log("meter initiated.")

    #Set meter settings
    config_meter(meter=meter)
    to_log("meter configuration set.")

    #set loop variables
    range = np.arange(meter.data.start, meter.data.stop+meter.data.step,
                      meter.data.step)
    data = list()

    #execute test routine
    to_log("Starting loop.")
    for freq in range:
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

    #format data to df
    to_log("Formatting data.")
    meter.data.df = pd.DataFrame(data=data,
                                 columns=["Frequency", "Primary", "Secondary"])

    #create new excel sheet and push data from df to worksheet
    to_log("writing data.")
    dsmutil.excel.write_sheet(wb=meter.data.wb, data=meter.data.df,
                              sheetname=argv[1])

    #write new summary line to "Sweep" sheet
    write_summary(meter=meter)
