
# coding: utf-8

# In[3]:

import numpy 
import pylab 
import random 
import matplotlib.pyplot as plt
  
# polymer= 2D polymer array s= size of the polymer
def reptation(polymer, s):
    n = s - 1
    x = numpy.zeros(s) 
    y = numpy.zeros(s)  

    for i in range(1, s): 
        x[i] = polymer[i][0]
        y[i] = polymer[i][1]
    print(polymer)
    pylab.plot(x, y, 'ro')  
    pylab.show() 

    
    p = x[n]
    q = y[n]
    val1 = random.randint(1, 4) 
    if val1 == 1: 
        x[n] = x[n] + 1
        y[n] = y[n] 
        for i in range(0, n):
            if (x[n] == x[i] and y[n] == y[i]):
                x[n] = p
                y[n] = q
    elif val1 == 2:
        x[n] = x[n] - 1
        y[n] = y[n] 
        for i in range(0, n):
            if (x[n] == x[i] and y[n] == y[i]):
                x[n] = p
                y[n] = q
    elif val1 == 3:
        x[n] = x[n]
        y[n] = y[n] + 1
        for i in range(0, n):
            if (x[n] == x[i] and y[n] == y[i]):
                x[n] = p
                y[n] = q
    elif val1 == 4:
        x[n] = x[n]
        y[n] = y[n] - 1
        for i in range(0, n):
            if (x[n] == x[i] and y[n] == y[i]):
                x[n] = p
                y[n] = q 
    r = x[n]
    t = y[n]
    x[n] = p
    y[n] = q
    for i in range(0, n): 
        x[i] = x[i + 1]
        y[i] = y[i + 1]
    x[n] = r
    y[n] = t
    for i in range(0, s): 
        polymer[i][0] = x[i]
        polymer[i][1] = y[i]
    print(polymer)
    pylab.plot(x, y, 'ro')
    pylab.show()
    return polymer  
    
