#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 14:04:23 2024

@author: isaacfoster
"""
import matplotlib.pyplot as plt
import library.bodies as body
from utilities.gmat import *
from utilities.eclipse import *
from utilities.timekeeper import*

dataframe       = gmt0001_ImportGMAT_Textfile('ISS_positions.txt')
gmat_eclipse    = gmt0103_ImportEclipseFile('ISS_eclipse.txt')
columns         = dataframe.columns

objects,variables = gmt0002_InspectColumns(columns)

unix            = gmt0004_ExtractTime(dataframe)
dates           = dataframe["ISS.UTCGregorian"]

#### Extract Object DAta
SunData         = gmt0101_ExtractBodyData(dataframe,'Sun')
EarthData       = gmt0101_ExtractBodyData(dataframe,'Earth')
ISSData         = gmt0101_ExtractBodyData(dataframe,'ISS')

#### Extract Position Data
Sun_positions   = gmt0102_ExtractPositionData(SunData)
Earth_positions = gmt0102_ExtractPositionData(EarthData)
ISS_positions   = gmt0102_ExtractPositionData(ISSData)


SunRadius       = body.planets['sun']['radius']
EarthRadius     = body.planets['earth']['radius']

eclipseType_vec = []

for i in range(0,len(unix)):
    eclipseType,theta,theta1,theta2 = EclipseType(Sun_positions.iloc[i,:],
                                                  Earth_positions.iloc[i,:],
                                                  ISS_positions.iloc[i,:],
                                                  SunRadius,
                                                  EarthRadius,
                                                  verbose=False)
    
    eclipseType_vec.append(eclipseType)
    
    