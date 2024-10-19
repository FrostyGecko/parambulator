# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 13:05:57 2024
 
@author: fosterij
"""
#%% Initalize
import library.bodies as body

#%% Set Defaults
radius              = body.planets['earth']['radius']
mu                  = body.planets['earth']['mu']
GMAT_date_format    = "%d %b %Y %H:%M:%S.%f"
datetime_format     = "%Y-%m-%dT%H:%M:%S"