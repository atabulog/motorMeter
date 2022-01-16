"""
Author: Austin Tabulog
Date: 01/09/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Pull out Frequency and ending impedance data from RLC meter tests.
"""

#imports
import dsmutil
import pandas as pd
import numpy as np
from os import path

if __name__ == '__main__':
    #select excel file
    filepath, filename = dsmutil.selectFile(extension="*.xlsm")

    #create list of sheets in file
    sheetnames = pd.ExcelFile(filepath).sheet_names

    #remove first sheet from file sheet list
    sheetnames = sheetnames[1:]

    data = list()
    #for sheet in file
    for sheet in sheetnames:
        #import data from sheet
        df = pd.read_excel(io=filepath, sheet_name=sheet)
        #grab starting and ending impedance
        zStart = float(str(df.Primary.iloc[0])[0:6])
        zEnd = float(str(df.Primary.iloc[-1])[0:6])
        #grab frequency of lowest impedance - assume resonance
        resFreq = df.Frequency[df.Primary == min(df.Primary.values)].values[0]
        #grab frequency of highest impedance - assume anti-resonance
        antiFreq = df.Frequency[df.Primary == max(df.Primary.values)].values[0]
        #print formatted values
        data.append([sheet, zStart, zEnd, resFreq, antiFreq])
    df = pd.DataFrame(data=data, index=None)
    df.to_excel(r"C:\\Users\\atabulog\\Desktop\\temp.xlsx")
