#!/usr/bin/env python
# coding: utf-8

# In[135]:


import numpy as np
import matplotlib.pyplot as plt


# In[2]:


def pivot(polymer, n):
    pivotp = np.random.randint(n-1)+1
    angle = np.random.randint(3)
    direction = np.random.randint(2)
    if (direction == 0):
        pivotv = np.zeros((pivotp,2))
        test = np.zeros((n-pivotp,2))
        np.copyto(pivotv,polymer[:pivotp])
        np.copyto(test,polymer[pivotp:])
    else:
        pivotv = np.zeros((n-pivotp,2))
        test = np.zeros((pivotp,2))
        np.copyto(pivotv,polymer[pivotp:])
        np.copyto(test,polymer[:pivotp])
    
    pivotv = pivotv - polymer[pivotp]
    
    if(angle == 0):
        pivotv = np.fliplr(pivotv)
        pivotv = pivotv * [-1,1]
    elif(angle == 1):
        pivotv = np.fliplr(pivotv)
        pivotv = pivotv * [1,-1]
    elif(angle == 2):
        pivotv = pivotv * -1
    
    pivotv = pivotv + polymer[pivotp]

    if (direction == 0):   #append to polymer
        x = np.insert(test,0,pivotv,axis=0)
    else:
        x = np.append(test,pivotv,axis=0)
    if (np.unique(x,axis=0).size == x.size):
        return x
    else:
        return polymer

    


# In[141]:


y = np.array([[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0]])


# In[160]:


def multirun(y,n):
    a = pivot(y,n)
    for x in range(0,10):
         a = pivot(a,n)
    print(a)


# In[157]:


def arraybuild(n):
    y = np.array([[0,0]])
    for x in range(1,n):
        y = np.append(y,np.array([[0,x]]),axis=0)
    return y


# In[161]:


multirun(arraybuild(100),100)


# In[ ]:





# In[146]:


multirun()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




