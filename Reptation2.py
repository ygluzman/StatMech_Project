
# coding: utf-8

# In[3]:

import numpy 
import pylab 
import random 
import matplotlib.pyplot as plt
  
# defining the number of steps 
s = 5
n = s - 1
steps = 5
x = numpy.zeros(s) 
y = numpy.zeros(s)


for i in range(1, s): 
    x[i] = x[i - 1] + 1
    y[i] = y[i - 1]

pylab.plot(x, y, 'ro')  
pylab.show() 

for i in range(1, steps):
    p = x[n]
    q = y[n]
    val1 = random.randint(1, 4) 
    if val1 == 1: 
        x[n] = x[n] + 1
        y[n] = y[n] 
        for i in range(1, n-1):
            if (x[n] == x[i] and y[n] == y[i]):
                x[n] = p
                y[n] = q
    elif val1 == 2:
        x[n] = x[n] - 1
        y[n] = y[n] 
        for i in range(1, n-1):
            if (x[n] == x[i] and y[n] == y[i]):
                x[n] = p
                y[n] = q
    elif val1 == 3:
        x[n] = x[n]
        y[n] = y[n] + 1
        for i in range(1, n-1):
            if (x[n] == x[i] and y[n] == y[i]):
                x[n] = p
                y[n] = q
    elif val1 == 4:
        x[n] = x[n]
        y[n] = y[n] - 1
        for i in range(1, n-1):
            if (x[n] == x[i] and y[n] == y[i]):
                x[n] = p
                y[n] = q
    pylab.plot(x, y, 'ro')  
    pylab.show()
    r = x[n]
    t = y[n]
    x[n] = p
    y[n] = q
    for i in range(0, n): 
        x[i] = x[i + 1]
        y[i] = y[i + 1]
    x[n] = r
    y[n] = t
    pylab.plot(x, y, 'ro')  
    print(x, y)
    pylab.show()
    


# In[ ]:




# In[ ]:



