# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 10:44:17 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt

pLinear = np.linspace(0.06,1)
symptomLinear = pLinear*4

plt.plot(pLinear, symptomLinear, label = "Linear")

pStep = [0,0.25,0.25,0.25,0.5,0.5,0.5,0.75,0.75,0.75,1]
symptomStep = [0,0,0,1,1,1,2,2,2,3,3]

plt.plot(pStep,symptomStep, c = 'red', label = 'Step')

plt.plot([0,0.25],[1,1], 'k--')
plt.plot([0,0.5],[2,2], 'k--')
plt.plot([0,0.75],[3,3], 'k--')

plt.text(0,0.1,'No symptom')
plt.text(0.26,0.8,'Symptom expressed weakly')
plt.text(0.51,1.8,'Moderate symptom')
plt.text(0.76,2.8,'Sharply')
plt.text(0.76,2.6,'expressed')
plt.text(0.76,2.4,'symptom')


plt.legend()
plt.xlabel("Från 0 till Pmax")
plt.ylabel("Symptomatic")

