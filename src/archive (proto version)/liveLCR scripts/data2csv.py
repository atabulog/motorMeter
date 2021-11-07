# -*- coding: utf-8 -*-
"""
Author: Austin Tabulog
Date: 01/21/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Script to convert all data sheets in an LCR tester excel file to
           independent .csv files in a folder named given file name.
"""
import dsmutil
import pandas as pd
from os import mkdir, path
from sys import argv

#prompt for desired file
filepath = argv[1]
filename = path.splitext(path.basename(filepath))[0]
#get sheet names in given file and remove first name
sheetnames = pd.ExcelFile(filepath).sheet_names[1:]

#create path to new folder
saveDirPath = path.dirname(filepath)+"\\"+filename

#create folder in same directory with filename as foldername
try:
    mkdir(saveDirPath)
except FileExistsError:
    pass

#for sheet if sheet names
for sheet in sheetnames:
    if not path.isfile(saveDirPath+"\\"+sheet+".csv"):
        # import data to dataFrame
        df = pd.read_excel(io=filepath, sheet_name=sheet)
        df.columns = ["Frequency", "Primary", "secondary"]
        # convert data to labeled CSV with no index and save as *.csv
        df.to_csv(path_or_buf=saveDirPath+"\\"+sheet+".csv", index=False)
