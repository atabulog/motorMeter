"""
Author: Austin Tabulog
Date: 10/30/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Module for GUI based file selection.
"""
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from os.path import basename

def selectFile(initialdir="\\\\DSMDC\\itar\\DEM17-01\\Data Experimental\\",
               title="Select a file.",
               extension="*.xlsx"):
    """Launches GUI prompt to select log file.
    Args:
        initialdir (str): [optional] starting path to look for file.
        title (str): [optional] instruction appearing in window frame.
    Returns:
        filepath (str): Full filepath to log file with extension.
        fileName (str): File basename without extension.
    """
    root = Tk()
    filepath = askopenfilename(initialdir=initialdir,
                               filetypes=(("filetype", extension),
                                          ("All Files", "*.*")),
                               title=title)
    filepath = filepath.replace("/", "\\")
    filename = basename(filepath).split(".")[0]
    root.destroy()
    return filepath, filename
