#%% Initialize
import numpy as np
import matplotlib.pyplot as plt 
import os
import seaborn as sb

#### Set Printing
np.set_printoptions(suppress=True, precision=6)

#### Import Orbit Dependancies
from jplephem.spk import SPK
import juliandate as jd
import astropy as ap
from astropy.time import Time

#### System Clear
try:
    os.system('clear')
    plt.close("all")
except:  
    pass

#%% Get SPK File Location
spk_filepath = 'data/spk_files/de440_mars.bsp'
spk_filepath = 'data/spk_files/de421.bsp'

#https://github.com/AndrewAnnex/SpiceyPy
#https://github.com/skyfielders/python-skyfield/
#https://space.stackexchange.com/questions/51068/is-it-posible-to-convert-jpl-horizons-vectors-to-ecef/51077?noredirect=1

deg2rad = np.pi/180
rad2deg = 1/deg2rad

#%% Get Ephemeris using jplephem
# https://pypi.org/project/jplephem/

def load_kernel(spk_filepath):
    return SPK.open(spk_filepath)

kernel = load_kernel(spk_filepath)

def get_sun_position_ICRF(kernel,julian_date):
    Sun_position        = kernel[0,10].compute(julian_date)
    return Sun_position

def get_mercury_position_ICRF(kernel,julian_date):
    Mercury_position    = kernel[0,1].compute(julian_date)
    return Mercury_position

def get_venus_position_ICRF(kernel,julian_date):
    Venus_position      = kernel[0,2].compute(julian_date)
    return Venus_position

def get_earth_position_ICRF(kernel,julian_date):
    Earth_position      = kernel[0,3].compute(julian_date)
    Earth_position      -= kernel[3,399].compute(julian_date)
    return Earth_position

def get_earth_barycenter_position_ICRF(kernel,julian_date):
    Earth_barycenter      = kernel[0,3].compute(julian_date)
    return Earth_barycenter
    
def get_mars_position_ICRF(kernel,julian_date):
    Mars_position       = kernel[0,4].compute(julian_date)
    return Mars_position

def get_jupiter_position_ICRF(kernel,julian_date):
    Jupiter_position    = kernel[0,5].compute(julian_date)
    return Jupiter_position

def get_saturn_position_ICRF(kernel,julian_date):
    Saturn_position     = kernel[0,6].compute(julian_date)
    return Saturn_position

def get_uranus_position_ICRF(kernel,julian_date):
    Uranus_position     = kernel[0,7].compute(julian_date)
    return Uranus_position

def get_neptune_position_ICRF(kernel,julian_date):
    Neptune_position    = kernel[0,8].compute(julian_date)
    return Neptune_position

def get_pluto_position_ICRF(kernel,julian_date):
    Pluto_position      = kernel[0,9].compute(julian_date)
    return Pluto_position


#### Get Velocity
def get_sun_velocity_ICRF(kernel,julian_date):
    Sun_position        = kernel[0,10].compute_and_differentiate(julian_date)
    return Sun_position

def get_mercury_velocity_ICRF(kernel,julian_date):
    Mercury_position    = kernel[0,1].compute_and_differentiate(julian_date)
    return Mercury_position

def get_venus_velocity_ICRF(kernel,julian_date):
    Venus_position      = kernel[0,2].compute_and_differentiate(julian_date)
    return Venus_position

def get_earth_velocity_ICRF(kernel,julian_date):
    Earth_position      = kernel[0,3].compute_and_differentiate(julian_date)
    Earth_position      -= kernel[3,399].compute_and_differentiate(julian_date)
    return Earth_position

def get_earth_barycenter_velocity_ICRF(kernel,julian_date):
    Earth_barycenter      = kernel[0,3].compute_and_differentiate(julian_date)
    return Earth_barycenter
    
def get_mars_velocity_ICRF(kernel,julian_date):
    Mars_position       = kernel[0,4].compute_and_differentiate(julian_date)
    return Mars_position

def get_jupiter_velocity_ICRF(kernel,julian_date):
    Jupiter_position    = kernel[0,5].compute_and_differentiate(julian_date)
    return Jupiter_position

def get_saturn_velocity_ICRF(kernel,julian_date):
    Saturn_position     = kernel[0,6].compute_and_differentiate(julian_date)
    return Saturn_position

def get_uranus_velocity_ICRF(kernel,julian_date):
    Uranus_position     = kernel[0,7].compute_and_differentiate(julian_date)
    return Uranus_position

def get_neptune_velocity_ICRF(kernel,julian_date):
    Neptune_position    = kernel[0,8].compute_and_differentiate(julian_date)
    return Neptune_position

def get_pluto_velocity_ICRF(kernel,julian_date):
    Pluto_position      = kernel[0,9].compute_and_differentiate(julian_date)
    return Pluto_position



def get_solar_vector(body_position,julian_date,kernel):
    sun_position        = get_sun_position_ICRF(kernel,julian_date)
    relative_position   = -sun_position + body_position
    return relative_position


def get_position_ICRF(body,julian_date,kernel):
    match body:
        case "Sun":
            return get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            return get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            return get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            return get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            return get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            return get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            return get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            return get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            return get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            return get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            return get_pluto_position_ICRF(kernel,julian_date)
    
def get_relative_position_ICRF(from_body,to_body,julian_date,kernel):
    match from_body:
        case "Sun":
            from_body_position = get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            from_body_position = get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            from_body_position = get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            from_body_position = get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            from_body_position = get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            from_body_position = get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            from_body_position = get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            from_body_position = get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            from_body_position = get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            from_body_position = get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            from_body_position = get_pluto_position_ICRF(kernel,julian_date)
        
    match to_body:
        case "Sun":
            to_body_position = get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            to_body_position = get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            to_body_position = get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            to_body_position = get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            to_body_position = get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            to_body_position = get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            to_body_position = get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            to_body_position = get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            to_body_position = get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            to_body_position = get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            to_body_position = get_pluto_position_ICRF(kernel,julian_date)
            
    #### Calculate relative position
    relative_position = to_body_position - from_body_position
    
    return relative_position


def beta_angle_psi(RAAN_deg,inc_deg,obliquity_deg,Gamma_deg):
    RAAN        = RAAN_deg*deg2rad
    inc         = inc_deg*deg2rad
    obliquity   = obliquity_deg*deg2rad
    Gamma       = Gamma_deg*deg2rad
    
    psi = np.arccos(np.cos(Gamma)*np.sin(RAAN)*np.sin(inc) - np.sin(Gamma)*np.cos(obliquity)*np.cos(RAAN)*np.sin(inc) + np.sin(Gamma)*np.sin(obliquity)*np.cos(inc))
    
    beta = psi - np.pi/2
    return beta*rad2deg
    

def beta_angle_dec(RAAN_earth_deg,inc_deg,RAAN_sun_deg,solar_declension_deg):
    RAAN_earth          = RAAN_earth_deg*deg2rad
    inc                 = inc_deg*deg2rad
    RAAN_sun            = RAAN_sun_deg*deg2rad
    solar_declension    = solar_declension_deg*deg2rad

    beta = np.sin(np.cos(solar_declension)*np.sin(inc)*np.sin(RAAN_earth-RAAN_sun) + np.sin(solar_declension)*np.cos(inc))
    return beta*rad2deg

def beta_angle_solar_vector(RAAN_earth,inc_deg,solar_vector):
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

RAAN_deg        = 30
inc_deg         = 40

orbit_time      = Time('2023-8-20 12:00:00', scale='utc')
julian_date     = orbit_time.jd

body_position   = get_earth_position_ICRF(kernel,julian_date)
solar_vector    = get_solar_vector(body_position,julian_date,kernel)

print(beta_angle_solar_vector(RAAN_deg,inc_deg,solar_vector))
    