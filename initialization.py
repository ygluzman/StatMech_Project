#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 22:32:31 2019

@author: peterwindsor
"""

import numpy as np

def init(N):
    """
    Initializes polymer of length N
    Will initialize along the x-axis of the grid

    Returns: Polymer of length N
    """
    poly_coord = [(n,0) for n in range(0, N, 1)]
    poly_array = np.array(poly_coord)
    return poly_array