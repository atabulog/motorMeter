# -*- coding: utf-8 -*-
"""
Author: Austin Tabulog
Date: 06/11/2020
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
from time import time_ns
from pandas import DataFrame
from difflib import ndiff
from time import sleep

#generic serial functions
def format_cr(command):
    """Function to format standard commands to binary with \n \r added.
    Args:
        command (str): command to device.
    Returns:
        binary version of command with CRLF appended.
    """
    return f"{command}\r".encode("utf-8")

def format_lf(command):
    """Function to format standard commands to binary with \n \r added.
    Args:
        command (str): command to device.
    Returns:
        binary version of command with CRLF appended.
    """
    return f"{command}\n".encode("utf-8")

def format_crlf(command):
    """Function to format standard commands to binary with \n \r added.
    Args:
        command (str): command to device.
    Returns:
        binary version of command with CRLF appended.
    """
    return f"{command}\n\r".encode("utf-8")


#serial baseclass
class SerialDevice(object):
    """baseclass for generic serial devices."""
    def reconnect(self):
        """ Function to reconnect or reset connection to serial device.
        Args:
            None.
        Returns:
            None.
        """
        self.ser = Serial(port=self.port, baudrate=self.baudrate,
                          bytesize=self.bytesize, parity=self.parity,
                          stopbits=self.stopbits, timeout=self.timeout)

    def close(self):
        """Function closes connection to serial device."""
        self.ser.close()


    def flush(self):
        """Function to flush all buffers for communication.
        Args:
            None.
        Returns:
            None.
        """
        self.ser.flushInput()
        self.ser.flushOutput()


    def write(self, command):
        """Function to send command to device and return response.
        Args:
            command (str): unformatted command to be sent to device.
        Returns:
            None
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        self.ser.write(format_crlf(command))
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
        resp = self.ser.readline().decode("ascii")

        #check numBytes in buffer and keep going if data is stored
        while self.ser.in_waiting > 0:
            #append newline to list and decode next line
            respList.append(resp)
            resp = self.ser.readline().decode("ascii")

        #set response and print if set to print
        self.response = "".join(respList)
        if self.printResp:
            print(self.response)

    def responseLoop_tabbed(self):
        """Function stores response from serial device.
        Args:
            None.
        Returns:
            None.
        Note:Function prints out serial response if print enabled
        """
        #timing variables
        startTime = time_ns()*1E-9
        newTime = startTime
        respList = list()
        resp = self.ser.readline().decode("ascii")

        while resp != "":
            #set response and print if set to print
            respList.append(resp)
            resp = self.ser.readline().decode("ascii")

        self.response = "".join(respList)
        if self.printResp:
            print("\t" + self.response)

    def write_varResponse(self, command, responseFunc):
        """Function sends command to device and returns using response function.
        Args:
            command (str): unformatted command to be sent to device.
        Returns:
            None
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        self.ser.write(command)
        responseFunc()

    def hexRespLoop(self):
        """Function stores response from serial device.
        Args:
            None.
        Returns:
            None.
        Note:Function prints out serial response if print enabled
        """
        #timing variables
        startTime = time_ns()*1E-9
        newTime = startTime
        respList = list()
        resp = self.ser.read()
        timeoutFlag = False
        prevData = False

        #run until exit condition occurrs
        while True:
            #if previous byte was not empty, but new byte is, end read
            if prevData and resp == b"":
                break
            #if timeout occurrs, end read
            elif newTime - startTime > self.timeout:
                timeoutFlag = True
                break
            #read data if not empty
            elif resp != b"":
                prevData = True
                respList.append(resp)

            #get new data and update time
            resp = self.ser.read()
            newTime = time_ns()*1E-9

        if timeoutFlag:
            #print timeout failure message
            print("TIMED OUT")

        else:
            #print out formatted hex message
            map_bin2hex = map(hex, map(ord, respList))
            self.response = list(map_bin2hex)
            if self.printResp:
                #print all hex vals
                print("\tREC:\t"+" ".join(x for x in self.response))


    def get_hexStr(self):
        """Return string of formatted hex characters in self.response.
        Args:
            None.
        Returns:
            string of formatted hex charactersfrom self.response.
        """
        hexStr = ""
        for hexByte in self.response:
            hexByte = hexByte.split("x")[1]
            if len(hexByte) == 1:
                hexStr+="0"+hexByte
            else:
                hexStr+=hexByte
        return hexStr.upper()


    def get_hexList(self, dataBytes=1):
        """Return list of formatted hex characters in self.response.
        Args:
            dataBytes (int): number of bytes to group together.
        Returns:
            list of formatted hex values grouped by bytes.
        """
        counter = 0
        hexList = list()
        sampleList = list()
        #go through response message excluding header information
        for hexByte in self.response[6:-1]:
            #strip 0x header and ensure leading zeros are not dropped
            hexByte = hexByte.split("x")[1]
            if len(hexByte) == 1:
                sampleList.append("0"+hexByte.upper())
            else:
                sampleList.append(hexByte.upper())

            #check if byteLength is met, and store to either list or string
            if counter == dataBytes-1:
                #reverse order of list and save as a string
                sampleList.reverse(); hexStr = "".join(sampleList)
                #write string into a 16 bit hex value and reset variables
                hexList.append(unpack("!i", bytearray.fromhex(hexStr))[0])
                sampleList = list()
                counter = 0
            else:
                counter += 1

        return hexList


#devices
class Korad(SerialDevice):
    """docstring for generic Korad powersupply."""

    def __init__(self, port, timeout, printResp):
        self.port = port
        self.baudrate = 9600
        self.bytesize = 8
        self.parity = "N"
        self.stopbits = 1
        self.timeout = timeout
        self.printResp = printResp
        self.response = None
        self.ser = Serial(port=self.port, baudrate=self.baudrate,
                             bytesize=self.bytesize, parity=self.parity,
                             stopbits=self.stopbits, timeout=self.timeout)


    def write(self, command):
        """Function to send command to device and return response.
        Args:
            command (str): command to be sent to device.
        Returns:
            None
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        self.ser.write(f"{command}".encode("utf-8"))
        self.responseLoop()

    def get_id(self):
        self.flush()
        self.ser.write(f"*IDN?".encode("utf-8"))
        self.responseLoop()

    def turn_on(self):
        self.write("OUT1")

    def turn_off(self):
        self.write("OUT0")


class KoradSingle(Korad):
    """Object for Korad single channel powersupply."""

    def __init__(self, port, timeout=0.1, printResp=False):
        super(KoradSingle, self).__init__(port, timeout, printResp)


    def get_voltage(self):
        self.write("VOUT1?")
        return float(self.response)


    def get_current(self):
        self.write("IOUT1?")
        return float(self.response)


class KoradDouble(Korad):
    """Object for Korad single channel powersupply."""

    def __init__(self, port, timeout=0.1, printResp=True):
        super(KoradDouble, self).__init__(port, timeout, printResp)


    def get_voltage(self, channel):
        self.write(f"VOUT{channel}?")


    def get_current(self, channel):
        self.write(f"IOUT{channel}?")

class BKPrecision891(SerialDevice):
    """Interaction object for BK Precision 891 LCR meter.
    Args:
        port (str): COMport for connection. ex: "COM1"
    Returns:
        None.
    Does:
        Creates serial connection to device and interaction oject with basic
        functions built in like a mini device API.
    """

    def __init__(self, port, timeout=0.1, printResp=True):
        self.port = port
        self.baudrate = 57600
        self.bytesize = 8
        self.parity = "N"
        self.stopbits = 1
        self.timeout = timeout
        self.printResp = printResp
        self.response = None
        self.primary = None
        self.primaryUnit = None
        self.secondary = None
        self.secondaryUnit = None
        self.ser = Serial(port=port, baudrate=57600, bytesize=8, parity="N",
                         stopbits=1, timeout=self.timeout)


    def __get_baseUnit(self, unit):
        """Set measurement channel units to baseUnits.
        Args:
            unit (str): measurement unit.
        Returns:
            baseUnit (str): the base unit.
        Note:
            base units are ohm, nF, mH, degrees.
        """
        #check if units are ohms
        if str(unit)[1:].lower() == "ohm":
            return "ohm"
        #check if capacitance measurement
        elif str(unit)[-1].upper() == "F":
            return "nF"
        #check if inductance measurement
        elif str(unit)[-1].upper() == "H":
            return "mH"
        elif str(unit).lower() == "th":
            return "th"
        else:
            print("ERROR: unknown unit.")
            return None


    def __scale_baseUnit(self, value, unit, channel):
        """Scale measured value to baseUnits.
        Args:
            value (float): value to scale.
            unit (str): unit value is in before scaling.
            channel (str): either 'primary' or 'secondary' for unit reference.
        Returns:
            scaledVal (float): value scaled to baseUnits.
        """
        #create unit dataFrame
        prefix = [["G", 1e9],
                  ["M", 1e6],
                  ["k", 1e3],
                  ["h", 1e1],
                  ["", 1],
                  ["d", 1e-1],
                  ["c", 1e-2],
                  ["m", 1e-3],
                  ["u", 1e-6],
                  ["n", 1e-9],
                  ["p", 1e-12],
                  ["f", 1e-15]]
        unitDf = DataFrame(data=prefix, columns=["Prefix", "Scale"])

        #if primary channel
        if channel.lower() == "primary":
            baseUnit = self.primaryUnit
        #else secondary channel
        else:
            baseUnit = self.secondaryUnit
        """THIS IS WHERE YOU LEFT OFF. WE ARE TRYING TO SCALE THE VALUE
           ACCORDING TO THE BASE UNIT.
        """
        #doesn't work:: prefix = "".join([s for i,s in enumerate(ndiff(baseUnit, unit))])


    def get_id(self):
        """Queries device for SCPI id, and returns results.
        Args:
            None.
        Returns:
            None.
        Note:
            response data gets saved to self.response.
        """
        self.flush()
        self.write("*IDN?")


    def get_meas(self, scaleVal=False):
        """Gets current measurement data and saves formatted data to self.primary
           and self.secondary.
        Args:
            None.
        Returns:
            None.
        Note:
            This function will not print out response from device.
        """
        #get measurement from device
        cmd = "FETC?"
        if self.printResp:
            self.printResp = False
            self.write(cmd)
            self.printResp = True
        else:
            self.write(cmd)

        #format response into primary and secondary values
        prim_val = float(self.response.split(",")[0].strip().split(" ")[0])
        prim_unit = str(self.response.split(",")[0].strip().split(" ")[-1])
        sec_val = float(self.response.split(",")[-1].strip().split(" ")[0])
        sec_unit = str(self.response.split(",")[-1].strip().split(" ")[-1])

        #scale values to base unit (ohm, nF, mH)
        self.primaryUnit = self.__get_baseUnit(unit=prim_unit)
        self.primary = self.__scale_baseUnit(value=prim_val, unit=prim_unit,
                                             channel="primary")


class DSM_Device(SerialDevice):
    """middle ground object for all DSM made serial controllers.
    Args:
        None.
    Returns:
        None.
    Does:
        Holder object for repeated functions for DSM hardware.
    """
    def __init__(self, port, baudrate=115200, bytesize=8, parity="N",
                 stopbits=1, timeout=0.1, printResp=True, machSer=False):
        self.port = port
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self.timeout = timeout
        self.printResp = printResp
        self.machSer = machSer
        self.response = None

        try:
            self.reconnect()
        except:
            self.ser = None


    def write(self, command, responseFunc=None):
        """Function to send command to device and return response.
        Args:
            command (str): command to be sent to device.
            responseFunc (function): funtion to decode machine serial response
                                     into human readable text
        Returns:
            None
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        if not self.machSer:
            self.ser.write(format_cr(command=command))
            self.responseLoop()
        else:
            self.ser.write(command)
            responseFunc(self)


class SpinTestDriver(DSM_Device):
    """ Interaction object for spin test driver.

    Args:
        port (str): COMport for connection. ex: "COM1".
        [timeout (float)]: Wait time before timeout in seconds.
        [printResp (bool)]: flag to print response or not.
    Returns:
        None.
    Does:
        Creates serial connection to device and interaction object with basic
        functions built in like a mini device API.
    """
    #object "GLOBALS"
    ENTRY_LEN = 6
    META_TABLE_LEN = 8
    DATA_TABLE_COLS_IDX = 9
    SPEED_DATA_COL = 5
    IDX_DATA_COL = 0
    MAX_IDX_DELTA = 1000
    MAX_SPEED_DELTA = 5
    BUFFER_SIZE = 256000

    def __init__(self, port, timeout=0.1, printResp=True):
        self.port = port
        self.timeout = timeout
        self.printResp = printResp
        self.response = None
        self.dataCapture = list()
        self.dataCapColumns = list()
        self.metaData = list()
        self.tempData = list()

        try:
            self.ser = Serial(port=self.port, baudrate=921600, bytesize=8,
                              parity="N", stopbits=1, timeout=self.timeout, )
            self.ser.set_buffer_size(self.BUFFER_SIZE)
        except:
            self.ser = None
            print("ERROR: Access denied")

    def __write(self, command):
        """Function to send command to device and return response.
        Args:
            command (str): command to be sent to device.
        Returns:
            None
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        self.ser.write(format_cr(command=command))
        self.responseLoop()

    def __canFloat(self, varList):
        """Checks if all entries in given list can be converted to floats.
        Args:
            varList (list): list of given parameters.
        Returns:
            (bool) True if all entries can be floated, False if not.
        """
        try:
            [float(x) for x in varList]
            return True
        except:
            return False

    def __sanitize_dataCapture(self):
        """Parse DMO data into structured list and remove non-compliant rows.
        Args:
            None.
        Returns:
            None.
        """
        removeSpikes = False
        #convert response into structured list
        self.tempData = [x.split("\t") for x in self.response.split("\r\n")]
        #pull out meta data from list
        self.metaData = self.tempData[0:self.META_TABLE_LEN]
        #pull out data capture columns from list
        self.dataCapColumns = self.tempData[self.DATA_TABLE_COLS_IDX]

        #iterate through data and remove any improper length entries
        self.tempData = [x for x in self.tempData if len(x) == self.ENTRY_LEN]
        #iterate through data and remove any improper data formats; save to dataCapture
        self.tempData = [[float(y) for y in x] for x in self.tempData if self.__canFloat(x)]

        #parse through data and remove anomolous spikes
        if removeSpikes:
            #always accept first data point as truth and setup for loop
            self.dataCapture.append(self.tempData[0])
            idxData = [self.tempData[0][self.IDX_DATA_COL], self.tempData[1][self.IDX_DATA_COL]]
            speedData = [self.tempData[0][self.SPEED_DATA_COL], self.tempData[1][self.SPEED_DATA_COL]]
            #iterate throughdata and remove any anomolous data points
            for i in range(len(self.tempData)-2):
                #do not add if index is vastly different
                if abs(idxData[1] - idxData[0]) > self.MAX_IDX_DELTA:
                    #update front point only
                    idxData[1] = self.tempData[i+2][self.IDX_DATA_COL]
                #do not add if speed is vastly different
                elif abs(speedData[1] - speedData[0]) > self.MAX_SPEED_DELTA:
                    #update front point only
                    idxData[1] = self.tempData[i+2][self.SPEED_DATA_COL]
                #otherwise add to list
                else:
                    self.dataCapture.append(self.tempData[i+1])
                    #update both points
                    idxData = (self.tempData[i+1][self.IDX_DATA_COL], self.tempData[i+2][self.IDX_DATA_COL])
                    speedData = (self.tempData[i+1][self.SPEED_DATA_COL], self.tempData[i+2][self.SPEED_DATA_COL])
        else:
            self.dataCapture = [x for x in self.tempData]

    def report_dataCapture(self):
        """Command to read data buffer on chip with DMO command.
        Args:
            None.
        Returns:
            None.
        Does:
            Fills the dataCapture attribute with Cleaned DMO data.
        """
        self.flush()
        if self.printResp:
            self.printResp = False
            self.__write("DMO")
            self.printResp = True
        else:
            self.__write("DMO")
        print("Collected data capture; needs to be sanitized")
        self.__sanitize_dataCapture()
        print("Data sanitized")

    def trigger_capture(self):
        """Command to one time trigger data capture on spin test hardware.
        Args:
            None.
        Returns:
            None.
        Does:
            Triggers data capture with TRG command.
        """
        self.flush()
        self.__write("TRG")
        if not self.printResp:
            print("\tTriggered data capture")



class MD90(DSM_Device):
    """Interaction object for DSM MD-90.
    Args:
        port (str): COMport for connection. ex: "COM1".
        [timeout (float)]: Wait time before timeout in seconds.
        [printResp (bool)]: flag to print response or not.
    Returns:
        None.
    Does:
        Creates serial connection to device and interaction oject with basic
        functions built in like a mini device API.
    """

    def __init__(self, port, timeout=0.1, printResp=True):
        self.port = port
        self.timeout = timeout
        self.printResp = printResp
        self.response = None

        try:
            self.ser = Serial(port=self.port, baudrate=115200, bytesize=8,
                              parity="N", stopbits=1, timeout=self.timeout)
        except:
            self.ser = None
            print("ERROR: Access denied")

    def write(self, command):
        """Function to send command to device and return response.
        Args:
            command (str): command to be sent to device.
        Returns:
            None
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        self.ser.write(format_cr(command=command))
        self.responseLoop()

    def get_id(self):
        self.flush()
        self.write("VER")

    def get_position(self):
        self.flush()
        self.write("GEE")

    def takeStep(self, val):
        self.flush()
        if val == True:
            self.write("ETS")
        elif val == False:
            self.write("DTS")

    def persistentMove(self, val):
        self.flush()
        if val == True:
            self.write("EPM")
        elif val == False:
            self.write("DPM")

    def deadband(self, val=None):
        self.flush()
        if val == None:
            self.write("GDB")
        else:
            self.write(f"SDB{val}")

    def set_rail(self, val):
        """Set status of rail either high or low.
        Args:
            val (bool): True turns on rails, False turns off rails.
        Returns:
            None.
        """
        self.flush()
        if val == True:
            self.write("EPS")
        elif val == False:
            self.write("DPS")


    def ramp_extender(self, val):
        self.flush()
        self.write(f"RDE{val}")


    def ramp_clamper(self, val):
        self.flush()
        self.write(f"RDC{val}")

    def closedLoop(self, val):
        self.flush()
        self.write(f"CLM{val}")



class PSC_Controller(DSM_Device):
    """Interaction object for DSM PSC general purpose controller.
    Args:
        port (str): COMport for connection. ex: "COM1".
        [timeout (float)]: Wait time before timeout in seconds.
        [printResp (bool)]: flag to print response or not.
    Returns:
        None.
    Does:
        Creates serial connection to device and interaction oject with basic
        functions built in like a mini device API.
    """
    def __init__(self, port, timeout=0.1, printResp=True):
        self.port = port
        self.timeout = timeout
        self.printResp = printResp
        self.response = None

        try:
            self.ser = Serial(port=self.port, baudrate=921600, bytesize=8,
                              parity="N", stopbits=1, timeout=self.timeout)
        except:
            self.ser = None
            print("ERROR: Access denied")


    def write(self, command):
        """Function to send command to device and return response.
        Args:
            command (str): command to be sent to device.
        Returns:
            None
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        self.ser.write(format_cr(command=command))
        self.responseLoop_tabbed()


    def write_machSerResp(self, command):
        """Function writes command and listens for hex response.
        Args:
            command (str): command to send to device.
        Returns:
            None.
        Note:
            Prints response to cli by defult. Disable using self.printResp=False.
        """
        self.flush()
        self.write_varResponse(format_cr(command=command), self.hexRespLoop)


    #command wrapper functions
    def mainMenu(self):
        """Function wrapper for SERV command.
        Args:
            None.
        Returns:
            None.
        """
        self.write("MENU")

    def servMenu(self):
        """Function wrapper for SERV command.
        Args:
            None.
        Returns:
            None.
        """
        self.write("SERV")

    def streamMode(self, input=None):
        """Function wrapper for MENU->STRM command.
        Args:
            [OPT] input (int): 0 for false, 1 for true.
        Returns:
            None.
        Note:
            Function acts as getter with no given input.
        """
        #if getter
        if input == None:
            self.write("STRM")
        #else setter
        else:
            self.write(f"STRM {input}")

    def responseFormat(self, input=None):
        """Function wrapper for MENU->RFRM command.
        Args:
            [OPT] input (int): 0 for machine, 1 for human, 2 for dev/UI.
        Returns:
            None.
        Note:
            Function acts as getter with no given input.
        """
        #if getter
        if input == None:
            self.write("RFRM")
        #else setter
        else:
            self.write(f"RFRM {input}")

    def sampleRate(self, input=None):
        """Function wrapper for SERV->SPRT command.
        Args:
            [OPT] input (int): sample rate in Hz.
        Returns:
            None.
        Note:
            Function acts as getter with no given input.
        """
        #if getter
        if input == None:
            self.write("SPRT")
        #else setter
        else:
            self.write(f"SPRT {input}")


    def systemMode(self, input=None):
        """Function wrapper for SERV->SYSM command.
        Args:
            [OPT] input (int): 0 for openloop, 1 for closed loop.
        Returns:
            None.
        Note:
            Function acts as getter with no given input.
        """
        #if getter
        if input == None:
            self.write("SYSM")
        #else setter
        else:
            self.write(f"SYSM {input}")

    def target(self, input=None):
        """Function wrapper for SERV->TARG command.
        Args:
            [OPT] input (float): desired target position in system set eu.
        Returns:
            None.
        Note:
            Function acts as getter with no given input.
        """
        #if getter
        if input == None:
            self.write("TARG")
        #else setter
        else:
            self.write(f"TARG {input}")

    def target_streamed(self, input=None):
        """Function wrapper for SERV->TARG command with hex streamed response.
        Args:
            [OPT] input (float): desired target position in system set eu.
        Returns:
            None.
        Note:
            Function acts as getter with no given input.
        """
        #if getter
        if input == None:
            self.write("TARG")
        #else setter
        else:
            self.printResp = False  #disable printResp
            #ensure stream is enabled and set to 500Hz
            self.mainMenu()
            self.streamMode(1)
            self.servMenu()
            self.sampleRate(500)
            self.printResp = True   #enable printResp
            self.flush()
            self.write_machSerResp(f"TARG {input}")


    #def deugData(self, input=None):
