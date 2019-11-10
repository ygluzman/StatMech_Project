# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 15:06:15 2019

@author: Yogev Gluzman
"""

import numpy as np

def lamilar_test(polymer1, polymer2, charges, temp, field=1):
    """
    Evalutes if move (reptation or pivot ) will be accepted in a lamilar field in the y direction
    Arguments:
    polymer1 -- initial polymer
    polymer2 -- polymer after move
    charges -- array of charges of each monomer in the polymer (1,1,1,1,1,1...,0,-1,-1,-1,-1,-1...)
    temp -- temperature for Metropolis acceptance rule
    field -- strength of lamilar field (default 1)
    
    Returns:
    1) Polymer
    2) Energy of the polymer
    """

    #Yogev called it blocks
    blocks=charges
    T=temp

    n = len(polymer1)
    E1 =0
    for i in range(0,n):
        E1 += blocks[i] * field * polymer1[i][1]

    E2 =0
    for i in range(0,n):
        E2 += blocks[i] * field * polymer2[i][1]

    DeltaE = E2-E1

    # for i in range(0,n):
    #     DeltaE += blocks[i] * field * (polymer1[i][1] - polymer2[i][1])

    if (DeltaE <= 0):
        # print('energy down accept move')
        return polymer2, E2 
    else:
        f = np.random.rand()
        bf = np.exp(-DeltaE/T)
        if (f<bf):
            # print('energy up accept move')
            return polymer2,E2
        else:
            # print('energy up reject move')
            return polymer1,E1

def generate_coblock_charges(length):
    """
    Generates charge array of polymer of length "length"
    If odd, middle monomer will have zero charge
    """

    switch_point = length//2

    if length%2 == 0:
        a = np.ones((switch_point,1))
        b = np.ones((length-switch_point,1))*-1
        poly = np.append(a,b)
    else:
        a = np.ones((switch_point,1))
        b = np.ones((length-(switch_point+1),1))*-1
        poly = np.append(a,np.array([0]))
        poly = np.append(poly,b)

    return poly

def main():
    print(generate_coblock_charges(7))


if __name__ == "__main__":
    main()








