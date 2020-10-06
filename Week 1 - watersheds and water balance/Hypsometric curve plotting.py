# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:59:39 2020

@author: Brian Chung
"""

import pandas as pd
import matplotlib.pyplot as py

hypsometricData = pd.read_excel("Week 1 - Hypsometric curve data.xlsx")

areaInAltRange = hypsometricData["Area within altitude range (km2)"]
cumulAreaInAltRange = hypsometricData["Cumulative area above lower altitude (km2)"]


for index, value in areaInAltRange.iteritems():
    areaValues = areaInAltRange.iloc[:index + 1]
    cumulArea = areaValues.sum()
    cumulAreaInAltRange.iloc[index] = cumulArea
    

hypsometricData["Cumulative area above lower altitude (km2)"] = cumulAreaInAltRange

totalArea = cumulAreaInAltRange.iloc[-1]

hypsometricData["Proportion of cumulative area above lower altitude (%)"] = 100*cumulAreaInAltRange/totalArea

cumulAreaInAltRange = cumulAreaInAltRange.to_numpy()
proportionCumulArea = hypsometricData["Proportion of cumulative area above lower altitude (%)"].to_numpy()
lowerAltitude = hypsometricData["Lower altitude (m)"].to_numpy()

hypsometricCurves = py.figure(figsize = (12, 15))
areaPlot = hypsometricCurves.add_subplot(2, 1, 1)
proportionPlot = hypsometricCurves.add_subplot(2, 1, 2)

areaPlot.set_title("Hypsometric curve 1: cumulative area above a given altitude")
areaPlot.set_xlabel(r"Area of watershed above a given altitude $(km^{2})$")
areaPlot.set_ylabel("Altitude (m)")
areaPlot.scatter(cumulAreaInAltRange, lowerAltitude)
areaPlot.plot(cumulAreaInAltRange, lowerAltitude)


proportionPlot.set_title("Hypsometric curve 2: proportion of cumulative area above a given altitude")
proportionPlot.set_xlabel("Proportion of watershed area above a given altitude (%)")
proportionPlot.set_ylabel("Altitude (m)")
proportionPlot.scatter(proportionCumulArea, lowerAltitude)
proportionPlot.plot(proportionCumulArea, lowerAltitude)
hypsometricCurves.savefig("Hypsometric curves for a hypothetical watershed.jpg")