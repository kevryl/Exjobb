# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 16:31:33 2021

@author: kevin
"""
import numpy as np
import matplotlib.pyplot as plt

import time

startTime = time.time()

populationSize = 100000

demografi = []


for ix in range(populationSize):
    r = np.random.rand()
    if r < 0.1771:
        demografi.append(np.random.randint(0,14))
    elif 0.1771 < r < 0.2851: 
        demografi.append(np.random.randint(15,24))
    elif 0.2851 < r < 0.6752:
        demografi.append(np.random.randint(25,54))
    elif 0.6752 < r < 0.7942:
        demografi.append(np.random.randint(55,64))
    elif 0.7942 < r:
        demografi.append(np.random.randint(65,100))


plt.hist(demografi,[0,15,25,55,65,100], weights=np.ones(len(demografi)) / len(demografi))

                    
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))