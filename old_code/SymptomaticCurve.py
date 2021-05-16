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

#%%

import numpy as np
import matplotlib.pyplot as plt

parameterTimeChanger = 10
a = 0.7/parameterTimeChanger #np.random.normal(2,0.2)
b = 0.5/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.001/parameterTimeChanger
e = 3/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

maxPlasma = 0
time = 100

for count, c in enumerate([0.2/parameterTimeChanger,1/parameterTimeChanger]):       
    virus = 1000
    plasma = 0
    mcell = 100
    virusPlot = [virus]
    plasmaPlot = [plasma]
    mcellPlot = [mcell]
    for ix in range(time):
        dvdt = a*virus - b*plasma
        dTdt = virus*(c + d*mcell) - e*plasma
        dMdt = f*plasma - g*mcell
        virus = virus + dvdt
        plasma = plasma + dTdt
        mcell = mcell + dMdt
        if virus < 10: virus = 0
        if plasma < 10: plasma = 0
        if mcell < 10: mcell = 0 
        # elif ix == 750:
        #     virus = virus + 500
        virusPlot.append(virus)
        plasmaPlot.append(plasma)
        mcellPlot.append(mcell)
        if maxPlasma < plasmaPlot[ix]: maxPlasma = plasmaPlot[ix]
    if count == 0:
        plt.plot(np.linspace(0.06,1,time+1),np.array(plasmaPlot)/maxPlasma*4, label = 'Agent A plasma')
    else:
        plt.plot(np.linspace(0.06,1,time+1),np.array(plasmaPlot)/maxPlasma*4, label = 'Agent B plasma')


pLinear = np.linspace(0.06,1)
symptomLinear = pLinear*4

plt.plot([0,1],[1,1], 'k--', alpha = 0.7)
plt.plot([0,1],[2,2], 'k--', alpha = 0.7)
plt.plot([0,1],[3,3], 'k--', alpha = 0.7)



plt.text(0,0.2,'1: Asymptomatic')
plt.text(0.0,1.1,'2: Weak symptoms')
plt.text(0.0,2.1,'3: Moderate symptoms')
plt.text(0.0,3.1,'4: Severe symptoms')

plt.legend()
plt.axis('off')
# plt.yscale('log')

