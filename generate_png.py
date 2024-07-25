#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 20:53:36 2024

@author: isaacfoster
"""

import code2flow as c2f
import os
c2f.code2flow('parambulator','parambulator.dot')

os.system('dot -Tpng parambulator.dot -o parambulator.png')