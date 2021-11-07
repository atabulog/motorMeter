"""
Author: Austin Tabulog
Date: 11/01/20
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: unique file name iterator from given base name and folder.
"""
#imports
from os import listdir
from os.path import splitext

#function
def gen_filename(folderPath, base):
    """Generates unique filename from given base within folderPath.
    Args:
        folderPath (str): folder to look in for file placement.
        base (str): file base name on which a numeric value is appended.
    Returns:
        fname (str): unique basename for new file.
    """
    #loop variables
    checkName = base
    exitFlag = False
    iterVal = 1

    # while no exit condition occurs
    while not exitFlag:
        noMatch = True
        #try to match name to all files (name and extension) in folder
        for file in listdir(folderPath):
            #if match is made, exit loop and no end condition
            if file == checkName:
                noMatch = False
                break
        #if no matches were found, raise end condition
        if noMatch:
            exitFlag = True

        #if match was found, iterate on name
        else:
            checkName = splitext(base)[0] + f"_{iterVal}" + splitext(base)[1]
            iterVal += 1

        #arbitrary stop value to end endless loops from occuring
        if iterVal > 1000:
            print(base)
            print(checkName)
            print(iterVal)
            raise ValueError("No name could be generated.")

    return checkName
