# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 10:06:39 2020

@author: Brian Chung
Contains my work for the week 7 discussion section
"""

import infiltration as infil
import scipy.optimize as opti
import matplotlib.pyplot as py

# Units of time are in hours
stormDuration = 3

# Units of flow are in cm and flow rates are in cm/hr
precipRate = 0.6
Ksat = 0.1
presHead = 15

# Units of water content are cm3/cm3
initContent = 0.15
satContent = 0.5

Fp = infil.Fpond(presHead, Ksat, satContent, initContent, precipRate)
pondingTime = infil.timep(Fp, precipRate)


def stormEndOptimize(totalInfiltration):
    """Gets plugged into root-finding algorithms to be optimized to solve
    for the amount of infiltration at the end
    """
    time = infil.stormEnd(pondingTime, Ksat, totalInfiltration, Fp, presHead,
                          satContent, initContent, stormDuration)
    return time


rootResults = opti.root(stormEndOptimize, 1.66)
endingInfiltrationTotal = float(rootResults.x)
endingInfilRate = infil.infilRateGA(Ksat, presHead, satContent, initContent,
                                    endingInfiltrationTotal, pondingTime)
infilAfterPonding = endingInfiltrationTotal - Fp
totalRain = precipRate*stormDuration
runOff = totalRain - endingInfiltrationTotal

# Making numpy 2-D arrays to graph infiltration rates vs time
plotValues = infil.graphData(endingInfiltrationTotal, precipRate, Ksat,
                             presHead, satContent, initContent)

# Making the infiltration rate vs time plot
greenAmptFigure = py.figure(num=1, figsize=(8, 4))
greenAmptSubplot = greenAmptFigure.add_subplot(1, 1, 1)
figureTitle = "Infiltration rate, Green-Ampt model, week 7 discussion"
figureXaxis = "Time (hours)"
figureYaxis = "Infiltration rate (cm/hr)"
greenAmptSubplot.set_title(figureTitle)
greenAmptSubplot.set_xlabel(figureXaxis)
greenAmptSubplot.set_ylabel(figureYaxis)
greenAmptSubplot.plot(plotValues[0, :], plotValues[1, :])
greenAmptFigure.savefig("Week 7 discussion infiltration rate plot.jpg")
