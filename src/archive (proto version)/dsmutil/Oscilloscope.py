# -*- coding: utf-8 -*-
"""
Author: Austin Tabulog
Date: 09/08/2021
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Keysight oscilloscope object for interaction through keysight serial API.
"""

#imports
from visa import ResourceManager
from pandas import DataFrame
from enum import Enum
from numpy import array, arange


class ConnectionError(Exception):
    """Exception raised for connection errors."""
    DEFAULT_MESSAGE = "Could not establish connection to oscilloscope."
    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)

class PreambleError(Exception):
    """Exception raised for connection errors."""
    DEFAULT_MESSAGE = "Could not establish data packet preamble."
    def __init__(self, message=DEFAULT_MESSAGE):
        super().__init__(message)

class Oscilloscope(object):
    """docstring for Oscilloscope."""
    #general params
    __MANUF_ID = "AGILENT TECHNOLOGIES"
    __DEVICE_LIST = ["DSO-X"]
    __DEFAULT_TIMEOUT = 3000 #ms
    __DEFAULT_DATA_POINTS = 5000
    __PREAMBLE_START = 4
    __CHANNELS = (1, 2, 3, 4)
    #queries
    __IDN_QUERY = "*IDN?"
    __QUERY_PREAMBLE = ":WAV:PRE?"
    #messages
    __INVALID_CHANNEL_MSG = "ERROR: INVALID CHANNEL GIVEN"

    def __init__(self, timeout=__DEFAULT_TIMEOUT, dataPoints=__DEFAULT_DATA_POINTS):
        """Initalizer for Oscilloscope object
        Args:
            timeout (int): time to wait before timeout in ms.
        Returns:
            None.
        """
        #default variables
        self.timeout = timeout #timeout in ms
        self.id = None
        self.comms = None
        self.response = list()
        self.binResponse = None
        self.dataPoints = dataPoints
        self.data = {"xAxis": list(),
                     1: list(),
                     2: list(),
                     3: list(),
                     4: list(),
                     }
        self.preamble = {"xIncr": 0,
                         "xOrigin": 0,
                         "xRef": 0,
                         "yIncr": 0,
                         "yOrigin": 0,
                         "yRef": 0}

        #connect to scope resource
        self.connect()
        #HACK: For some ungodly reason, the preamble must be called before it can be updated?
        # because of this, __set_preamble is called twice on purpose.
        self.query(":WAV:POIN?")
        self.__config_dataRead()
        self.__set_preamble()

    def connect(self):
        """Establish communication with oscilloscope.
        Args:
            None.
        Return:
            None.
        """
        # create visa resource manager and iterate through available resources
        rm = ResourceManager()
        for resource in rm.list_resources():
            #ignore all TCPIP connections
            if "TCPIP" not in resource:
                #connect to device and check device identity
                dev = rm.open_resource(resource)
                try:
                    resp = dev.query(self.__IDN_QUERY).lstrip().rstrip().split(",")
                    #if proper manufacturer ID
                    if resp[0] == self.__MANUF_ID:
                        #if proper device name
                        for deviceName in self.__DEVICE_LIST:
                            if deviceName in resp[1]:
                                #save connection and ID
                                self.comms = dev
                                self.id = resp
                                break
                except:
                    pass

        #throw error if no device could be connected
        if self.comms == None:
            raise ConnectionError()


    def disconnect(self):
        """Disconnect communication with oscilloscope.
        Args:
            None.
        Return:
            None.
        """
        self.comms = None
        self.id = None

    def __config_dataRead(self):
        """Configrues data presentation from device.
        Args:
            None.
        Returns:
            None.
        """
        #set timeout
        self.comms.timeout = self.timeout
        #set point count and mode
        self.write(":WAV:POIN:MODE NORM")
        #format wave data for export
        self.write(":WAV:FORM WORD")
        self.write(":WAV:BYT LSBF")
        self.write(":WAV:UNS 0")
        self.write(f":WAV:POIN 5000")


    def write(self, msg):
        """Send given command to resource without response.
        Args:
            msg (str): command to send to resource.
        Returns:
            None.
        """
        self.comms.clear()
        self.comms.write(msg)


    def query(self, msg):
        """Send given message to resource and store response.
        Args:
            msg (str): query to send to resource.
        Returns:
            None.
        """
        #flush buffer and write out query
        self.comms.clear()
        #store formatted response
        self.response = self.comms.query(msg)

    def fetch_channelData(self, channel):
        """saves current data on screen for given channel to data dictionary.
        Args:
            Channel (int): target channel from 1 to 4.
        Returns:
            None.
        """
        #only send query if valid channel given
        if channel in self.__CHANNELS:
            #set wave channel and response format
            self.write(f":WAV:SOUR CHAN{channel}")
            self.write(":WAV:FORM: word")
            #clear comms and retrieve channel data
            self.comms.clear()
            self.binResponse = array(
                            self.comms.query_binary_values(":WAV:DATA?", "h", False),
                            dtype=float)
            #scale data based on preamble
            self.binResponse = self.binResponse*self.preamble["yIncr"] + self.preamble["yOrigin"]
            #save data to proper data channel
            self.data[channel] = self.binResponse.tolist()
        else:
            print(self.__INVALID_CHANNEL_MSG)

    def __set_preamble(self):
        """Get the preamble from the scope and set for data reading.
        Args:
            None.
        Returns:
            None.
        Does:
            Sets preamble variables for binary message decoding.
        """
        #get preamble from device and format as intended
        try:
            self.query(self.__QUERY_PREAMBLE)
            self.response = self.response.lstrip().rstrip().split(",")
            #loop through preamble dict and store values from response
            i = self.__PREAMBLE_START
            for k in self.preamble.keys():
                self.preamble[k] = float(self.response[i])
                i+=1
            #generate x-axis data from preamble
            self.data["xAxis"] = arange(self.preamble["xOrigin"],
                           self.preamble["xOrigin"] + self.dataPoints*self.preamble["xIncr"],
                           self.preamble["xIncr"]).tolist()
        except:
            raise PreambleError()
