# -*- coding: utf-8 -*-
"""
Author: Austin Tabulog
Date: 01/15/2020
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Method to scale values based on given units.
"""
from pandas import DataFrame

def scale_unit(given, desired):
    """Convert scale factor of similar unit.
    Args:
        given (str): given unit.
        desired (str): desired unit.
    Returns:
        scale (float): scale factor to multiply value by.
    """
    #check if greek letters present
    try:
        given.encode(encoding="utf-8").decode("ascii")
    except:
        print("THIS IS UNFINISHED")
        import pdb; pdb.set_trace()
    try:
        desired.encode(encoding="utf-8").decode("ascii")
    except:
        desired = "ohm"

    #if already equivalent, skip the rest
    if given == desired:
        return 1.0
    else:
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
        symbol = given[1:]
        try:
            givenScale = unitDf[unitDf.Prefix == given.strip(symbol)].Scale.values[0]
        except:
            raise KeyError(f"Unit factor {given.strip(symbol)} not recognized.")

        try:
            desiredScale = unitDf[unitDf.Prefix == desired.strip(symbol)].Scale.values[0]
        except:
            raise KeyError(f"Unit factor {desired.strip(symbol)} not recognized.")
        return float(givenScale/desiredScale)
