import numpy as np
import pylab 
import random 
import matplotlib.pyplot as plt

def reptation(polymer):
    """
    Makes a repatation move on a polymer, checks for overlap, then returns original or accepted polymer
    """
    n = len(polymer)
    end_n = np.random.randint(2) #Choose which end to move
    direction = np.random.randint(4) #Choose a direction (up,down,left,or right)

    #Make the move on the appropriate endpoint
    if end_n == 0:
        endpoint = polymer[0].copy()
    else:
        endpoint = polymer[-1].copy()
    
    if direction == 0:
        endpoint[0] += 1
    elif direction == 1:
        endpoint[0] -= 1
    elif direction == 2:
        endpoint[1] += 1
    elif direction == 3:
        endpoint[1] -=1
    
    #Delete other end point and append new point onto appropriate end of array
    if end_n == 0:
        # print("Moving from beginning...")
        # print("Polymer:",polymer)
        array = polymer[:n-1].copy()
        # print("Array: ",array)
        # print("Endpoint:", endpoint)
        array = np.vstack([endpoint,array])
        # print("New Array:",array)
        # array = np.insert(array,0,endpoint,axis=0)
    else:
        # print("Moving from the end...")
        # print("Polymer:",polymer)
        array = polymer[1:n].copy()
        # print("Array: ",array)
        # print("Endpoint:", endpoint)
        array = np.vstack([array,endpoint])
        # print("New Array:",array)
        # array = np.append(array,endpoint,axis=0)

    #Check if move is accepted
    if (np.unique(array,axis=0).size == array.size):
        return array
    else:
        return polymer














# # defining the number of steps 
# def reptation_2(polymer):
#     """
#     Does a reptation move on a polymer passed as an argument
#     """

#     #Takes length of polymer and assigns x and y to first and 2nd columns
#     s = len(polymer)
#     n=s-1
#     x = numpy.zeros(s) 
#     y = numpy.zeros(s)  

#     for i in range(1, s): 
#         x[i] = polymer[i][0]
#         y[i] = polymer[i][1]
    
#     #p and q are the x and y coordinates of the end points of the polymer
#     p = x[n]
#     q = y[n]
#     val1 = np.random.randint(4) 
#     if val1 == 0: 
#         x[n] = x[n] + 1
#         y[n] = y[n] 
#         for i in range(0, n):
#             if (x[n] == x[i] and y[n] == y[i]):
#                 x[n] = p
#                 y[n] = q
#     elif val1 == 1:
#         x[n] = x[n] - 1
#         y[n] = y[n] 
#         for i in range(0, n):
#             if (x[n] == x[i] and y[n] == y[i]):
#                 x[n] = p
#                 y[n] = q
#     elif val1 == 2:
#         x[n] = x[n]
#         y[n] = y[n] + 1
#         for i in range(0, n):
#             if (x[n] == x[i] and y[n] == y[i]):
#                 x[n] = p
#                 y[n] = q
#     elif val1 == 3:
#         x[n] = x[n]
#         y[n] = y[n] - 1
#         for i in range(0, n):
#             if (x[n] == x[i] and y[n] == y[i]):
#                 x[n] = p
#                 y[n] = q 
#     r = x[n]
#     t = y[n]
#     x[n] = p
#     y[n] = q
#     for i in range(0, n): 
#         x[i] = x[i + 1]
#         y[i] = y[i + 1]
#     x[n] = r
#     y[n] = t
#     for i in range(0, s): 
#         polymer[i][0] = x[i]
#         polymer[i][1] = y[i]
#     #print(polymer)
#     #pylab.plot(x, y, 'ro')
#     #pylab.show()
#     return polymer  

    
