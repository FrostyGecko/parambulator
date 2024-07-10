#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:52:53 2024

@author: isaacfoster
"""

#%% Initialize
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#### Set Printing
np.set_printoptions(suppress=True, precision=6)

#### Import Orbit Dependancies
from jplephem.spk import SPK
import astropy
from astropy.coordinates import get_sun

#%% Get SPK File Location
spk_filepath = 'de421.bsp'

#https://github.com/AndrewAnnex/SpiceyPy
#https://github.com/skyfielders/python-skyfield/
#https://space.stackexchange.com/questions/51068/is-it-posible-to-convert-jpl-horizons-vectors-to-ecef/51077?noredirect=1

deg2rad = np.pi/180
rad2deg = 1/deg2rad

#%% Get Ephemeris using jplephem
# https://pypi.org/project/jplephem/

def load_kernel(spk_filepath):
    return SPK.open(spk_filepath)

def get_sun_position_ICRF(kernel,julian_date):
    Sun_position        = kernel[0,10].compute(julian_date)
    return Sun_position

def get_earth_position_ICRF(kernel,julian_date):
    Earth_position      = kernel[0,3].compute(julian_date)
    Earth_position      -= kernel[3,399].compute(julian_date)
    return Earth_position

def get_solar_vector(body_position,julian_date,kernel):
    sun_position        = get_sun_position_ICRF(kernel,julian_date)
    relative_position   = -sun_position + body_position
    return relative_position


#%% Beta Angle Functions
def beta_angle_psi(RAAN_deg,inc_deg,obliquity_deg,Gamma_deg):
    RAAN        = RAAN_deg*deg2rad
    inc         = inc_deg*deg2rad
    obliquity   = obliquity_deg*deg2rad
    Gamma       = Gamma_deg*deg2rad
   
    psi = np.arccos(np.cos(Gamma)*np.sin(RAAN)*np.sin(inc) - np.sin(Gamma)*np.cos(obliquity)*np.cos(RAAN)*np.sin(inc) + np.sin(Gamma)*np.sin(obliquity)*np.cos(inc))
   
    beta = psi - np.pi/2
    return beta*rad2deg
   
def beta_angle_dec(RAAN_deg,inc_deg,RAAN_sun_deg,solar_declension_deg):
    RAAN                = RAAN_deg*deg2rad
    inc                 = inc_deg*deg2rad
    RAAN_sun            = RAAN_sun_deg*deg2rad
    solar_declension    = solar_declension_deg*deg2rad

    beta = np.arcsin(np.cos(solar_declension)*np.sin(inc)*np.sin(RAAN-RAAN_sun) + np.sin(solar_declension)*np.cos(inc))
    return beta*rad2deg

def beta_angle_solar_vector(RAAN_deg,inc_deg,solar_vector):
    RAAN    = RAAN_deg*deg2rad
    inc     = inc_deg*deg2rad
   
    sum_squares = sum([solar_vector[0]**2, solar_vector[1]**2, solar_vector[2]**2])
    S_mag       = sum_squares ** 0.5 #position vector
   
    Sx_hat  = solar_vector[0]/S_mag
    Sy_hat  = solar_vector[1]/S_mag
    Sz_hat  = solar_vector[2]/S_mag
   
    xcom = np.sin(RAAN)*np.sin(inc)*Sx_hat
    ycom = np.cos(RAAN)*np.sin(inc)*Sy_hat
    zcom = np.cos(inc)*Sz_hat
   
    beta = np.arccos(xcom-ycom+zcom) - np.pi/2
   
    return beta*rad2deg


def delta_RAAN(radius,a,e,i):
    J2      = 1.08262668e-3     # J2 constant
    dRAAN   = (-3*np.sqrt(mu)*radius**2*J2*np.cos(i*deg2rad))/(2*a**(7/2))
    
    ## Vellado??
    ## https://strathprints.strath.ac.uk/71130/1/McGrath_Macdonald_JGCD_2020_General_perturbation_method_for_satellite_constellation_deployment.pdf 
    
    return dRAAN*rad2deg

#%% Variable Definition
# Setting variables for the beta angle analysis. All variables defined in radians

kernel      = load_kernel(spk_filepath)  # Load spk kernel

eps         = 23.44*deg2rad     # obliquity of the ecliptic
R_earth     = 6378              # radius of earth in km
mu          = 398600.44189

start_date  = astropy.time.Time('2024-9-22')
num_days    = 365

# setting parameters for the example orbit of the ISS - this could be done differently
# depending which ones you know
i_start     = 51.6405
RAAN_start  = 0
e_start     = 0.0
a_start     = 6778

#%% For Loop
#creating variables that go within the loop
#setting the time to fall equinox
raan_list                   = []
beta_declension_list        = []
beta_rickmans_method_list   = []
RAAN                        = RAAN_start
i_rad                       = i_start*deg2rad

# Iterate through each day to find Beta
for i,day in enumerate(range(0,num_days)):
    current_date = start_date + day
   
    #### Update RAAN
    dRAAN           = delta_RAAN(R_earth,a_start,e_start,i_start)*86400
    RAAN            = RAAN + dRAAN
    RAAN_rad        = RAAN*deg2rad
    raan_list.append(RAAN)
    
    #### Rickman Method Using original orbit equations
    
    
    
    #### Rickman Method Using SPK Files
    julian_date     = current_date.jd
    body_position   = get_earth_position_ICRF(kernel,julian_date)
    solar_vector    = get_solar_vector(body_position,julian_date,kernel)
    beta_rickmans_method = beta_angle_solar_vector(RAAN,i_start, solar_vector)
    beta_rickmans_method_list.append(beta_rickmans_method)
   
    #### Declension Method
    sun                 = get_sun(current_date)
    sun_declension      = sun.dec.degree
    sun_RA              = sun.ra.degree
    beta_dec_method_degrees = beta_angle_dec(RAAN,i_start,sun_RA,sun_declension)
    beta_declension_list.append(beta_dec_method_degrees)
   

#### Convert Lists
beta_declension_array       = np.asarray(beta_declension_list)
beta_rickmans_method_array  = np.asarray(beta_rickmans_method_list)
raan_array                  = np.asarray(raan_list)

#load excel data
DH_file_path    = "beta_angle.xlsx"
DH_excel_data   = pd.read_excel(DH_file_path, sheet_name='Beta Angle Calculator')
DH_beta_column  = DH_excel_data.iloc[:, 29]
beta_angle_DH   = DH_beta_column.iloc[6:372]

#%% Plot
# Plot the data
time = np.arange(0, 365)
plt.plot(time, beta_angle_DH, label = 'DH file')
plt.plot(time, beta_declension_array, label = 'Declension Method (STCH)')
plt.plot(time, beta_rickmans_method_array, label = 'Rickman method',linestyle = '--')
plt.title('Plot of Beta Angle Calculations Over One Year')
plt.xlabel('Days of the Year')
plt.ylabel('Beta Angle')
plt.legend()
plt.grid()
plt.show()

