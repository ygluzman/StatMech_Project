#!/usr/bin/env python
# coding: utf-8

import numpy as np

def pivot(polymer):
    """
    Makes a pivot move on a polymer, checks for overlap, then returns original or accepted polymer
    """

    n= len(polymer)
    pivotp = np.random.randint(n-1)+1 # point about which it pivots
    angle = np.random.randint(3) # angle of the rotation 0=90 , 1 = -90, 2 = 180
    direction = np.random.randint(2) # direction up or down polymer that gets rotated
    if (direction == 0):
        pivotv = np.zeros((pivotp,2)) #the vector that will be rotated
        test = np.zeros((n-pivotp,2)) # the remaining portion of the polymer 
        np.copyto(pivotv,polymer[:pivotp])
        np.copyto(test,polymer[pivotp:])
    else:
        pivotv = np.zeros((n-pivotp,2))
        test = np.zeros((pivotp,2))
        np.copyto(pivotv,polymer[pivotp:])
        np.copyto(test,polymer[:pivotp])
    
    # changes the axis
    pivotv = pivotv - polymer[pivotp]
    
    # rotates the polymer
    if(angle == 0):
        pivotv = np.fliplr(pivotv)
        pivotv = pivotv * [-1,1]
    elif(angle == 1):
        pivotv = np.fliplr(pivotv)
        pivotv = pivotv * [1,-1]
    elif(angle == 2):
        pivotv = pivotv * -1
    
    # change the axis back 
    pivotv = pivotv + polymer[pivotp]

    if (direction == 0):   #append to polymer
        x = np.insert(test,0,pivotv,axis=0)
    else:
        x = np.append(test,pivotv,axis=0)
    
    # check for number of unique points 
    if (np.unique(x,axis=0).size == x.size):
        return x
    else:
        return polymer

 
