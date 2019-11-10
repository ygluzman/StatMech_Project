#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 22:32:31 2019

@author: peterwindsor
"""

#Import Dependencies
import numpy as np

#Define Polymer Coordinates where "N" is the number of segments and "l" is the segment length
def init(N, l=1):
    poly_coord = [(n,0) for n in range(0, N, l)]
    poly_array = np.array(poly_coord)
    return poly_array

# print(initialization(24, 1))