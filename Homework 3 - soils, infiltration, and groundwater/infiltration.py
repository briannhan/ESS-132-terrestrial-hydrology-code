# -*- coding: utf-8 -*-
"""
The purpose of this module is to perform calculations of the infiltration
of water into soil using the Horton equations (empirical) and the
Green-Ampt model (somewhat theoretical but simplified). This module can be
imported by other scripts, which would then use the methods within this module
"""


import numpy as np

# %%
# Calculating infiltration capacity using the Horton equations


def infilCapaHorton(f0, fc, k, t):
    """Calculates infiltration capacity (max infiltration rate) using the
    Horton equation for infiltration capacity

    Parameters
    ----------
    f0 = initial infiltration capacity (length/time)
    fc = infiltration capacity after soil becomes saturated (length/time)
    t = time (hours, minutes, seconds)
    k = decay constant specific to the soil (estimated), (hr^-1)

    Returns
    -------
    ft = infiltration capacity at time t (length/time)

    """
    ft = fc + (f0 - fc)*np.exp(-k*t)
    return ft


def totalInfilHorton1time(f0, fc, k, t):
    """Assuming that the actual infiltration rate is the infiltration capacity,
    this calculates the maximum amount of water that can infiltrate after a
    given amount of time using an integrated version of the Horton equation

    Parameters
    ----------
    f0 = initial infiltration capacity (length/time)
    fc = infiltration capacity after soil becomes saturated (length/time)
    t = time (hours, minutes, seconds)
    k = decay constant specific to the soil (estimated), (hr^-1)

    Returns
    -------
    Ft = total amount of infiltration after time t (length)
    """
    numerator = (f0 - fc)*(1 - np.exp(-k*t))
    Ft = (fc*t) + (numerator/k)
    return Ft


def totalInfilHorton2time(f0, fc, k, t1, t2):
    """Assuming that the actual infiltration rate is the infiltration capacity,
    this calculates the maximum amount of water that can infiltrate between
    2 time periods by taking the definite integral of the Horton equation
    between times t1 & t2.

    Parameters
    ----------
    f0 = initial infiltration capacity (length/time)
    fc = infiltration capacity after soil becomes saturated (length/time)
    t1 = initial time (hours, minutes, seconds)
    t2 = final time (hours, minutes, seconds)
    k = decay constant specific to the soil (estimated), (hr^-1)

    Returns
    -------
    Ft = total amount of infiltration between times t1 & t2 (length)
    """
    fraction = (f0 - fc)/(-k)
    Ft = (fc*t2) - (fc*t1) + (fraction*(np.exp(-k*t2) - np.exp(-k*t1)))
    return Ft


def kOrt(f0, fc, f, knownValue, unknownVar):
    """Intended to be used for calculations involving the Horton equation. This
    calculates the value of the decay rate constant (k) if knownValue is time
    (t) and if knownValue is the decay rate constant (k), then it calculates
    the time (t)

    Parameters
    ----------
    f0 = initial infiltration capacity (length/time)
    fc = infiltration capacity after soil becomes saturated (length/time)
    f0 = infiltration capacity at a specific time t (length/time)
    knownValue = either k or t; if it's k, then units are time^-1 and this
    function returns time t, and if it's t, then the units are units of time
    and this function returns the decay rate constant
    unknownVar = a character (k or t) that signifies the variable that the user
    wants this function to return

    Returns
    -------
    list of the following 2 items:
    variable = string that describes the variable that this function calculates
    unknownValue = the value of the variable that this function calculates; if
    knownValue is k, then this variable is t with units of time, and if
    knownValue is t, then this variable is k with units of time^-1
    """
    unknownValue = np.log((f - fc)/(f0 - fc))/(-knownValue)
    if "k" in unknownVar.lower():
        variable = "decay rate constant"
    elif "t" in unknownVar.lower():
        variable = "time"
    return [variable, unknownValue]
# %%
# Calculates infiltration rates using the Green-Ampt model


def Fpond(presHead, Ks, thetaSat, thetaInit, rainfallRate):
    """Calculates the total amount of water that had infiltrated before
    ponding occurred

    Parameters
    ----------
    presHead = pressure head, can be obtained by soil texture (length)
    Ks = saturated hydraulic conductivity, can be obtained by soil texture,
    (length/time)
    thetaSat = saturated water content
    thetaInit = initial water content
    rainfallRate = well, pretty self-explanatory (length/time)

    Returns
    -------
    Fp = total amount of water infiltrated by the time ponding started (length)
    """
    numerator = np.absolute(presHead)*Ks*(thetaSat - thetaInit)
    denominator = rainfallRate - Ks

    Fp = numerator/denominator
    return Fp


def timep(Fp, rainfallRate):
    """Calculates the amount of time it takes before ponding occurs

    Parameters
    ----------
    Fp = total amount of water infiltrated by the time ponding started (length)
    rainfallRate = well, pretty self-explanatory (length/time)

    Returns
    -------
    timep = amount of time before ponding takes place (hour, minutes, seconds)
    """
    timep = Fp/rainfallRate
    return timep


def infilRateGA(Ks, presHead, thetaSat, thetaInit, F, tp):
    """Calculates the infiltration rate in the Green-Ampt model. The
    infiltration rate is calculated AFTER ponding occurs. The infiltration rate
    when t <= tp is the rainfall rate.

    Parameters
    -----------
    rainfallRate = well, pretty self-explanatory (length/time)
    presHead = pressure head, can be obtained by soil texture (length)
    Ks = saturated hydraulic conductivity, can be obtained by soil texture,
    (length/time)
    thetaSat = saturated water content
    thetaInit = initial water content
    F = total amount infiltrated at time t (length)
    tp = amount of time before ponding takes place (hour, minutes, seconds)

    Returns
    -------
    f = infiltration rate after a given amount F had infiltrated (length/time)
    """
    numerator = Ks*np.absolute(presHead)*(thetaSat - thetaInit)
    fraction = numerator/F
    f = Ks + fraction

    return f


def time(tp, Ks, F, Fp, presHead, thetaSat, thetaInit):
    """Calculates the amount of time it takes for a given amount F to have
    infiltrated if the amount that had infiltrated is GREATER than the amount
    that infiltrated before ponding takes place

    Parameters
    ----------
    tp = amount of time before ponding takes place (hour, minutes, seconds)
    presHead = pressure head, can be obtained by soil texture (length)
    Ks = saturated hydraulic conductivity, can be obtained by soil texture,
    (length/time)
    F = total amount infiltrated at the specified time (length)
    Fp = total amount of water infiltrated by the time ponding started (length)
    thetaSat = saturated water content
    thetaInit = initial water content

    Returns
    -------
    time = amount of time it takes for the amount F to have infiltrated
    (hours, minutes, seconds)"""

    numeratorLN = Fp + np.absolute(presHead)*(thetaSat - thetaInit)
    denomLN = F + np.absolute(presHead)*(thetaSat - thetaInit)
    naturalLog = np.log(numeratorLN/denomLN)

    product1 = np.absolute(presHead)*(thetaSat - thetaInit)*naturalLog
    brackets = F - Fp + product1

    product2 = (1/Ks)*brackets
    time = tp + product2
    return time


def stormEnd(tp, Ks, F, Fp, presHead, thetaSat, thetaInit, endingTime):
    """This function is intended to be used to find the total amount of
    infiltration by the end of a storm. The function is intended to be called
    once by another function (function x) in the script that uses this function
    and function x will then undergo the root finding algorithms of scipy.
    Function x will take only 1 argument: the mathematical root of the
    function, which is the total amount infiltrated by the end of the storm.
    Function stormEnd(), which is this function, will have the same form
    as function time(), but it will subtract the ending time while time()
    does not. The purpose of this subtraction is to ensure the total amount
    infiltrated by the end of the storm truly occurs by the end of the stormf
    and to also ensures that the returned value, when properly optimized, is 0

    Parameters
    ----------
    tp = amount of time before ponding takes place (hour, minutes, seconds)
    presHead = pressure head, can be obtained by soil texture (length)
    Ks = saturated hydraulic conductivity, can be obtained by soil texture,
    (length/time)
    F = total amount infiltrated at the specified time (length)
    Fp = total amount of water infiltrated by the time ponding started (length)
    thetaSat = saturated water content
    thetaInit = initial water content
    endingTime = the time when the storm ends; storm duration (units of time)

    Returns
    -------
    time = amount of 'time' it takes for the amount F to have infiltrated,
    should be 0 if properly optimized (hours, minutes, seconds)"""

    numeratorLN = Fp + np.absolute(presHead)*(thetaSat - thetaInit)
    denomLN = F + np.absolute(presHead)*(thetaSat - thetaInit)
    naturalLog = np.log(numeratorLN/denomLN)

    product1 = np.absolute(presHead)*(thetaSat - thetaInit)*naturalLog
    brackets = F - Fp + product1

    product2 = (1/Ks)*brackets
    time = tp + product2 - endingTime
    return time


def graphData(finalF, rainfallRate, Ksat, presHead, thetaSat, thetaInit):
    """Returns a numpy 2-D array that will be used to make a plot of
    infiltration rates over time according to the Green-Ampt model

    Parameters
    ----------
    finalF = total amount infiltrated by the time the storm ended (length)
    rainfallRate = self-explanatory; the rainfall rate of a storm (length/time)
    Ksat = saturated hydraulic conductivity of a specific soil
    presHead = pressure head at wetting front, same as the variable used in
    other Green-Ampt model functions (length)
    thetaSat = saturated water content
    thetaInit = initial water content

    Returns
    -------
    A 2-D numpy array in which the first row is time and the second row
    contains infiltration rates at those times
    """
    Fp = Fpond(presHead, Ksat, thetaSat, thetaInit, rainfallRate)
    pondingTime = timep(Fp, rainfallRate)
    # making arrays of values before ponding
    timeArrayBeforePond = np.linspace(0, pondingTime)
    infilRateArrayBeforePond = np.full(50, rainfallRate)

    # making arrays of values after ponding
    initFp = Fp + (1e-8)
    infilAmountAfterPond = np.linspace(initFp, finalF)
    timeArrayAfterPond = time(pondingTime, Ksat, infilAmountAfterPond, Fp,
                              presHead, thetaSat, thetaInit)
    infilRateArrayAfterPond = infilRateGA(Ksat, presHead, thetaSat, thetaInit,
                                          infilAmountAfterPond, pondingTime)

    # combining arrays of values
    timeArray = np.concatenate((timeArrayBeforePond, timeArrayAfterPond))
    infilRateArray = np.concatenate((infilRateArrayBeforePond,
                                     infilRateArrayAfterPond))
    results = np.stack((timeArray, infilRateArray), axis=0)
    return results
