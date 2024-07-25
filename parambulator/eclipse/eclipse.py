#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:13:10 2024

@author: isaacfoster
"""

#%% Initialize
import numpy as np
import parambulator.ephem.ephem as eph

#%% Functions
def EclipseType(P1,P2,P3,r1,r2): 
    '''
    Source: https://celestrak.org/columns/v03n01/

    Parameters
    ----------
    P1 : TYPE
        DESCRIPTION.
    P2 : TYPE
        DESCRIPTION.
    P3 : TYPE
        DESCRIPTION.
    r1 : TYPE
        DESCRIPTION.
    r2 : TYPE
        DESCRIPTION.

    Returns
    -------
    eclipseType : TYPE
        DESCRIPTION.
    theta : TYPE
        DESCRIPTION.
    theta1 : TYPE
        DESCRIPTION.
    theta2 : TYPE
        DESCRIPTION.

    '''
    #### Calculate Vectors
    R31     = P1 - P3
    R21     = P1 - P2
    R32     = P2 - P3
    
    #### Calculate Distances
    D31     = np.sqrt(sum(R31**2))
    D21     = np.sqrt(sum(R21**2))
    D32     = np.sqrt(sum(R32**2))
    
    #### Calculate Angular Radii
    theta   = np.arccos((np.dot(R32,R31))/(D32*D31))
    theta1  = np.arcsin(r1/D31)
    theta2  = np.arcsin(r2/D32)
    
    #### Calculate Eclipse Type
    if D31 < D21:
        eclipseType     = -1
        print('Object inbetween bodies in question')
    else:
        if theta < (theta2 - theta1):
            eclipseType = 3
            print('Eclipse Type: umbra')
        elif abs(theta2 - theta1) < theta < (theta1 + theta2):
            eclipseType = 2
            print('Eclipse Type: penumbral eclipse')
        elif theta < (theta1 - theta2):
            print('Eclipse Type: penumbral, annular')
            eclipseType = 1
        else:
            print('Eclypse Type: Sunlit')
            eclipseType = 0  
            
    return eclipseType, theta, theta1, theta2

def OcclusionPercentage(theta,theta1,theta2):
    '''
    
    Source: https://dassencio.org/102

    Parameters
    ----------
    theta : TYPE
        DESCRIPTION.
    theta1 : TYPE
        DESCRIPTION.
    theta2 : TYPE
        DESCRIPTION.

    Returns
    -------
    occ_per : TYPE
        DESCRIPTION.

    '''
    #### Assign Effective Circle Parameters
    Delta   = theta
    alpha1  = theta1
    alpha2  = theta2

    A1      = np.pi*(alpha1)**2
           
    if alpha1 >= alpha2:
        pass
    else:
        r_big = alpha2
        r_small = alpha1
        
        alpha1 = r_big
        alpha2 = r_small

    #### Calculate Circle Occlusion Widths
    if theta == 0:
        Delta1 = 0
        Delta2 = 0
    else: 
        Delta1  = (alpha1**2 - alpha2**2 + Delta**2)/(2*Delta)
        Delta2  = Delta - Delta1

    #### Calculate Intersection Area
    if alpha1 < alpha2:
        print('WARNING: r1 < r2')
        A_int   = 0
    elif Delta >= (alpha1 + alpha2):
        print('Delta >= alpha1 + alpha2')
        A_int   = 0
    elif Delta <= (alpha1 - alpha2):
        print('Delta <= alpha1 - alpha2')
        A_int   = np.pi*(alpha2**2)
    else:
        A_int   = (alpha1**2 * np.arccos(Delta1/alpha1)) + (alpha2**2 * np.arccos(Delta2/alpha2)) - Delta1*np.sqrt(alpha1**2 - Delta1**2) - Delta2*np.sqrt(alpha2**2 - Delta2**2) 
        
    occ_per = (A_int/A1)*100
        
    print('Occlusion%: '+str(occ_per))
    
    return occ_per


def ecl00000_EclipseEC1(P1,P2,P3,r1,r2):
    
    eclipseType, theta, theta1, theta2 = EclipseType(P1,P2,P3,r1,r2)
    occlusion = OcclusionPercentage(theta,theta1,theta2)
    
    return eclipseType, occlusion

def ecl00000_EclipseEC2(body1,body2,SCpos):
    
    import parambulator.data.planet_data as planet_data
    import parambulator.ephem.ephem as eph
    
    r1  = planet_data[body1]['radius']
    r2  = planet_data[body2]['radius']
    P1  = eph.get_position_ICRF[body1]
    P2  = eph.get_position_ICRF[body2]
    eclipseType, theta, theta1, theta2 = EclipseType(P1,P2,SCpos,r1,r2)
    occlusion = OcclusionPercentage(theta,theta1,theta2)
    
    return eclipseType, occlusion
    
def EclipseGeometry(P1,P2,P3,r1,r2):
    #### Calculate Vectors
    R31     = P1 - P3
    R21     = P1 - P2
    R32     = P2 - P3
    
    #### Calculate Distances
    D31     = np.sqrt(sum(R31**2))
    D21     = np.sqrt(sum(R21**2))
    D32     = np.sqrt(sum(R32**2))
    
    #### Calculate Angular Radii
    theta   = np.arccos((np.dot(R32,R31))/(D32*D31))
    theta1  = np.arcsin(r1/D31)
    theta2  = np.arcsin(r2/D32)
    
    #### Calculate Eclipse Geometry
    d1      = np.sqrt( (np.tan(theta1)**2 - r1**2) / ( (1/(D31**2)) -1 ) )
    d2      = np.sqrt( (np.tan(theta2)**2 - r2**2) / ( (1/(D32**2)) -1 ) )
    d31     = D31 - np.sqrt(r1**2 - d1**2)
    d32     = D32 - np.sqrt(r2**2 - d2**2)
    d       = np.sin(theta)*D32
    s       = np.cos(theta)*D32
    
    
if __name__ == '__main__':
    
    try:
        import os
        import matplotlib.pyplot as plt
        os.system('clear')
        print('----Program Start----')
        plt.close("all")
    except:  
        pass
    
    #### Constants
    SunRadius       = 695700
    EarthRadius     = 6378.165
    deg2rad         = np.pi/180
    rad2deg         = 180/np.pi
    
    #### Positions
    SunPos          = np.array([0,0,0])
    EarthPos        = np.array([-147000000,0,0])
    SatPos          = np.array([-7000,600,0]) + EarthPos
    
    #### Calculate Eclipse
    eclipseType,theta,theta1,theta2 = EclipseType(SunPos,EarthPos,SatPos,SunRadius,EarthRadius)
    occ_per     = OcclusionPercentage(theta, theta1, theta2)
        

    