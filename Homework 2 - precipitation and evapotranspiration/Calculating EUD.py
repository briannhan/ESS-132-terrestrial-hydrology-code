# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 21:06:22 2020

@author: Brian Chung
"""


import numpy as np


# %%
def thiessenPolygonEUD(area, precip) -> float:
    """
    Calculates Equivalent Uniform Depth of precipitation using
    Thiessen Polygons

    Parameters
    ------------
    area = list of area of individual Thiessen Polygons (km2)
    precip = list of rain gauge readings from each Thiessen Polygon (mm)

    Returns
    ---------
    EUD = EUD of entire watershed
    """

    area = np.array(area)
    totalArea = np.sum(area)
    precip = np.array(precip)

    EUDsingles = precip*area/totalArea
    EUD = np.sum(EUDsingles)
    return EUD


precipA = 17.3
areaA = 125

precipB = 18.6
areaB = 310

precipC = 20.1
areaC = 190

precipD = 22.7
areaD = 210

precipE = 21.3
areaE = 290

precipF = 19.8
areaF = 130

precipG = 18.1
areaG = 205

precipH = 16.9
areaH = 105

areaList = [areaA, areaB, areaC, areaD, areaE, areaF, areaG, areaH]
pptList = [precipA, precipB, precipC, precipD,
           precipE, precipF, precipG, precipH]

thiessenEUD = thiessenPolygonEUD(areaList, pptList)
# %%
isohyeteBelow17 = np.array(17)
areaBelow17 = 70

isohyete17_18 = np.array([17, 18])
area17_18 = 245

isohyete18_19 = np.array([18, 19])
area18_19 = 300

isohyete19_20 = np.array([19, 20])
area19_20 = 240

isohyete20_21 = np.array([20, 21])
area20_21 = 335

isohyete21_22 = np.array([21, 22])
area21_22 = 250

isohyete22 = np.array([22])
area22 = 125

totalArea = np.sum([areaBelow17, area17_18, area18_19, area19_20, area20_21,
                    area21_22, area22])


def isohyetalSinglesEUD(isohyetes, area) -> float:
    """
    Calculates Equivalent Uniform Depth of precipitation of a single region
    between isohyetes. It does so by taking the mean of the isohyetes
    and multiplying that by the area between the 2 isohyetes in the watershed
    or the area bounded by that isohyete and the watershed


    Parameters
    -----------
    isohyetes = numpy array of 1 or 2 isohyetes (mm)
    area = area between isohyetes (km2)
    """
    isohyeteMean = np.mean(isohyetes)
    EUDsingle = area*isohyeteMean/totalArea

    return EUDsingle


isohyetalEUD = np.sum([isohyetalSinglesEUD(isohyeteBelow17, areaBelow17),
                       isohyetalSinglesEUD(isohyete17_18, area17_18),
                       isohyetalSinglesEUD(isohyete18_19, area18_19),
                       isohyetalSinglesEUD(isohyete19_20, area19_20),
                       isohyetalSinglesEUD(isohyete20_21, area20_21),
                       isohyetalSinglesEUD(isohyete21_22, area21_22),
                       isohyetalSinglesEUD(isohyete22, area22)])
# %%


def vaporPressure(temp: float) -> float:
    """Calculates the saturation vapor pressure of water at a particular
    temperature using the Clausius-Clayperon equation

    Parameter
    ----------
    temp = air temperature in degrees Celsius

    Returns
    --------
    vp = vapor pressure in Pascal"""
    exponent = (17.27*temp)/(temp + 237.3)
    vp = 611*np.exp(exponent)

    return vp


saturationVP_Pa = vaporPressure(21)
saturationVP_inHg = saturationVP_Pa*2.9533*(10**(-4))
actualVP_Pa = vaporPressure(11)
actualVP_inHg = actualVP_Pa*2.9533*(10**(-4))
actualVP_mb = actualVP_Pa/100

RH = 100*actualVP_Pa/saturationVP_Pa

# The units of the evaporation rate in the Meyer equation are inches/day
evapoMeyer_in = 0.36*(saturationVP_inHg - actualVP_inHg)*(1 + (2.1/10))

# Conversion of rate to cm/day
evapoMeyer = evapoMeyer_in*2.54

# units of evaporation rate in Dunne equation is in cm/day
evapoDunne = (0.013 + (0.00016*2.1*1.61*24))*actualVP_mb*((100 - RH)/100)
