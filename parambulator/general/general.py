#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:52:53 2024

@author: isaacfoster
"""

def gen0000_InverseSquare(I0,R0,R1):
    '''
    

    Parameters
    ----------
    I0 : TYPE
        DESCRIPTION.
    R0 : TYPE
        DESCRIPTION.
    R1 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return I0*((R0**2)/(R1**2))
    
def gen0000_GravAcc(G,r,m1,m2):
    '''
    

    Parameters
    ----------
    G : TYPE
        DESCRIPTION.
    r : TYPE
        DESCRIPTION.
    m1 : TYPE
        DESCRIPTION.
    m2 : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    return G*(m1*m2)/(r**2)