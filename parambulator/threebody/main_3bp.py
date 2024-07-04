#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 15:36:02 2022

@author: isaacfoster
"""

class celestial_object(object):
    def __init__(self,planet_dict):
        for key in planet_dict:
            setattr(self, key, planet_dict[key])
        

class ThreeBodySystem:
    class ND:
        m_star = False
        L_star = False
        u_star = False
        R_star = False
        a_star = False
        T_star = False
        G_star = False
        
    def __init__(self,body1,body2,orbiter,a):
        if body1.m > body2.m:
            self.body1      = body1
            self.body2      = body2
            self.orbiter    = orbiter
        else:
            self.body1 = body2
            self.body2 = body1
        
        self.a  = a
        
    def ConvertDimensional(self):
        import math_constants as mc
        import numpy as np
        
        u1 = self.body1.data.u
        u2 = self.body2.data.u
        
        #### Calculate non-dimensional system constants
        self.m_star  = (self.body1.u + self.body2.u)/mc.G                       # Non-dimensional mass of system         
        self.L_star  = self.a                                                   # Non-dimensional length
        self.u_star  = self.body2.m/(self.body1.m + self.body2.m)               # Non-dimensional u of system
        self.R_star  = 1                                                        # Non-dimensional distance from m1 to m2
        self.a_star  = self.R_star                                              # Non-dimensional semi-major axis from m1 to m2
        self.T_star  = np.sqrt((self.L_star**3)/(self.m_star*mc.G))             # Non-dimensional time units
        self.G_star  = (mc.G*self.m_star*(self.T_star**2))/(self.L_star**3)     # Non-dimensional gravitational constant
        self.v_star  = self.L_star/self.T_star                                  # Non-dimensional velocity
        self.n_star  = np.sqrt((self.G_star*self.m_star)/(self.L_star**3))      # Non-dimensional n
    
        #### Calculate non-dimensional system distances
        self.d1_star = self.u_star*self.R_star                                  # Non-dimensional distance from barycenter to m1
        self.d2_star = self.R_star - self.d1_star                               # Non-dimensional distance from barycenter to m2 
        self.D1_star = [-self.d1_star, 0, 0]                                    # Non-dimensional vector from barycenter to m1
        self.D2_star = [ self.d2_star, 0, 0]                                    # Non-dimensional vector from barycenter to m2
    
        self.ND.m_star = self.m_star
        
    def PrintND(self):
        if hasattr(self, 'm_star') == False:
            self.ConvertDimensional()
    
        print('System Non-Dimensional Constants')
        print('  m_star:',self.m_star)
        print('  L_star:',self.L_star)
        print('  u_star:',self.u_star)
        print('  R_star:',self.R_star)
        print('  a_Star:',self.a_star)
        print('  T_star:',self.T_star)
        
        
    def IC_nondimensionalize(self,IC_dimensional):
        #%% Extract Inputs
        x0      = IC_dimensional[0]
        y0      = IC_dimensional[1]
        z0      = IC_dimensional[2]
        xdot0   = IC_dimensional[3]
        ydot0   = IC_dimensional[4]
        zdot0   = IC_dimensional[5]
        
        # Define non-dimensional initial conditions
        x1 = x0/R;                                          # ND x position
        x2 = y0/R;                                          # ND y position
        x3 = z0/R;                                          # ND z position
        x4 = xdot0/v_star;                                  # ND x velocity
        x5 = ydot0/v_star;                                  # ND y velocity 
        x6 = zdot0/v_star;                                  # ND z velocity  
        
        # Adjust Initial Conditions to be wrt cm
        x1 = x1-d1  # Adjust initial non-dimensional x-position to make initial 
                    # position with resepct to barycenter.
        
        # Assign Output
        IC_ND = [x1, x2, x3, x4, x5, x6]
        
        class IC_ND:
            # Define non-dimensional initial conditions
            x1 = x0/R;                                          # ND x position
            x2 = y0/R;                                          # ND y position
            x3 = z0/R;                                          # ND z position
            x4 = xdot0/v_star;                                  # ND x velocity
            x5 = ydot0/v_star;                                  # ND y velocity 
            x6 = zdot0/v_star;                                  # ND z velocity  
            
        return IC_ND()


