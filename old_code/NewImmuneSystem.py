# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:39:44 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt

virus = 1000
plasma = 0
mcell = 5


a = 0.2
b = 0.2
c = 0.2
d = 0.5
e = 0.1
f = 0.05
g = 0.005


virusPlot = [[0,virus,0]]
plasmaPlot = [plasma]
mcellPlot = [mcell]

time = 200
for ix in range(time):
    if virus > 0:
        dvdt = a*virus - b*plasma
        dTdt = c*virus + d*mcell - e*plasma
        dMdt = f*plasma - g*mcell
        virus = virus + dvdt
        plasma = plasma + dTdt
        mcell = mcell + dMdt
        if virus < 0: virus = 0
        if plasma < 0: plasma = 0
        if mcell < 0: mcell = 0
    else:
        dvdt = 0  
        dTdt = - e*plasma
        dMdt =  - g*mcell
        virus = virus + dvdt
        plasma = plasma + dTdt
        mcell = mcell + dMdt
        if virus < 0: virus = 0
        if plasma < 0: plasma = 0
    if ix == 100:
        virus = virus + 1000
    virusPlot.append([ix,int(virus),int(dvdt)])
    plasmaPlot.append(plasma)
    mcellPlot.append(mcell)
    
    
plt.plot(range(time+1),np.array(virusPlot)[:,1],label = 'virus', c = 'red')
# plt.plot(range(time+1),np.array(virusPlot)[:,2],label = 'dVdt', c = 'orange')
plt.plot(range(time+1),plasmaPlot, label = 'plasma', c = 'blue')
plt.plot(range(time+1),mcellPlot, label = 'mcell', c = 'green')

plt.xlabel("Tidssteg")
plt.ylabel('Antal partiklar')
# plt.axis([0, time, np.min([virusPlot,plasmaPlot,mcellPlot]), np.max([virusPlot,plasmaPlot,mcellPlot])])
plt.legend()

#%%
import numpy as np
import matplotlib.pyplot as plt


virus = 100
plasma = 0
mcell = 2
time = 200

reinfectionOn = False
reinfectionTime = time/2
reinfcetionVirus = virus

parameterTimeChanger = 10
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 0.5/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.001/parameterTimeChanger
e = 1/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger


virusPlot = [[0,virus,0]]
plasmaPlot = [plasma]
mcellPlot = [mcell]

for ix in range(time):
    # if virus > 0:
    dvdt = a*virus - b*plasma
    dTdt = virus*(c + d*mcell) - e*plasma
    dMdt = f*plasma - g*mcell
    virus = virus + dvdt
    plasma = plasma + dTdt
    mcell = mcell + dMdt
    if virus < 1: virus = 0
    if plasma < 1: plasma = 0
    if mcell < 2: mcell = 2
    # else:
    #     dvdt = 0  
    #     dTdt = - e*plasma
    #     dMdt =  - g*mcell
    #     virus = virus + dvdt
    #     plasma = plasma + dTdt
    #     mcell = mcell + dMdt
    #     if mcell < 1: mcell = 0
    #     if plasma < 1: plasma = 0
    if reinfectionOn == True:
        if ix == reinfectionTime:
            virus = virus + reinfcetionVirus
    virusPlot.append([ix,int(virus),int(dvdt)])
    plasmaPlot.append(plasma)
    mcellPlot.append(mcell)
    
    
plt.plot(range(time+1),np.array(virusPlot)[:,1],label = 'virus', c = 'red')
# plt.plot(range(time+1),np.array(virusPlot)[:,2],label = 'dVdt', c = 'orange')
plt.plot(range(time+1),plasmaPlot, label = 'plasma', c = 'blue')
plt.plot(range(time+1),mcellPlot, label = 'mcell', c = 'green')
plt.semilogy()

plt.title('a ='+str(a)+' b ='+str(b)+' c ='+str(c)+' d ='+str(d)+' e ='+str(e)+' f = '+str(f)+' g = '+str(g))
plt.xlabel("Tidssteg")
plt.ylabel('Antal partiklar')
# plt.axis([0, time, np.min([virusPlot,plasmaPlot,mcellPlot]), np.max([virusPlot,plasmaPlot,mcellPlot])])
plt.legend()

