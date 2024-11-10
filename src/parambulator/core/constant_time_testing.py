#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 23:16:24 2024

@author: isaacfoster
"""

from uncertainties import ufloat
import numpy as np
import time
import constant as constant
from uncertainties import unumpy as unp
from pint import UnitRegistry
ureg = UnitRegistry()

#%% 1
a = 3
b = 3
n = 50000
time_vec = np.zeros(n)

for i in range(n):
    t1 = time.time()
    c = a*b
    c = a/b
    c = np.cos(c)
    t2 = time.time()
    time_vec[i] = t2-t1

time1 = np.mean(time_vec)

#%% 2
a = ufloat(3, 0.2)
b = ufloat(3, 0.2)
time_vec = np.zeros(n)

for i in range(n):
    t1 = time.time()
    c = a*b
    c = a/b
    c = unp.cos(c)
    t2 = time.time()
    time_vec[i] = t2-t1

time2 = np.mean(time_vec)

#%% 3
a = ufloat(3, 0.2)*ureg('m')
b = ufloat(3, 0.2)*ureg('m')
time_vec = np.zeros(n)

for i in range(n):
    t1 = time.time()
    c = a*b
    c = a/b
    c = unp.cos(c)
    
    t2 = time.time()
    time_vec[i] = t2-t1

time3 = np.mean(time_vec)

#%% 4
a   = constant.constant(
                    abbrev          = 'sigma',
                    name            = 'Stefan-Boltzmann constant',
                    value           = 3,
                    uncertainty     = 0.2,
                    unit            = 'W/(m^2*K^4)',
                    value_ref       = 'NIST',
                    value_ref_link  = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma',
                    u_ref           = 'NIST',
                    u_ref_link      = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma'
                   )

b   = constant.constant(
                    abbrev          = 'sigma',
                    name            = 'Stefan-Boltzmann constant',
                    value           = 3,
                    uncertainty     = 0.2,
                    unit            = 'W/(m^2*K^4)',
                    value_ref       = 'NIST',
                    value_ref_link  = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma',
                    u_ref           = 'NIST',
                    u_ref_link      = 'https://physics.nist.gov/cgi-bin/cuu/Value?sigma'
                   )

time_vec = np.zeros(n)

for i in range(n):
    t1 = time.time()
    c = a*b
    c = a/b
    c = np.cos(c)
    
    t2 = time.time()
    time_vec[i] = t2-t1

time4 = np.mean(time_vec)

#%% 5
#### Constant With direct access
time_vec = np.zeros(n)

for i in range(n):
    t1 = time.time()
    c = a.n*b.n
    c = a.n/b.n
    c = np.cos(c)
    
    t2 = time.time()
    time_vec[i] = t2-t1

time5 = np.mean(time_vec)

#%%
print('Time to complete 50000 calculations compared to numpy')
print(f"Time Taken Compared to Numpy - Numpy: {time1/time1}")
print(f"Time Taken Compared to Numpy - ufloat: {time2/time1}")
print(f"Time Taken Compared to Numpy - ufloat W/pint: {time3/time1}")
print(f"Time Taken Compared to Numpy - constant: {time4/time1}")
print(f"Time Taken Compared to Numpy - constant Nominal: {time5/time1}")
print('Estimated minutes to make 1 billion calculations')
print(f"Time to complete 1 billion operations - Numpy: {(time1*1000000000)/120}")
print(f"Time to complete 1 billion operations - ufloat: {(time2*1000000000)/120}")
print(f"Time to complete 1 billion operations - ufloat W/pint: {(time3*1000000000)/120}")
print(f"Time to complete 1 billion operations - constant: {(time4*1000000000)/120}")
print(f"Time to complete 1 billion operations - constant Nominal: {(time5*1000000000)/120}")