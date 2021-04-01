# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:39:44 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt

virus = 1000
tcell = 0
mcell = 3

parameterTimeChanger = 10
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 0.5/parameterTimeChanger
c = 10/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.011/parameterTimeChanger
e = 1/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.005/parameterTimeChanger

virusPlot = [virus]
tcellPlot = [tcell]
mcellPlot = [mcell]


time = 1000
for ix in range(time):
    dvdt = a*virus - b*tcell
    dTdt = virus*(c + d*mcell) - e*tcell
    dMdt = f*tcell - g*mcell
    virus = virus + dvdt
    tcell = tcell + dTdt
    mcell = mcell + dMdt
    if virus < 10: virus = 0
    if tcell < 10: tcell = 0
    if mcell < 10: mcell = 0
    if ix == 500:
        virus = virus + 500 
    elif ix == 750:
        virus = virus + 500
    virusPlot.append(virus)
    tcellPlot.append(tcell)
    mcellPlot.append(mcell)

    
plt.plot(range(time+1),virusPlot,label = 'virus', c = 'red')
plt.plot(range(time+1),tcellPlot, label = 'tcell', c = 'green')
plt.plot(range(time+1),mcellPlot, label = 'mcell', c = 'blue')
plt.legend()
plt.yscale('log')
plt.axis([0, time, np.min([virusPlot,tcellPlot,mcellPlot]), np.max([virusPlot,tcellPlot,mcellPlot])])

