# -*- coding: utf-8 -*-
"""
Author: Austin Tabulog
Date: 01/08/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Object to describe keysight oscilloscope communication routine
           through visa library.
"""
#imports
import dsmutil
import numpy as np
import pandas as pd
import visa
from sys import exit
from time import sleep
from re import match
from os import getcwd
from time import time
from datetime import datetime

"""data containing objects"""
class deviceData(object):
    """docstring for LCRData."""

    def __init__(self, excelPath=None):
        self.df = None
        self.meas_primary = None
        self.meas_secondary = None


class LCR_SweepData(deviceData):
    """docstring for LCR."""

    def __init__(self, excelPath):
        #init parent
        super().__init__(self)
        #create excel instance and pull data from excel sheet
        self.wb = dsmutil.excel.create_instance(excelPath)
        sweepDf = pd.read_excel(excelPath, sheet_name="Sweep", nrows=8,
                               usecols=[1,2,3])
        testDf = pd.read_excel(excelPath, sheet_name="Sweep", nrows=4,
                               usecols=[5,6])

        #reformat dfs to have proper columns
        sweepDf.columns = sweepDf.iloc[0]
        sweepDf = sweepDf.drop(sweepDf.index[0])
        testDf.columns = testDf.iloc[0]
        testDf = testDf.drop(testDf.index[0])

        #set object parameters from sheet data
        self.primary = sweepDf.value.values[0]
        self.unit_primary = sweepDf.Units.values[0]
        self.secondary = sweepDf.value.values[1]
        self.level = sweepDf.value.values[2]
        self.start = sweepDf.value.values[3]
        self.stop = sweepDf.value.values[4]
        self.step = sweepDf.value.values[5]
        self.dwell = sweepDf.value.values[6]
        try: #if test parameter table exists in file
            self.motorID = testDf.value.values[0]
            self.manufacturer = testDf.value.values[1]
            self.channel = testDf.value.values[2]
        except AttributeError: #if not
            self.motorID = None
            self.manufacturer = None
            self.channel = None

    def write_summary(self, dataSheet, writeSheet="Sweep"):
        """Writes summary row to 'Sweep' sheet
        Args:
            meter (LCRMeter): meter connection referenced.
        Returns:
            None.
        """
        #create testID
        testID = str(self.motorID) + " " + self.channel + " " + dataSheet
        #create summary sheet ref and start row count at 17
        sumSheet = self.wb.Sheets[writeSheet]
        #get resonant frequency data
        self.resFreq = int(self.df.Frequency[self.df.Primary == min(self.df.Primary.values)].values[0])
        self.antiresFreq = int(self.df.Frequency[self.df.Primary == max(self.df.Primary.values)].values[0])
        #loop variables
        row = 17
        #step through row numbers until empty value found
        while sumSheet.Range(f"B{row}").Value != None:
            row += 1
        #write test settings to empty row
        sumSheet.Range(f"B{row}").Value = testID
        sumSheet.Range(f"C{row}").Value = self.motorID
        sumSheet.Range(f"D{row}").Value = self.manufacturer
        sumSheet.Range(f"E{row}").Value = self.channel
        sumSheet.Range(f"F{row}").Value = self.primary
        sumSheet.Range(f"G{row}").Value = self.secondary
        sumSheet.Range(f"H{row}").Value = self.level
        sumSheet.Range(f"I{row}").Value = self.start
        sumSheet.Range(f"J{row}").Value = self.stop
        sumSheet.Range(f"K{row}").Value = self.step
        sumSheet.Range(f"L{row}").Value = self.dwell
        sumSheet.Range(f"T{row}").Value = self.resFreq
        sumSheet.Range(f"U{row}").Value = self.antiresFreq
        #save changes
        self.wb.Save()


    def to_log(self, msg):
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


"""visa device objects"""
class VisaDevice(object):
    """docstring for VisaDevice."""

    def __init__(self, excelPath=None, idPhrase=None):
        # set parameters
        self.id = list()
        self.idPhrase = idPhrase
        self.comms = None
        self.data = None

        #connect comms
        self.connect_comms()
        # if no scope was detected, throw error
        if self.comms == None:
            raise IOError("Could not establish connection to a device.")


    def connect_comms(self):
        """ Set self.comms.
        Args:
            None.
        Does:
            if scope found sets self.comms to scope.
        """
        # list of types of devices to ignore
        ignoreList = ["TCPIP"]
        # set self.comms to a visa.resource if successful IDN query
        # create visa resource manager
        rm = visa.ResourceManager()
        # create list of devices
        deviceList = list(rm.list_resources())
        for device in deviceList:
                for ignore in ignoreList:
                    if ignore not in device:
                        # establish communication routine with device
                        dev = rm.open_resource(device)
                        if self.check_comms(dev):
                            tempID = dev.query("*IDN?").strip("\n")
                            if self.idPhrase == None:
                                self.id = tempID
                                self.comms = dev
                                return
                            elif match(f"(?i){self.idPhrase}", tempID) != None:
                                self.id = tempID
                                self.comms = dev
                                return


    def liveLoop(self, event):
        """Null function acts a listener for animation loop.
        Note:
            animation is a scope method to ease getting the data to the
            animation artist.
        """
        # check comms
        if self.check_comms():
            self.connection = True
        # else try to re-establish comms
        else:
            for i in range(5):
                print(f"Lost connection, trying to re-establish {i}/5")
                self.connect_comms()
                if self.check_comms():
                    print(f"Connect re=established.")
                    break
            if not self.check_comms():
                print("Comms could not be re-established:")
                print("Terminating program")
                exit(0)


    def check_comms(self, dev=None):
        """ Check if self.comms is communicating properly with hardware.
        Args:
            [OPTIONAL]
            dev (visa.resource): device to use for check.
        Does:
            Returns true if successful response, else returns false.
        """
        try:
            # if no device given, use self.comms
            if dev == None:
                # query comms and format response to list
                res = self.comms.query("*IDN?").split(",")
            else:
                # query comms and format response to list
                res = dev.query("*IDN?").split(",")
            return True

        except:
            return False



class LCRMeter(VisaDevice):
    """docstring for LCRMeter."""

    def __init__(self, excelPath=None, idPhrase=None):
        self.excelPath = excelPath
        self.idPhrase = idPhrase
        super().__init__(self, idPhrase=self.idPhrase)
        if excelPath == None:
            self.data = deviceData()
        else:
            self.data = LCR_SweepData(self.excelPath)


    def read_current(self):
        data = self.comms.query("FETC?")
        return data


    def read_all(self):
        values = list()
        step = int(self.comms.query("SWEE:STEP?").rstrip())
        for i in range(int(300/step)-1):
            self.comms.write(f"SWEE:POI {i}")
            read = self.comms.query("SWEE:DATA?").rstrip().split(",")
            values.append([float(read[0]), float(read[1])])
            dsmutil.progressBar(iteration=i+2, total=int(300/step))
            sleep(0.1)

        self.comms.clear()
        self.data.sweepDf = pd.DataFrame(data=values, index=None,
                                        columns=["Frequency", "Value"])
