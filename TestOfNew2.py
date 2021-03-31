# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 10:32:06 2021

@author: kevin
"""


import numpy as np
import matplotlib.pyplot as plt


B = 1

m = 0.1
p = 1
d = 0.5
thetaOne = 100
thetaTwo = 10000

h = 1
f = h/(thetaOne + h)*thetaTwo/(thetaTwo + h)
BPlot = []
time = 30
for ix in range(time):
    dBdt = m + B*(p*f - d)
    B = B + dBdt
    BPlot.append(B)
    
plt.plot(range(time),BPlot)