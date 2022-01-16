# -*- coding: utf-8 -*-
"""
Author: Austin Tabulog
Date: 09/01/2021
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Package to support command line style interactions with formatted commands.
"""

#imports
class StringProcessor():
    """docstring for ."""

    def __init__(self, cmdDict=dict(), cmdLen=None, separator=" ", inputStr="\nCommand: "):
        self.cmdDict = cmdDict
        self.cmdLen = cmdLen
        self.separator = separator
        self.activeFlag = False
        self.cmd = None
        self.param = None
        self.inputStr=inputStr

        #add exit command to cmdDict
        cmdDict["EXIT"]= [None, "Exit command processor", []]

    def reset_command(self):
        self.cmd = None
        self.param = None

    def add_command(self, entry):
        """Add command to command dict.
        Args:
            entry: list of two params. param 1 is key string. Param 2 is formatted
                   list of [execution funciton, "description", optional list of default params]
        Returns:
            None.
        """
        failedFlag = False
        #check if entry is of appropriate length
        if len(entry) < 2 or len(entry) > 3:
            failedFlag = True
        elif type(entry[0]) != type(""): #check if key name acceptable
            failedFlag = True
        elif hasattr(entry[1][0], '__call__') == False: #check if given value NOT callable function or method
            failedFlag = True
        elif len(entry[1])==3:
            if type(entry[1][2] != list()): #if optional parameter given, and not of list type
                failedFlag  = True

        #if entry failed checks, print message and pass
        if failedFlag:
            print(f"Entry not added: {entry}")
        else:
            try:
                self.cmdDict[entry[0].upper()] = entry[1]
            except:
                print(f"Entry not added: {entry}")


    def print_commands(self):
        print("\nCOMMANDS")
        print("==========================================")
        for k,v in self.cmdDict.items():
            print(f"{k}:\t{v[1]}")
        print("==========================================\n")

    def parse_command(self, usrInput):
        """Match given input to command structure.
        Args:
            usrInput (str): given user string.
        Returns:
            None.
        """
        #if no command length given, parse by separator
        if self.cmdLen==None:
            if usrInput != "":
                try:
                    self.cmd = usrInput.split(self.separator)[0].upper()
                    self.param = float(usrInput.split(self.separator)[1])
                except:
                    self.cmd = usrInput
                    self.param = None

        #else parse by command length
        else:
            try:
                self.cmd = usrInput[0:self.cmdLen].upper()
                if usrInput[self.cmdLen:] == "":
                    self.param = None
                else:
                    self.param = float(usrInput[self.cmdLen:])
                self.cmdFlag = True
            except:
                pass

    def process_command(self):
        """Processes given command against known command dictionary.
        Args:
            None.
        Returns:
            None.
        """

        for k,v in self.cmdDict.items():
            if self.cmd == k:
                #check if exit command
                if v[0] == None:
                    self.activeFlag = False
                    break
                #execute funciton without value if no parameter given
                elif self.param == None:
                    try:
                        #run wiht default param if given
                        if len(v) == 3:
                            v[0](v[2])
                        #else run with no param
                        else:
                            v[0]()
                    except:
                        print("ERROR: could not run with default parameter.")
                #else execute with parameter list
                else:
                    try:
                        v[0](v[2])
                    except:
                        print("ERROR: could not execute with given parameter.")

        #reset command after processing
        self.reset_command()

    def start_commandProcessor(self):
        """Starts the command processor loop.
        Args:
            None.
        Returns:
            None
        """
        self.print_commands()
        self.activeFlag = True
        while self.activeFlag == True:
            self.parse_command(input(self.inputStr).upper())
            self.process_command()
        print("\nCOMMAND ENTRY EXITED")
