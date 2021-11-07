"""
Author: Austin Tabulog
Date: 11/18/19
email: atabulog@dynamic-structures.com

============================================================================
The following program is property of Dynamic Structures and Materials LLC.
Use of the following code is prohibited without express permision from
Dynamic Structures and Materials LLC.
============================================================================

OBJECTIVE: Module for fft related calculations and manipulation.
"""
#imports
from math import sqrt
from dsmutil.signal import firstDifference


def get_mag(data, frequency):
    """Return magnitude value for a given frequency from formatted pandas
       dataFrame.
    Args:
        data (pd.DataFrame): data to parse formatted with arbitrary index and
                             columns ['Frequency', 'Magnitude'].
        frequency (int or float): frequency of interest.
    Returns:
        magnitude (float): magnitude of frequency provided in float format.
    """
    return float(data[data.Frequency==frequency].Magnitude.iloc[0])


def calc_qFactor(data, frequency):
    """Return calculated qFactor for a given peak from formatted pandas
       dataFrame.
    Args:
        data (pd.DataFrame): data to parse formatted with arbitrary index and
                             columns ['Frequency', 'Magnitude'].
        frequency (int or float): frequency of interest.
    Returns:
        qFactor (float):qFactor of peak provided in float format.
    """
    #peak index
    peakIndex = int(data[data.Frequency == frequency].index.values)
    #get amplitude for peak frequency
    peakAmp = float(data.Magnitude.iloc[peakIndex])
    #get frequency bounds for value passing threshold
    upperFreq = data[data.Magnitude.values > peakAmp / sqrt(2)].iloc[-1].Frequency
    lowerFreq = data[data.Magnitude.values > peakAmp / sqrt(2)].iloc[0].Frequency

    # get slope of signal for slope termination
    slope = firstDifference(data=data)
    peakSign = float(slope[slope.Frequency == frequency].Sign.iloc[0])

    #get frequency where slope change occurs
    upperSign = slope[slope.index > peakIndex].Sign
    upperIndex = upperSign[upperSign.values != -1].index[0]

    lowerSign = slope[slope.index < peakIndex].Sign
    lowerIndex = lowerSign[lowerSign.values != 1].index[0]
    #switch to slope stop if slope change is closer than threshold values
    if slope.iloc[upperIndex].Frequency < upperFreq:
        upperFreq = slope.iloc[upperIndex].Frequency
    if slope.iloc[lowerIndex].Frequency > lowerFreq:
        lowerFreq = slope.iloc[lowerIndex].Frequency

    return float(frequency / abs(upperFreq - lowerFreq))


def calc_deltaFreq(freqs):
    """Return calculated frequency delta in Hz.
    Args:
        freqs (list): list of frequencies to compare in kHz.
    Returns:
        delta_frequency (float): frequency delta in Hz in float.
    """
    return abs(1000*(freqs[0] - freqs[1]))


def calc_deltaMag(freqs, data):
    """Return calculated frequency delta in Hz.
    Args:
        freqs (list): list of frequencies to compare in kHz.
    Returns:
        delta_frequency (float): magnitude delta in float.
    """
    mag1 = get_mag(data=data, frequency=freqs[0]*1000)
    mag2 = get_mag(data=data, frequency=freqs[1]*1000)
    return abs(mag2 - mag1)
