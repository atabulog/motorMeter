"""
Author: Austin Tabulog
Date: 02/18/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: fetch most recent zfit solution parameters and push to db.
"""

#imports
import dsmutil
import winreg
from subprocess import check_output
import pandas as pd
from sys import argv
from os import path

#ripped function from zfit to get last data file information
# REGISTRY ACCESS ==========================================================================
REG_PATH = r"SOFTWARE\ZFitDevel\Settings"
def set_reg(name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False

#constants
homeDir = "\\\\DSMDC\\itar\\DEM17-01\\Data Experimental\\LCR testing\\"
zfitDir = homeDir + "Zfit\\"
dataDir = homeDir + "data\\"
testDir = homeDir + path.splitext(path.basename(argv[1]))[0] + "\\"
zfitApp = zfitDir + "Zfit.pyw"
paramsFile = zfitDir + "params.csv"

#user specifies datafile
try:
    filepath, filename = dsmutil.selectFile(initialdir=testDir,
                                            extension="*.csv")
except:
    filepath, filename = dsmutil.selectFile(initialdir=dataDir,
                                            extension="*.csv")
#set zFit registry to open selected file
set_reg(name="DataFilename", value=filepath)
#launch zfit from command line and wait until closed
check_output(zfitApp, shell=True)


#init meter object to access correct data file
data = dsmutil.LCR_SweepData(excelPath=argv[1])
#write values to excel file
sumSheet = data.wb.Sheets["Sweep"]
#iterate on rows until empty row
row = 17
while sumSheet.Range(f"B{row}").Value != None:
    # if row contains fitted filename
    if sumSheet.Range(f"B{row}").Value == filename:
        break
    row += 1


#grab values from params.csv
paramsDf = pd.read_csv(filepath_or_buffer=paramsFile, sep=",", index_col=0)

#format values into proper units
#zfit always solves with values in base units, but I don't always show in base
Cd = float(str(paramsDf.loc["Cd"].values[0] * 10**9)) #F 2 nF
Rd = float(str(paramsDf.loc["Rd"].values[0]))
Lm = float(str(paramsDf.loc["Lm"].values[0] * 10**3)) #H 2 mH
Ro = float(str(paramsDf.loc["Ro"].values[0]))
Cm = float(str(paramsDf.loc["Cm"].values[0] * 10**9)) #F 2 nF

#write param values
sumSheet.Range(f"M{row}").Value = Cd
sumSheet.Range(f"N{row}").Value = Rd
sumSheet.Range(f"O{row}").Value = Lm
sumSheet.Range(f"P{row}").Value = Ro
sumSheet.Range(f"Q{row}").Value = Cm
#added to accomodate models using the rotor also
try:
    Ck = float(str(paramsDf.loc["Ck"].values[0]))
    Lk = float(str(paramsDf.loc["Lk"].values[0] * 10**3)) #H to mH

    sumSheet.Range(f"R{row}").Value = Ck
    sumSheet.Range(f"S{row}").Value = Lk
except:
    sumSheet.Range(f"R{row}").Value = 0
    sumSheet.Range(f"S{row}").Value = 0
