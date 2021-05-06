# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 10:48:13 2021

@author: kevin
"""


import matplotlib.pyplot as plt
import numpy as np

v = np.linspace(0,1)
a = 0.2

infection = (1-v)*a*v

plt.plot(v,infection)
plt.xlabel('v')
plt.ylabel('infection')
