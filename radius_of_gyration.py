#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 23:05:11 2019

@author: peterwindsor
"""

#Import Dependencies
import numpy as np
from scipy.spatial import distance as dist

#Calculate Radius of Gyration
def radius_gyration(poly_array):
  x = [p[0] for p in poly_array]
  y = [p[1] for p in poly_array]
  center = (sum(x)/len(poly_array), sum(y)/len(poly_array))
  center_array = np.array(center)
  dist_center = dist.cdist(poly_array, center_array[np.newaxis,:], 'euclidean')
  radius_gyration_dist = np.mean(dist_center, 0)[0]
  return radius_gyration_dist


#Daniel:
def radius_of_gyration(poly):
    centroid = np.sum(poly,axis=0)/poly.shape[0]
    dist = poly-centroid
    dist = dist**2
    dist = np.sum(dist)
    dist = dist/poly.shape[0]
    dist = np.sqrt(dist)
    return dist
