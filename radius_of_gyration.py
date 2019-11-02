#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 23:05:11 2019

@author: peterwindsor
"""

#Import Dependencies
import numpy as np
from scipy.spatial import distance as dist

#Polymer Segment Length
l = 1

#Number of Segments
N = 24

#Define Polymer Coordinates
poly_coord = [(n,0) for n in range(0, N, l)]

#Make Polymer Coordinates into Array
poly_array = np.array(poly_coord)

#Calculate Radius of Gyration
x = [p[0] for p in poly_array]
y = [p[1] for p in poly_array]
center = (sum(x)/len(poly_array), sum(y)/len(poly_array))
center_array = np.array(center)
dist_center = dist.cdist(poly_array, center_array[np.newaxis,:], 'euclidean')
radius_gyration = np.mean(dist_center, 0)