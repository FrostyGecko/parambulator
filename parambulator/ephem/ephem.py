#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:52:53 2024

@author: isaacfoster
"""
#%% Initialize
from jplephem.spk import SPK

#https://github.com/AndrewAnnex/SpiceyPy
#https://github.com/skyfielders/python-skyfield/
#https://space.stackexchange.com/questions/51068/is-it-posible-to-convert-jpl-horizons-vectors-to-ecef/51077?noredirect=1

#%% Defaults
spk_filepath    = 'spk_files/de440_mars.bsp'
spk_folder      = 'spk_files'

#%% General Ephemeris Functions
def eph00001_load_kernel(spk_filepath):
    '''
    

    Parameters
    ----------
    spk_filepath : TYPE
        DESCRIPTION.

    Returns
    -------
    kernel : TYPE
        DESCRIPTION.

    '''
    kernel = SPK.open(spk_filepath)
    return kernel

def eph00002_get_available_spk_files(spk_folder):
    '''
    

    Parameters
    ----------
    spk_folder : TYPE
        DESCRIPTION.

    Returns
    -------
    files : TYPE
        DESCRIPTION.

    '''
    import os
    files =  os.listdir(spk_folder)
    return files

def eph00003_print_available_spk_files(spk_folder):
    '''
    

    Parameters
    ----------
    spk_folder : TYPE
        DESCRIPTION.

    Returns
    -------
    bool
        DESCRIPTION.

    '''
    try: 
        files = eph00002_get_available_spk_files(spk_folder)
        try:
            files.remove('.DS_Store')
        except:
            pass
        print(files) 
        return True
    except:
        return False

#%% Position Functions
def eph00100_get_sun_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Sun_position : TYPE
        DESCRIPTION.

    '''
    Sun_position        = kernel[0,10].compute(julian_date)
    return Sun_position

def eph00101_get_mercury_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Mercury_position : TYPE
        DESCRIPTION.

    '''
    Mercury_position    = kernel[0,1].compute(julian_date)
    return Mercury_position

def eph00102_get_venus_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Venus_position : TYPE
        DESCRIPTION.

    '''
    Venus_position      = kernel[0,2].compute(julian_date)
    return Venus_position

def eph00103_get_earth_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Earth_position : TYPE
        DESCRIPTION.

    '''
    Earth_position      = kernel[0,3].compute(julian_date)
    Earth_position      -= kernel[3,399].compute(julian_date)
    return Earth_position

def eph00104_get_earth_barycenter_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Earth_barycenter : TYPE
        DESCRIPTION.

    '''
    Earth_barycenter      = kernel[0,3].compute(julian_date)
    return Earth_barycenter
    
def eph00105_get_mars_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Mars_position : TYPE
        DESCRIPTION.

    '''
    Mars_position       = kernel[0,4].compute(julian_date)
    return Mars_position

def eph00106_get_jupiter_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Jupiter_position : TYPE
        DESCRIPTION.

    '''
    Jupiter_position    = kernel[0,5].compute(julian_date)
    return Jupiter_position

def eph00107_get_saturn_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Saturn_position : TYPE
        DESCRIPTION.

    '''
    Saturn_position     = kernel[0,6].compute(julian_date)
    return Saturn_position

def eph00108_get_uranus_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Uranus_position : TYPE
        DESCRIPTION.

    '''
    Uranus_position     = kernel[0,7].compute(julian_date)
    return Uranus_position

def eph00109_get_neptune_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Neptune_position : TYPE
        DESCRIPTION.

    '''
    Neptune_position    = kernel[0,8].compute(julian_date)
    return Neptune_position

def eph00110_get_pluto_position_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Pluto_position : TYPE
        DESCRIPTION.

    '''
    Pluto_position      = kernel[0,9].compute(julian_date)
    return Pluto_position

#%% Velocity Functions
def eph00200_get_sun_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Sun_position : TYPE
        DESCRIPTION.

    '''
    Sun_position        = kernel[0,10].compute_and_differentiate(julian_date)
    return Sun_position

def eph00201_get_mercury_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Mercury_position : TYPE
        DESCRIPTION.

    '''
    Mercury_position    = kernel[0,1].compute_and_differentiate(julian_date)
    return Mercury_position

def eph00202_get_venus_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Venus_position : TYPE
        DESCRIPTION.

    '''
    Venus_position      = kernel[0,2].compute_and_differentiate(julian_date)
    return Venus_position

def eph00203_get_earth_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Earth_position : TYPE
        DESCRIPTION.

    '''
    Earth_position      = kernel[0,3].compute_and_differentiate(julian_date)
    Earth_position      -= kernel[3,399].compute_and_differentiate(julian_date)
    return Earth_position

def eph00204_get_earth_barycenter_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Earth_barycenter : TYPE
        DESCRIPTION.

    '''
    Earth_barycenter      = kernel[0,3].compute_and_differentiate(julian_date)
    return Earth_barycenter
    
def eph00205_get_mars_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Mars_position : TYPE
        DESCRIPTION.

    '''
    Mars_position       = kernel[0,4].compute_and_differentiate(julian_date)
    return Mars_position

def eph00206_get_jupiter_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Jupiter_position : TYPE
        DESCRIPTION.

    '''
    Jupiter_position    = kernel[0,5].compute_and_differentiate(julian_date)
    return Jupiter_position

def eph00207_get_saturn_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Saturn_position : TYPE
        DESCRIPTION.

    '''
    Saturn_position     = kernel[0,6].compute_and_differentiate(julian_date)
    return Saturn_position

def eph00208_get_uranus_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Uranus_position : TYPE
        DESCRIPTION.

    '''
    Uranus_position     = kernel[0,7].compute_and_differentiate(julian_date)
    return Uranus_position

def eph00209_get_neptune_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Neptune_position : TYPE
        DESCRIPTION.

    '''
    Neptune_position    = kernel[0,8].compute_and_differentiate(julian_date)
    return Neptune_position

def eph00210_get_pluto_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Pluto_position : TYPE
        DESCRIPTION.

    '''
    Pluto_position      = kernel[0,9].compute_and_differentiate(julian_date)
    return Pluto_position

#%% Extended Functions
def get_position_ICRF(body,julian_date,kernel):
    '''
    

    Parameters
    ----------
    body : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    match body:
        case "Sun":
            return eph00100_get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            return eph00101_get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            return eph00102_get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            return eph00103_get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            return eph00104_get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            return eph00105_get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            return eph00106_get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            return eph00107_get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            return eph00108_get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            return eph00109_get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            return eph00110_get_pluto_position_ICRF(kernel,julian_date)
        
def eph00111_get_relative_position(from_body_position,to_body_position):
    '''
    

    Parameters
    ----------
    from_body_position : TYPE
        DESCRIPTION.
    to_body_position : TYPE
        DESCRIPTION.

    Returns
    -------
    relative_position : TYPE
        DESCRIPTION.

    '''
    relative_position = to_body_position - from_body_position
    return relative_position
    
def get_relative_position_ICRF1(from_body,to_body,julian_date,kernel):
    '''
    

    Parameters
    ----------
    from_body : TYPE
        DESCRIPTION.
    to_body : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    relative_position : TYPE
        DESCRIPTION.

    '''
    match from_body:
        case "Sun":
            from_body_position = eph00100_get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            from_body_position = eph00101_get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            from_body_position = eph00102_get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            from_body_position = eph00103_get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            from_body_position = eph00104_get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            from_body_position = eph00105_get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            from_body_position = eph00106_get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            from_body_position = eph00107_get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            from_body_position = eph00108_get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            from_body_position = eph00109_get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            from_body_position = eph00110_get_pluto_position_ICRF(kernel,julian_date)
        
    match to_body:
        case "Sun":
            to_body_position = eph00100_get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            to_body_position = eph00101_get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            to_body_position = eph00102_get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            to_body_position = eph00103_get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            to_body_position = eph00104_get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            to_body_position = eph00105_get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            to_body_position = eph00106_get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            to_body_position = eph00107_get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            to_body_position = eph00108_get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            to_body_position = eph00109_get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            to_body_position = eph00110_get_pluto_position_ICRF(kernel,julian_date)
            
    #### Calculate relative position
    relative_position = to_body_position - from_body_position
    
    return relative_position

def get_relative_position_ICRF2(fromPos,to_body,julian_date,kernel):
    '''
    

    Parameters
    ----------
    fromPos : TYPE
        DESCRIPTION.
    to_body : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.
    kernel : TYPE
        DESCRIPTION.

    Returns
    -------
    relative_position : TYPE
        DESCRIPTION.

    '''
    match to_body:
        case "Sun":
            to_body_position = eph00100_get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            to_body_position = eph00101_get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            to_body_position = eph00102_get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            to_body_position = eph00103_get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            to_body_position = eph00104_get_earth_barycenter_position_ICRF(kernel,julian_date)
        case "Mars":
            to_body_position = eph00105_get_mars_position_ICRF(kernel,julian_date)
        case "Jupiter":
            to_body_position = eph00106_get_jupiter_position_ICRF(kernel,julian_date)
        case "Saturn":
            to_body_position = eph00107_get_saturn_position_ICRF(kernel,julian_date)
        case "Uranus":
            to_body_position = eph00108_get_uranus_position_ICRF(kernel,julian_date)
        case "Neptune":
            to_body_position = eph00109_get_neptune_position_ICRF(kernel,julian_date)
        case "Pluto":
            to_body_position = eph00110_get_pluto_position_ICRF(kernel,julian_date)
            
    #### Calculate relative position
    relative_position = to_body_position - fromPos
    
    return relative_position

#%% Frame Conversions