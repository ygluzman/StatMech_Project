#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 23:05:11 2019
"""

#Import Dependencies
import numpy as np

def calc_dist(array):
    """
    Squares all values in an array, takes total sum, divides by length, and takes the sqrt
    """
    length = len(array)
    array = array**2
    array = np.sum(array)
    array = array/length
    array = np.sqrt(array)
    return array


def radius_of_gyration(poly):
    """
    Calculate radius of gyration of a given numpy array
    Returns total, x, and y components
    """
    centroid = np.sum(poly,axis=0)/poly.shape[0]
    
    dist = poly-centroid
    x_dist = dist[:,0]
    y_dist = dist[:,1]

    dist = calc_dist(dist)
    x_dist = calc_dist(x_dist)
    y_dist = calc_dist(y_dist)

    return dist, x_dist, y_dist


# from scipy.spatial import distance as dist
# #Calculate Radius of Gyration
# def radius_gyration(poly_array):
#   x = [p[0] for p in poly_array]
#   y = [p[1] for p in poly_array]
#   center = (sum(x)/len(poly_array), sum(y)/len(poly_array))
#   center_array = np.array(center)
#   dist_center = dist.cdist(poly_array, center_array[np.newaxis,:], 'euclidean')
#   radius_gyration_dist = np.mean(dist_center, 0)[0]
#   return radius_gyration_dist
