#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 21:53:48 2019

@author: peterwindsor
"""

#Import Dependencies
import numpy as np
from scipy.spatial import distance as dist

#Calculate end to end distance where "ploy_array" is the coordinate polymer array and "N" is the number of segments in the polymer
def end_to_end(poly_array, N):
  dist_array = dist.cdist(poly_array, poly_array, 'euclidean')
  end_to_end_dist = dist_array[0,N-1]
  return end_to_end_dist

print(end_to_end(poly_array, N))
