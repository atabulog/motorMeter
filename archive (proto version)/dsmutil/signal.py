"""
Author: Austin Tabulog
Date: 11/30/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Module describing signal manipulation functions.
"""
#imports
from pandas import DataFrame, errors
from numpy import column_stack, array, convolve, sign

class columnError(ValueError):
    """Exception that is raised by a column mismatch error.
    """


def check_format(data, format):
    """Check if columns given match desired format.
    Args:
        data (pd.DataFrame): dataFrame to check fit against reference.
        format (pd.DataFrame): formatted dataFrame to use as reference.
    Returns:
        bool: True if exact match, False otherwise.
    """
    check = True
    # check if columns are identical
    if not data.columns.tolist() == format.columns.tolist():
        check = False

    return check


def rec_lowPass(data, x=0.1):
    """Symmetric lowpass filter function.
    Args:
        data (pd.DataFrame): Dataframe in [Frequency, Magnitude] format.
    [OPT] x (float): float of filter value between 0 and 1.
    Returns:
        dataOut (pd.DataFrame): dataFrame of filtered Data in same form as data.
    """

    # define filter math parameters
    a0 = 1 - x
    b1 = x

    # define storage variable
    filteredResults = [data.Magnitude.values.tolist(), [data.Magnitude.values[0]],
                       [data.Magnitude.values[0]]]
    # do twice
    for i in range(2):
        # apply recursive filter from low to high
        for j in range(len(data.Magnitude.values)):
            filteredResults[i+1].append(
                a0*filteredResults[i][j] + b1*filteredResults[i+1][j-1])
        # filp order of filtered list
        filteredResults[i+1] = list(reversed(filteredResults[i+1]))

    # format final filtered list into dataFrame
    dataOut = DataFrame(
        data=column_stack(
        (data.Frequency.values, list(reversed(filteredResults[1][1:])))),
        columns=data.columns)
    return dataOut


def firstDifference(data):
    """Create first difference of given magnitude data.
    Args:
        data (pd.DataFrame): Dataframe in [Frequency, Magnitude] format.
    Returns:
        firstDiff (pd.DataFrame): first difference data following input format
                                  with extra sign column.
    """
    #expected format df
    formDf = DataFrame(column_stack(([], [])),
                       columns=["Frequency", "Magnitude"])

    #check if input data is correct format
    if check_format(data, formDf):
        # convolve input data
        diffData = convolve(data.Magnitude.values, array([1, -1]), mode="same").T
        #reformat to input format
        vals = column_stack((data.Frequency.values, diffData, sign(diffData)))
        diffDf = DataFrame(data=vals,
                           columns=["Frequency", "Magnitude", "Sign"])
        return diffDf.drop(diffDf.index[0])
    else:
        columnError(
            f"\nExpected format {formDf.columns}.\n" + \
            f"Given format {data.columns}."
            )
