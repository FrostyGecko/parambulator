#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 13:43:11 2022

@author: isaacfoster
"""
#%% Initialize
import numpy as np

#%% MATH CONSTANTS
deg2rad = np.pi/180             # [rad/deg]
rad2deg = 180/np.pi             # [deg/rad]
G       = 6.6738*(10**(-20))    # [km^3 kg^-1 s^-2]
day2sec = 24*60*60              # [sec/day]
sec2day = 1/day2sec             # [day/sec]