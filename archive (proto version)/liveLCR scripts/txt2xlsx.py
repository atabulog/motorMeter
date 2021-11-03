"""
Author: Austin Tabulog
Date: 01/09/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Convert exported *.txt sweep files in given folder to excel workbook.
"""
#imports
import re
import dsmutil
import numpy as np
import pandas as pd
from os import path, listdir
from sys import argv


#functions
def format_header(line):
    """Parse header formatted data into list of lists with label, value pairs.
    Args:
        line (str): line data from file
    Returns:
        header (list): list of lists containing header data.
    """
    header = None
    return header


def format_data(line):
    """Parse table formatted data into list of lists with label, value pairs.
    Args:
        line (str): line data from file
    Returns:
        data (list): list of lists containing table data.
    """
    data = None
    return data

def scale_unit(given, desired, symbol="F"):
    """Convert scale factor of similar unit.
    Args:
        given (str): given unit type.
        desired (str): desired unit type.
    [OPTIONAL]
        symbol (str): base unit defaults to Farads 'F'.
    Returns:
        scale (float): scale factor to multiply value by.
    """
    prefix = [["G", 10e9],
              ["M", 10e6],
              ["k", 10e3],
              ["h", 10e2],
              ["da", 10e1],
              ["", 1],
              ["d", 10e-1],
              ["c", 10e-2],
              ["m", 10e-3],
              ["u", 10e-6],
              ["n", 10e-9],
              ["p", 10e-12],
              ["f", 10e-15]]
    unitDf = pd.DataFrame(data=prefix, columns=["Prefix", "Scale"])
    try:
        givenScale = unitDf[unitDf.Prefix == given.strip(symbol)].Scale.values[0]
    except:
        raise KeyError(f"Unit factor {given.strip(symbol)} not recognized.")

    try:
        desiredScale = unitDf[unitDf.Prefix == desired.strip(symbol)].Scale.values[0]
    except:
        raise KeyError(f"Unit factor {desired.strip(symbol)} not recognized.")

    return float(givenScale/desiredScale)


#main
if __name__ == '__main__':
    # create excel instance for data storage
    # request data file directory
    folderPath, _ = dsmutil.selectFolder(title="Select data directory.")
    if folderPath == "\\":
        exit(0)
    # call instance and set configs
    excelWb = dsmutil.excel.create_instance()

    #loop variables
    header = list()


    # for text file in folder
    fileCounter = 0
    for file in listdir(folderPath):
        table = list()
        if path.splitext(file)[1] == ".TXT":
            #get filename
            filename = path.splitext(file)[0]
            #open file and read line by line
            with open(folderPath+file, "r+") as f:
                counter = 0
                for line in f:
                    line = line.rstrip()
                    #skip first two lines
                    if counter < 2:
                        pass
                    # grab header data
                    elif counter < 12:
                        header.append("".join(line.split()).split(":"))

                    # grab table data
                    else:
                        lineList = line.split(":")
                        lineList = [x.lstrip().split() for x in lineList]
                        values = [int(lineList[0][0]),
                                  float(re.split("(\d+(?:\.\d+)?)", lineList[1][0])[1]),
                                  float(lineList[2][0])]
                        units = [None,
                                 re.split("(\d+(?:\.\d+)?)", lineList[1][0])[2],
                                 lineList[2][1]]

                        values[1] = scale_unit(given=units[1], desired="", symbol="Hz")*values[1]
                        values[2] = scale_unit(given=units[2], desired="n")*values[2]
                        table.append([a for b in zip(values, units) for a in b])
                    counter += 1
            #write header to worksheet

            #write table to worksheet
            tableDf = pd.DataFrame(data=table, columns=["Index", "Index-units", "Frequency", "Frequency-units", "Value", "Value-units"])
            tableDf = tableDf.drop("Index-units", axis=1)
            dsmutil.excel.write_sheet(wb=excelWb, data=tableDf, sheetname=filename)
            # save data file
            excelWb.sheets[0].Name = "Analysis"
        # progress bar
        fileCounter += 1
        dsmutil.progressBar(iteration=fileCounter,
                            total=len(listdir(folderPath)))
    # save file
    dsmutil.excel.save_instance(wb=excelWb, path=folderPath+argv[1])
