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

def eph00002_get_available_spk_files(spk_folder,output=False):
    '''
    

    Parameters
    ----------
    spk_folder : TYPE
        DESCRIPTION.
        
    output : Bool
        If True, will print available spk files. 
        if False, will not print available spk files.
        default is False

    Returns
    -------
    files : TYPE
        DESCRIPTION.

    '''
    try: 
        import os
        files = os.listdir(spk_folder)
        spk_files = []
        for files in os.listdir(spk_folder):
            if files.endswith('.bsp'):
                spk_files.append(files)
        
        if output is True:
            print(spk_files)
    except:
        print('ERROR-eph002: Unable to get available SPK files')
    return spk_files
    
def eph00004_PrintKernel(kernel):
    try: 
        print(kernel)
    except:
        print('ERROR-eph004: Unable to print kernel.')
    return True

#%% Position Functions
def eph01000_get_sun_position_ICRF(kernel,julian_date):
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

def eph01010_get_mercury_position_ICRF(kernel,julian_date):
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
    Mercury_position    = kernel[1,199].compute(julian_date)
    return Mercury_position

def eph01020_get_venus_position_ICRF(kernel,julian_date):
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
    Venus_position      -= kernel[0,299].compute(julian_date)
    return Venus_position

def eph01030_get_earth_position_ICRF(kernel,julian_date):
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

def eph01031_get_luna_position_ICRF(kernel,julian_date):
    
    moon_position   = kernel[0,3].compute(julian_date)
    moon_position   -= kernel[3,301].compute(julian_date)
    
    return moon_position

def eph01032_get_luna_position_ECI(kernel,julian_date):

    moon_position   = kernel[3,301].compute(julian_date)
    return moon_position

def eph01040_get_earthBC_position_ICRF(kernel,julian_date):
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
    

def eph01050_get_marsBC_position_ICRF(kernel,julian_date):
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

def eph01060_get_jupiterBC_position_ICRF(kernel,julian_date):
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

def eph01070_get_saturnBC_position_ICRF(kernel,julian_date):
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

def eph01080_get_uranusBC_position_ICRF(kernel,julian_date):
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

def eph01090_get_neptuneBC_position_ICRF(kernel,julian_date):
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

def eph01100_get_plutoBC_position_ICRF(kernel,julian_date):
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
    Sun_velocity : TYPE
        DESCRIPTION.

    '''
    Sun_velocity        = kernel[0,10].compute_and_differentiate(julian_date)
    return Sun_velocity

def eph02010_get_mercury_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Mercury_velocity : TYPE
        DESCRIPTION.

    '''
    Mercury_velocity    = kernel[0,1].compute_and_differentiate(julian_date)
    return Mercury_velocity

def eph02020_get_venus_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Venus_velocity : TYPE
        DESCRIPTION.

    '''
    Venus_velocity      = kernel[0,2].compute_and_differentiate(julian_date)
    return Venus_velocity

def eph02030_get_earth_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Earth_velocity : TYPE
        DESCRIPTION.

    '''
    Earth_velocity      = kernel[0,3].compute_and_differentiate(julian_date)
    Earth_velocity      -= kernel[3,399].compute_and_differentiate(julian_date)
    return Earth_velocity

def eph02031_get_luna_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Earth_velocity : TYPE
        DESCRIPTION.

    '''
    Earth_velocity      = kernel[0,3].compute_and_differentiate(julian_date)
    Earth_velocity      -= kernel[3,301].compute_and_differentiate(julian_date)
    return Earth_velocity

def eph02032_get_luna_velocity_ECI(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Earth_velocity : TYPE
        DESCRIPTION.

    '''
    luna_velocity      = kernel[3,301].compute_and_differentiate(julian_date)
    return luna_velocity

def eph02040_get_earthBC_velocity_ICRF(kernel,julian_date):
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
    
def eph02050_get_marsBC_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Mars_velocity : TYPE
        DESCRIPTION.

    '''
    Mars_velocity       = kernel[0,4].compute_and_differentiate(julian_date)
    return Mars_velocity

def eph02060_get_jupiterBC_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Jupiter_velocity : TYPE
        DESCRIPTION.

    '''
    Jupiter_velocity    = kernel[0,5].compute_and_differentiate(julian_date)
    return Jupiter_velocity

def eph02070_get_saturnBC_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Saturn_velocity : TYPE
        DESCRIPTION.

    '''
    Saturn_velocity     = kernel[0,6].compute_and_differentiate(julian_date)
    return Saturn_velocity

def eph02080_get_uranusBC_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Uranus_velocity : TYPE
        DESCRIPTION.

    '''
    Uranus_velocity     = kernel[0,7].compute_and_differentiate(julian_date)
    return Uranus_velocity

def eph02090_Get_neptuneBC_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Neptune_velocity : TYPE
        DESCRIPTION.

    '''
    Neptune_velocity    = kernel[0,8].compute_and_differentiate(julian_date)
    return Neptune_velocity

def eph02100_get_plutoBC_velocity_ICRF(kernel,julian_date):
    '''
    

    Parameters
    ----------
    kernel : TYPE
        DESCRIPTION.
    julian_date : TYPE
        DESCRIPTION.

    Returns
    -------
    Pluto_velocity : TYPE
        DESCRIPTION.

    '''
    Pluto_velocity      = kernel[0,9].compute_and_differentiate(julian_date)
    return Pluto_velocity

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
            return eph01000_get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            return eph01010_get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            return eph01020_get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            return eph01030_get_earth_position_ICRF(kernel,julian_date)
        case "EarthBC":
            return eph01040_get_earthBC_position_ICRF(kernel,julian_date)
        case "MarsBC":
            return eph01050_get_marsBC_position_ICRF(kernel,julian_date)
        case "JupiterBC":
            return eph01060_get_jupiterBC_position_ICRF(kernel,julian_date)
        case "SaturnBC":
            return eph01070_get_saturnBC_position_ICRF(kernel,julian_date)
        case "UranusBC":
            return eph01080_get_uranusBC_position_ICRF(kernel,julian_date)
        case "NeptuneBC":
            return eph01090_get_neptuneBC_position_ICRF(kernel,julian_date)
        case "PlutoBC":
            return eph01100_get_plutoBC_position_ICRF(kernel,julian_date)
        
def eph0111_get_relative_position(from_body_position,to_body_position):
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
            from_body_position = eph01000_get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            from_body_position = eph01010_get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            from_body_position = eph01020_get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            from_body_position = eph01030_get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            from_body_position = eph01040_get_earthBC_position_ICRF(kernel,julian_date)
        case "Mars":
            from_body_position = eph01050_get_marsBC_position_ICRF(kernel,julian_date)
        case "JupiterBC":
            from_body_position = eph01060_get_jupiterBC_position_ICRF(kernel,julian_date)
        case "SaturnBC":
            from_body_position = eph01070_get_saturnBC_position_ICRF(kernel,julian_date)
        case "UranusBC":
            from_body_position = eph01080_get_uranusBC_position_ICRF(kernel,julian_date)
        case "NeptuneBC":
            from_body_position = eph01090_get_neptuneBC_position_ICRF(kernel,julian_date)
        case "PlutoBC":
            from_body_position = eph01100_get_plutoBC_position_ICRF(kernel,julian_date)
        
    match to_body:
        case "Sun":
            to_body_position = eph01000_get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            to_body_position = eph01010_get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            to_body_position = eph01020_get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            to_body_position = eph01030_get_earth_position_ICRF(kernel,julian_date)
        case "Earth Barycenter":
            to_body_position = eph01040_get_earthBC_position_ICRF(kernel,julian_date)
        case "MarsBC":
            to_body_position = eph01050_get_marsBC_position_ICRF(kernel,julian_date)
        case "JupiterBC":
            to_body_position = eph01060_get_jupiterBC_position_ICRF(kernel,julian_date)
        case "SaturnBC":
            to_body_position = eph01070_get_saturnBC_position_ICRF(kernel,julian_date)
        case "UranusBC":
            to_body_position = eph01080_get_uranusBC_position_ICRF(kernel,julian_date)
        case "NeptuneBC":
            to_body_position = eph01090_get_neptuneBC_position_ICRF(kernel,julian_date)
        case "PlutoBC":
            to_body_position = eph01100_get_plutoBC_position_ICRF(kernel,julian_date)
            
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
            to_body_position = eph01000_get_sun_position_ICRF(kernel,julian_date)
        case "Mercury":
            to_body_position = eph01010_get_mercury_position_ICRF(kernel,julian_date)
        case "Venus":
            to_body_position = eph01020_get_venus_position_ICRF(kernel,julian_date)
        case "Earth":
            to_body_position = eph01030_get_earth_position_ICRF(kernel,julian_date)
        case "EarthBC":
            to_body_position = eph01040_get_earthBC_position_ICRF(kernel,julian_date)
        case "MarsBC":
            to_body_position = eph01050_get_marsBC_position_ICRF(kernel,julian_date)
        case "JupiterBC":
            to_body_position = eph01060_get_jupiterBC_position_ICRF(kernel,julian_date)
        case "SaturnBC":
            to_body_position = eph01070_get_saturnBC_position_ICRF(kernel,julian_date)
        case "UranusBC":
            to_body_position = eph01080_get_uranusBC_position_ICRF(kernel,julian_date)
        case "NeptuneBC":
            to_body_position = eph01090_get_neptuneBC_position_ICRF(kernel,julian_date)
        case "PlutoBC":
            to_body_position = eph01100_get_plutoBC_position_ICRF(kernel,julian_date)
            
    #### Calculate relative position
    relative_position = to_body_position - fromPos
    
    return relative_position

#%% Test
if __name__ == '__main__':
    julian_date = 2460489.547616
    
    kernels     = eph00002_get_available_spk_files('spk_files/')
    for kernel in kernels:
        kernel      = eph00001_load_kernel('spk_files/de440.bsp')
        position    = kernel[0,1].compute_and_differentiate(julian_date)
        print(position)
    
    