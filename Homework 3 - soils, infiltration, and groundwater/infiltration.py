# -*- coding: utf-8 -*-
"""
The purpose of this script is to perform calculations of the infiltration
of water into soil using the Horton equations (empirical) and the
Green-Ampt model (somewhat theoretical but simplified)
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


def totalInfilHorton(f0, fc, k, t):
    """Calculates the total amount that had infiltrated using an integrated
    version of the Horton equation

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


def infilRateGA(rainfallRate, Ks, presHead, thetaSat, thetaInit, F, t, tp):
    """Calculates the infiltration rate in the Green-Ampt model. The
    infiltration rate is calculated 2 different ways: before ponding and
    after ponding

    Parameters
    -----------
    rainfallRate = well, pretty self-explanatory (length/time)
    presHead = pressure head, can be obtained by soil texture (length)
    Ks = saturated hydraulic conductivity, can be obtained by soil texture,
    (length/time)
    thetaSat = saturated water content
    thetaInit = initial water content
    t = a point in time (hours, minutes, seconds)
    F = total amount infiltrated at time t (length)
    tp = amount of time before ponding takes place (hour, minutes, seconds)

    Returns
    -------
    f = infiltration rate after a given amount F had infiltrated (length/time)
    """
    if t <= tp:
        f = rainfallRate
    elif t > tp:
        numerator = Ks*np.absolute(presHead)*(thetaSat - thetaInit)
        fraction = numerator/F
        f = Ks + fraction

    return f


def time(tp, Ks, F, Fp, presHead, thetaSat, thetaInit):
    """Calculates the amount of time it takes for a given amount F to have
    infiltrated if the amount that had infiltrated is greated than the amount
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
    if F > Fp:
        numeratorLN = Fp + np.absolute(presHead)*(thetaSat - thetaInit)
        denomLN = F + np.absolute(presHead)*(thetaSat - thetaInit)
        naturalLog = np.log(numeratorLN/denomLN)

        product1 = np.absolute(presHead)*(thetaSat - thetaInit)*naturalLog
        brackets = F - Fp + product1

        product2 = (1/Ks)*brackets
        time = tp + product2
        return time

    else:
        print("F is equal to or less than Fp, can't use this function")
        return
