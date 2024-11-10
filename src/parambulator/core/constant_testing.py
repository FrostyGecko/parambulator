#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:24:15 2024

@author: isaacfoster
"""

from constant import constant

#### Define Radiator Area
panel_length    = constant(0.5,0.0005,'m')
panel_width     = constant(0.5,0.0005,'m')

panel_area      = panel_length*panel_width

#### Define Radiator emissivity
panel_epsilon   = constant(0.8,0.02)

#### Define Temperatures

panel_temp_1    = constant(301,0.2,'K')
panel_temp_2    = constant(299,0.2,'K')
panel_temp_3    = constant(298,0.2,'K')
panel_temp_4    = constant(300,0.2,'K')

panel_temp_avg  = (panel_temp_1+panel_temp_2+panel_temp_3+panel_temp_4)/4
sink_temp       = constant(170,2,'K')

#### Define supporting constant
sigma   = constant(
                    abbrev          = 'sigma',
                    name            = 'Stefan-Boltzmann constant', 
                    value           = 5.670374419*(10**(-8)),
                    uncertainty     = 0,
                    unit            = 'W/(m^2*K^4)',
                    value_ref       = 'NIST',
                    value_ref_link  = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma',
                    u_ref           = 'NIST',
                    u_ref_link      = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma'
                   )
Q_radiated = sigma*panel_area*panel_epsilon*(panel_temp_avg**4 - sink_temp**4)
              
#### Example Calculation
print(f"Q radiated = {Q_radiated}")


#### Changing Units
# panel_area.unit = "in^2" 

#### Sampling
# panel_area.sample_gauss