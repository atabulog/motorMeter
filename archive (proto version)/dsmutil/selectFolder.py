"""
Author: Austin Tabulog
Date: 11/30/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Module for GUI based folder selection.
"""
from tkinter import Tk
from tkinter.filedialog import askdirectory
from os.path import basename, splitext

def selectFolder(initialdir="\\\\DSMDC\\itar\\DEM17-01\\Data Experimental\\",
                 title="Select a folder."):
    """Launches GUI prompt to select log folder.
    Args:
        initialdir (str): [optional] starting path to look for file.
        title (str): [optional] instruction appearing in window frame.
    Returns:
        folderPath (str): Full filepath to log file with extension.
        folderName (str): File basename without extension.
    """
    root = Tk()
    # call tkinter folder dialog function
    folderPath = askdirectory(initialdir="C:/Desktop",
                              title="Select test data folder")
    folderPath = folderPath.replace("/", "\\")
    folderName = splitext(basename(folderPath))[0]
    folderPath = folderPath + "\\"
    root.destroy()
    return folderPath, folderName
