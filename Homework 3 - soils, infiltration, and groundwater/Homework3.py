# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 01:41:49 2020

@author: Brian Chung
Contains my work for Homework 3
"""

import numpy as np
import infiltration as infil
# %%
# Question 1: characterizing soils

# Mass units are in grams
initSoilMass = 176
drySoilMass = 164
satSoilMass = 218
soilFieldCapaMass = 188

# a) Calculating initial gravimetric water content
# Volume units are in cubic centimeters
soilVolume = 100

initWaterMass = initSoilMass - drySoilMass
initGravWaterContent = initWaterMass/drySoilMass

# b) Calculating porosity
# Units of density: grams per cubic centimeters
waterDensity = 1
satWaterMass = satSoilMass - drySoilMass
poreSpace = satWaterMass/waterDensity
porosity = poreSpace/soilVolume

# c & d) Calculating field capacity & permanent wilting point
# Units of field capacity & permanent wilting point are cm3/cm3
fieldCapaWaterMass = soilFieldCapaMass - drySoilMass
fieldCapaWaterVolume = fieldCapaWaterMass/waterDensity
fieldCapacity = fieldCapaWaterVolume/soilVolume
permWiltPt = 0.04
avaiWater = fieldCapacity - permWiltPt
# %%
# Question 2: calculating infiltration capacity using the Horton equation
# Units of infiltration rates or capacity or rainfall rates are in cm/hr
f0 = 8
fc = 1
k = 1.1
rainfallRate = 2

# time unit is hours
stormDuration = 4

# I define the critical time as the time when infiltration rate equals
# rainfall rate. Now I'm working on b) v.
timeCrit = np.log((2 - fc)/(f0 - fc))/(-k)
maxInfilCrit = infil.totalInfilHorton1time(f0, fc, k, timeCrit)
actualInfilVolumeCrit = rainfallRate*timeCrit

totalRainAfterCrit = rainfallRate*(stormDuration - timeCrit)
totalInfilAfterCrit = infil.totalInfilHorton2time(f0, fc, k,
                                                  timeCrit, stormDuration)
totalRunoffHeight = totalRainAfterCrit - totalInfilAfterCrit

# units of area: square meters
watershedArea = 300000

# converting runoff height from centimeters to meters
totalRunoffHeight = totalRunoffHeight/100
runoffVolume = watershedArea*totalRunoffHeight
# %%
# Question 3: characterizing infiltration using the Green-Ampt model

# units of hydraulic conductivity & rainfall rate are in cm/hr
Ksat = 0.032
rainfallRate = 0.7

# unit for pressure head is cm
presHead = 20.8

# water content is unitless
thetaInit = 0.15
thetaSat = 0.5

# unit for rainfall duration is hour
rainDuration = 4

# a) Calculating Fp (total amount infiltrate by the time when ponding starts)
# and tp (the amount of time it takes before ponding begins)
Fp = infil.Fpond(presHead, Ksat, thetaSat, thetaInit, rainfallRate)
pondingTime = infil.timep(Fp, rainfallRate)

# b) Solving for: total amount of rainfall, total amount infiltrated by the end
# of the storm, total amount of runoff, infiltration rates at the beginning and
# end of the storm

totalRain = rainfallRate*rainDuration
F = 1.4
timeEnd = infil.time(pondingTime, Ksat, F, Fp, presHead, thetaSat, thetaInit)
runoffHeight = totalRain - F

initInfilRate = infil.infilRateGA(rainfallRate, Ksat, presHead, thetaSat,
                                  thetaInit, 0, 0, pondingTime)
finalInfilRate = infil.infilRateGA(rainfallRate, Ksat, presHead, thetaSat,
                                   thetaInit, F, rainDuration, pondingTime)
