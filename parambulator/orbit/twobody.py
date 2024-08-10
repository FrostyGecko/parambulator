#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:52:53 2024

@author: isaacfoster
"""
#%% Initialize
import numpy as np
import pandas as pd
import parambulator.data.planet_data as planet_data

#%% Constants
deg2rad     = np.pi/180  # [rad/deg]
rad2deg     = 180/np.pi  # [deg/rad]
mu_default  = planet_data.planets['earth']['mu']

#%% General
def LagrangeFG(R0,V0,delta_nu,mu=mu_default):
    
    delta_nu = delta_nu*(3.1415926/180)
    
    #### Calculate F&G parameters
    r0      = np.linalg.norm(R0)
    h       = np.linalg.norm(np.cross(R0, V0))
    v0r     = (np.dot(R0,V0))/np.linalg.norm(R0)
    r       = (h**2/mu)/(1 + (h**2/(mu*r0) - 1)*np.cos(delta_nu) - (h*v0r*np.sin(delta_nu))/mu)
    
    #### Calculate f,g,fdot,gdot
    f       = 1 - (mu*r*(1 - np.cos(delta_nu)))/(h**2)
    g       = r*r0*np.sin(delta_nu)/h
    f_dot_1 = (mu/h)*((1-np.cos(delta_nu))/np.sin(delta_nu))
    f_dot_2 = (mu/h**2)*(1 - np.cos(delta_nu)) - 1/r0 - 1/r
    f_dot   = f_dot_1*f_dot_2
    g_dot   = 1 - ((mu*r0)/h**2)*(1 - np.cos(delta_nu))
    
    FG      = pd.Series([f,g,f_dot,g_dot])
    index   = ['f','g','f_dot','g_dot']
    FG.index = index
    
    return FG

def LagrangeFG_NextState(R0,V0,FG):
    R1  = FG['f']*R0 + FG['g']*V0
    V1  = FG['f_dot']*R0 + FG['g_dot']*V0
    
    return R1, V1

def twb0000_Vescape(r_mag,mu=mu_default):
    '''
    

    Parameters
    ----------
    r_mag : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    Vescape = np.sqrt((2*mu)/r_mag)
    return Vescape

#%% Keplerian Elements
def twb00101_eccVec1(R,V,mu=mu_default):
    '''
    

    Parameters
    ----------
    R : TYPE
        DESCRIPTION.
    V : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    e_vec : TYPE
        DESCRIPTION.

    '''
    
    h_vec   = np.cross(R, V)
    e_vec   = np.cross(V,h_vec)/mu - R/np.linalg.norm(R)
    
    return e_vec

def twb00102_ecc1(R,V,mu=mu_default):
    '''
    

    Parameters
    ----------
    R : TYPE
        DESCRIPTION.
    V : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    e : TYPE
        DESCRIPTION.

    '''
    
    h_vec   = np.cross(R, V)
    e_vec   = np.cross(V,h_vec)/mu - R/np.linalg.norm(R)
    e       = np.linalg.norm(e_vec)
    return e

def twb00103_ecc2(h,r,mu):
    '''
    

    Parameters
    ----------
    h : TYPE
        DESCRIPTION.
    r : TYPE
        DESCRIPTION.
    mu : TYPE
        DESCRIPTION.

    Returns
    -------
    e : TYPE
        DESCRIPTION.

    '''
    e = ((h**2)/(mu*r) - 1)
    return e

def twb00104_ecc3(e_vec):
    '''
    

    Parameters
    ----------
    e_vec : TYPE
        DESCRIPTION.

    Returns
    -------
    e : TYPE
        DESCRIPTION.

    '''
    e = np.linalg.norm(e_vec)
    return e

def twb00105_SemiLatusRectum1(R,V,mu=mu_default):
    '''
    

    Parameters
    ----------
    R : TYPE
        DESCRIPTION.
    V : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    p : TYPE
        DESCRIPTION.

    '''
    h_vec   = np.cross(R, V)
    h_mag   = np.linalg.norm(h_vec)
    p       = (h_mag**2)/mu
    
    return p

def twb00106_SemiLatusRectum2(h,mu=mu_default):
    '''
    

    Parameters
    ----------
    h : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    p = h**2/mu
    return p

def twb00107_SemiLatusRectum3(a,e):
    '''
    

    Parameters
    ----------
    a : TYPE
        DESCRIPTION.
    e : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    p = a*(1-e**2)
    return p

    
def twb00108_SemiMajorAxis1(specific_energy,mu=mu_default):
    '''
    

    Parameters
    ----------
    specific_energy : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    a = -mu/(2*specific_energy)
    return a

def twb00109_Period(a,mu=mu_default):
    '''
    

    Parameters
    ----------
    a : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    P = (2*np.pi*(a**(3/2)))/np.sqrt(mu)
    return P

def twb00110_SpecificEnergy1(R,V,mu=mu_default):
    '''
    

    Parameters
    ----------
    R : TYPE
        DESCRIPTION.
    V : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    E : TYPE
        DESCRIPTION.

    '''
    r = np.linalg.norm(R)
    v = np.linalg.norm(V)
    
    E = (v**2)/2 - mu/r
    return E

def twb00110_SpecificEnergy2(r,v,mu=mu_default):
    '''
    

    Parameters
    ----------
    v : TYPE
        DESCRIPTION.
    r : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    E = (v**2)/2 - mu/r
    return E

def twb00111_PeriapsisMag(R,V,mu=mu_default):
    
    e_vec           = twb00101_eccVec1(R,V,mu)
    e               = np.linalg.norm(e_vec)
    r               = np.linalg.norm(R)
    v               = np.linalg.norm(V)
    specific_energy = (v**2/2) - mu/r
    a               = -mu/(2*specific_energy)
    p_hat           = e_vec/np.linalg.norm(e_vec)
    r_p             = a*(1-e)*p_hat
    
    return r_p

def twb00112_ApoapsisMag(R,V,mu=mu_default):
    
    e_vec           = twb00101_eccVec1(R,V,mu)
    e               = np.linalg.norm(e_vec)
    r               = np.linalg.norm(R)
    v               = np.linalg.norm(V)
    specific_energy = (v**2/2) - mu/r
    a               = -mu/(2*specific_energy)
    p_hat           = e_vec/np.linalg.norm(e_vec)
    r_a             = -a*(1+e)*p_hat
    
    return r_a

def twb00111_CartToKepler(R,V,mu=mu_default):
    '''
    

    Parameters
    ----------
    R : TYPE
        DESCRIPTION.
    V : TYPE
        DESCRIPTION.
    mu : TYPE, optional
        DESCRIPTION. The default is mu_default.

    Returns
    -------
    kep_elements : TYPE
        DESCRIPTION.

    '''
    
    r               = np.linalg.norm(R)
    v               = np.linalg.norm(V)
    H               = np.cross(R,V)
    h               = np.linalg.norm(H)
    e_vec           = twb00101_eccVec1(R,V,mu)
    scriptE         = twb00110_SpecificEnergy2(r,v)
    a               = twb00108_SemiMajorAxis1(scriptE,mu)
    i               = np.arccos(H[2]/h)
    e               = twb00103_ecc2(h,r,mu)   
    p               = twb00106_SemiLatusRectum2(h,mu)
    P               = twb00109_Period(a,mu)
    r_p             = a*(1- e)
    r_a             = a*(1+e)
    K               = np.array([0,0,1])
    N               = np.cross(K,H)
    n               = np.linalg.norm(N)
    
    #### Right Ascension of the Ascending Node
    RAAN            = np.arccos(N[0]/n)
    
    if N[1] > 0:
        RAAN        = np.pi - RAAN
        
    #### Argument of Periapsis
    omega           = np.arccos(np.dot(N,e_vec)/(n*e))
    
    #### True Anomaly
    if e_vec[2] > 0:
        omega       = 2*np.pi - omega
    
    e_vec_dot_R     = np.dot(e_vec,R)
    nu              = np.arccos(e_vec_dot_R/(e*r))
    
    #### Argument of Latitude at Epoch
    if e_vec_dot_R > 0:
        nu          = 2*np.pi - nu
    
    arg_lat_epoch   = np.arccos(np.dot(N,R)/(n*r))
    
    #### True Longitude at Epoch
    if R[2] > 0:
        arg_lat_epoch = 2*np.pi - arg_lat_epoch
        
    true_long_epoch   = RAAN+omega+nu
    
    #### Compile Keplerian Elements
    kep_elements  = {
                'a':                a,
                'e':                e,
                'i':                i*rad2deg,
                'RAAN':             RAAN*rad2deg,
                'omega':            omega*rad2deg,
                'nu':               nu*rad2deg,
                'P':                P,
                'e_vec':            e_vec,
                'specific_energy':  scriptE,
                'p':                p,
                'h':                h,
                'r_p':              r_p,
                'r_a':              r_a,
                'arg_lat_epoch':    arg_lat_epoch*rad2deg,
                'true_long_epoch':  true_long_epoch*rad2deg,
                
        }

    return kep_elements

#%% Two Body Orbit Vectors
def twb00201_NodeVector1(R,V):
    '''
    

    Parameters
    ----------
    R : TYPE
        DESCRIPTION.
    V : TYPE
        DESCRIPTION.

    Returns
    -------
    N : TYPE
        DESCRIPTION.

    '''
    h_vec   = np.cross(R, V)
    K       = np.array([0,0,1])
    N       = np.cross(K,h_vec)
    
    return N

def twb00204_OrbitNormalVector2(RAAN,inc):
    
    RAAN    = np.deg2rad(RAAN)
    inc     = np.deg2rad(inc)
    
    A = np.matrix([[np.cos(RAAN), -np.sin(RAAN),  0],
                   [np.sin(RAAN), np.cos(RAAN),   0],
                   [0,           0,               1]])
   
    B = np.matrix([[1, 0, 0],
                   [0, np.cos(inc), -np.sin(inc)],
                   [0, np.sin(inc), np.cos(inc)]])
   
    n = np.matrix([[0],
                   [0],
                   [1]])
                   
    O_hat = A @ B @ n
    
    return O_hat