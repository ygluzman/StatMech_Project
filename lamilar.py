# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:06:15 2019

@author: Yogev Gluzman
"""

import numpy as np

def lamilar(polymer1, polymer2, T, field, blocks):
    DeltaE = 0
    n = len(polymer1)
    for i in range(0,n):
        DeltaE += blocks[i] * field * (polymer1[i][1] - polymer2[i][1])
    if (DeltaE <= 0):
        print('energy down accept move')
        return polymer2 
    f = np.random.rand()
    bf = np.exp(-DeltaE/T)
    if (f<bf):
        print('energy up accept move')
        return polymer2
    else:
        print('energy up reject move')
        return polymer1

def coblock(length,switch_point):
    a = np.ones((switch_point,1))
    b = np.ones((length-switch_point,1))*-1
    poly = np.append(a,b)
    return poly
