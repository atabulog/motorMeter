# -*- coding: utf-8 -*-
"""
Author: Austin Tabulog
Date: 01/11/2021
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Serial device base class and serial specific device implementations.
"""
#imports
from serial import Serial
from dsmutil import serialObjects


class MachineSerial(object):
    """Baseclass object desribing machine serial message according to ARR 20-01
       Tactical controller ICD.
    """
    def __init__(self, port, baudrate, bytesize, parity, stopbits, timeout, printResp, packet):
        #initalize parameters
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.printResp = printResp
        #self.packet = packet

        #establish serial connection
        self.ser = Serial(port=self.port, baudrate=self.baudrate,
                             bytesize=self.bytesize, parity=self.parity,
                             stopbits=self.stopbits, timeout=self.timeout)





    def write(self):
        """Function to send command to device and return response.
        Args:
            packet (str): unformatted packet to be sent to device.
        Returns:
            None
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        self.ser.write(self.packet.sendBuff)
        self.responseLoop()


    def responseLoop(self):
        """Function stores response from serial device.
        Args:
            None.
        Returns:
            None.
        Note:Function prints out serial response if print enabled
        """
        respList = list()
        resp = self.ser.read()

        while resp != "":
            #append ASCII formatted byte to response
            respList.append(resp.decode("ASCII"))
            resp = self.ser.read()

        self.response = "".join(respList)
        if self.prinResp:
            print(self.response)
