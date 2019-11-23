#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miscellaneous functions for calculating observables and initializing the polymer
"""

#Import Dependencies
import numpy as np

def calc_mean_dist(array):
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

    dist = calc_mean_dist(dist)
    x_dist = calc_mean_dist(x_dist)
    y_dist = calc_mean_dist(y_dist)

    return dist, x_dist, y_dist

def end_to_end(poly):
    """
    Calculate end to end distance of a given numpy array
    Returns total, x, and y components
    """
    end1 = poly[0]
    end2 = poly[-1]
    end2end = end2-end1

    dist = end2end**2
    dist = np.sum(dist)
    dist = np.sqrt(dist)

    x_dist = np.abs(end2end[0])
    y_dist = np.abs(end2end[1])

    return dist, x_dist, y_dist

def init(N):
    """
    Initializes polymer of length N along the x-axis of the grid, and
    returns the initialized polymer
    """
    poly_coord = [(n,0) for n in range(0, N, 1)]
    poly_array = np.array(poly_coord)
    return poly_array





