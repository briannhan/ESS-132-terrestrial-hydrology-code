# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:15:59 2020

@author: Brian Chung
This script carries out my work for homework 4
"""
# Importing necessary libraries
import streamflow as sf
import pandas as pd
import matplotlib.pyplot as py
# %%
# Question 1: Soil Conservation Servation Curve Number method
# a) Calculating S, Ia, Q, etc
precip = 4.8  # inches
CNforest = 55
CNdeveloped = 98
CNlandscaping = 70
Sforest = sf.potentialMaxRetention(CNforest)
Sdeveloped = sf.potentialMaxRetention(CNdeveloped)
Slandscaping = sf.potentialMaxRetention(CNlandscaping)

IaForest = sf.initialAbstraction(Sforest)
IaDeveloped = sf.initialAbstraction(Sdeveloped)
IaLandscaping = sf.initialAbstraction(Slandscaping)

Qforest = sf.QfromP_CN(precip, CNforest)
Qdeveloped = sf.QfromP_CN(precip, CNdeveloped)
Qlandscaping = sf.QfromP_CN(precip, CNlandscaping)

# units of area are in acres
areaForestInitial = 54
areaForestFinal = 9
areaDeveloped = 36
areaLandscaping = 9

# units of volume of runoff are in acre-ft
runoffForestInitial = (Qforest/12)*areaForestInitial
runoffForestFinal = (Qforest/12)*areaForestFinal
runoffDeveloped = (Qdeveloped/12)*areaDeveloped
runoffLandscaping = (Qlandscaping/12)*areaLandscaping
totalRunoffInitial = runoffForestInitial
totalRunoffFinal = runoffForestFinal + runoffDeveloped + runoffLandscaping

# b) Calculating percent change in runoff after development
runoffChange = 100*(totalRunoffFinal - totalRunoffInitial)/totalRunoffInitial

# %%
# Question 2: Making & using a unit hydrograph to predict streamflow after
# a hypothetical storm
unitHydro = pd.read_excel(io="Homework 4 hydrograph example.xlsx",
                          sheet_name="Making unit hydrograph")
unitHydro["DataframeNum"] = 1
unitHydroCols = unitHydro.columns.tolist()
newStorm = pd.read_excel(io="Homework 4 hydrograph example.xlsx",
                         sheet_name="New storm hyetograph")
newStorm["DataframeNum"] = 2
newHyetoCols = newStorm.columns.tolist()
newHydro = pd.read_excel(io="Homework 4 hydrograph example.xlsx",
                         sheet_name="New storm hydrograph")
newHydrographColumns = newHydro.columns.tolist()
newName = "Unit hydrograph (m3/sec for 1cm of runoff)"
newColumn = {unitHydroCols[3]: newName}
unitHydro = unitHydro.rename(columns=newColumn)

# Calculating event flow
unitHydro["Event flow (m3/sec)"] = (unitHydro["Streamflow (m3/sec)"]
                                    - 50)

# Calculating the volume of runoff over the entire period of the data
Vdrh = 3600*unitHydro.groupby("DataframeNum")[unitHydroCols[2]].sum()
# Vdrh = sigma(Qdrh*deltaTime) = sigma(Qdrh*1 hr) = sigma(Qdrh*3600 s)
# Vrdh is in m3

# Calculating runoff depth
watershedArea = 324000000  # square meters
runoffDepth = float(100*Vdrh/watershedArea)  # coerced pandas series into float
# converted from meters to centimeters

# Calculating unit hydrograph
unitHydro[newName] = unitHydro[unitHydroCols[2]]/runoffDepth

# Plotting unit hydrograph
py.figure(num=1, figsize=(8, 6))
py.title("Unit hydrograph")
py.xlabel("Time (hrs)")
py.ylabel(newName)
py.plot(unitHydro["Time (hrs)"], unitHydro[newName])
py.scatter(unitHydro["Time (hrs)"], unitHydro[newName])
py.savefig("Unit hydrograph")

# Filling out the 2nd data frame, which is the hyetograph of a new storm
interval = 2  # hours
newStorm["Total rainfall (cm)"] = newStorm["Rainfall rate (cm/hr)"]*interval
totalRainfall = newStorm.groupby("DataframeNum")["Total rainfall (cm)"].sum()
totalRainfall = float(totalRainfall)

# The following calculations of infiltration follow instructions in the
# homework but they are greatly simplified due to assumptions made by the
# homework
totalInfil = totalRainfall*0.5  # infiltration is 50% of total rainfall over
# the entire storm
stormDuration = interval*4  # hours
intervalInfil = totalInfil*interval/stormDuration
newStorm[newHyetoCols[3]] = newStorm["Total rainfall (cm)"] - intervalInfil

# So it turns out that calculating the streamflow for the new storm is
# exceedingly difficult, so imma just export the first 2 dataframes into new
# Excel files and then finish the math in Excel instead
unitHydro.to_excel("Homework 4 unit hydrograph.xlsx")
newStorm.to_excel("Homework 4 new storm hyetograph.xlsx")

# Now, time to plot the modeled streamflow that I worked out in Excel
model = pd.read_excel("Homework 4 unit hydrograph - fully worked out.xlsx")
py.figure(num=2, figsize=(8, 6))
py.title("Modeled streamflow")
py.xlabel("Time (hrs)")
py.ylabel(newName)
py.plot(model["Time (hrs)"], model["Streamflow (m3/s)"])
py.scatter(model["Time (hrs)"], model["Streamflow (m3/s)"])
py.savefig("Modeled streamflow")
