#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 23:46:48 2024

@author: isaacfoster
"""

import pyvista as pv
from pyvista import examples
import pyviewfactor as pvf

filename = examples.planefile
filename = 'planes.stl'
mesh = pv.read(filename)
mesh = examples.download_notch_stress()

cell = mesh.get_cell(0)
faces = cell.faces
len(faces)
