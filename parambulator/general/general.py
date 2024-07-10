#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:52:53 2024

@author: isaacfoster
"""

def InverseSquare(I0,R0,R1):
    return I0*((R0**2)/(R1**2))
    
def GravAcc(G,r,m1,m2):
    return G*(m1*m2)/(r**2)