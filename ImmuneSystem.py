# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:39:44 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt

virus = 10000
tcell = 0
mcell = 10000

parameterTimeChanger = 5
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 1/parameterTimeChanger
c = 4/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.0002/parameterTimeChanger
e = 5.5/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

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
    # elif ix == 750:
    #     virus = virus + 500
    virusPlot.append(virus)
    tcellPlot.append(tcell)
    mcellPlot.append(mcell)

    
plt.plot(range(time+1),virusPlot,label = 'virus', c = 'red')
plt.plot(range(time+1),tcellPlot, label = 'plasma', c = 'blue')
plt.plot(range(time+1),mcellPlot, label = 'mcell', c = 'green')
modelConstantsTextLower = 'Immune: a= {:.2f}, b= {:.2f}, c= {:.2f}, d= {:.5f}, e= {:.2f}, f= {:.2f}, g= {:.2f}'.format(a*parameterTimeChanger, b*parameterTimeChanger, c*parameterTimeChanger, d*parameterTimeChanger, e*parameterTimeChanger, f*parameterTimeChanger, g*parameterTimeChanger)
plt.figtext(0.5, -0.05, modelConstantsTextLower, ha="center", fontsize=12) 

plt.legend()
plt.yscale('log')
# plt.xscale('log')

#%%
import numpy as np
import matplotlib.pyplot as plt

def Model(a,b,c,d,e,f,g,time, virusStart, plasmaStart, mcellStart):
    virus = [virusStart]
    plasma = [plasmaStart]
    mcell = [mcellStart]
    
    virusTemp = virusStart
    plasmaTemp = plasmaStart
    mcellTemp = mcellStart
    
    for ix in range(time):
        dvdt = a*virusTemp - b*plasmaTemp
        dpdt = virusTemp*(c + d*mcellTemp) - e*plasmaTemp
        dmdt = f*plasmaTemp - g*mcellTemp
        virusTemp = virusTemp + dvdt
        plasmaTemp = plasmaTemp + dpdt
        mcellTemp = mcellTemp + dmdt
        if virusTemp < 10: virusTemp = 0
        if plasmaTemp < 10: plasmaTemp = 0
        if mcellTemp < 10: mcellTemp = 0
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 100
plasma = 0
mcell = 3

parameterTimeChanger = 10
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 1/parameterTimeChanger
c = 0.36/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.00001/parameterTimeChanger
e = 4/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.010/parameterTimeChanger

time = 200

alphaValue = 0.5
# for c in [0.1, 1]:
virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
plt.plot(range(time+1),virusPlot, c = 'red', alpha = alphaValue)
plt.plot(range(time+1),plasmaPlot, c = 'blue', alpha = alphaValue, label = c)
plt.plot(range(time+1),mcellPlot, c = 'green', alpha = alphaValue)
alphaValue += 0.5
plt.legend(['virus','plasm','mcell'])
plt.legend()
plt.yscale('log')
# plt.xscale('log')
plt.xlabel('Time cycle')
plt.ylabel('Population')
    

# %%

import numpy as np
import matplotlib.pyplot as plt

def Model(a,b,c,d,e,f,g,time, virusStart, plasmaStart, mcellStart):
    virus = [virusStart]
    plasma = [plasmaStart]
    mcell = [mcellStart]
    
    virusTemp = virusStart
    plasmaTemp = plasmaStart
    mcellTemp = mcellStart
    
    for ix in range(time):
        dvdt = a*virusTemp - b*plasmaTemp
        dpdt = virusTemp*(c + d*mcellTemp) - e*plasmaTemp
        dmdt = f*plasmaTemp - g*mcellTemp
        virusTemp = virusTemp + dvdt
        plasmaTemp = plasmaTemp + dpdt
        mcellTemp = mcellTemp + dmdt
        if virusTemp < 10: virusTemp = 0
        if plasmaTemp < 10: plasmaTemp = 0
        if mcellTemp < 10: mcellTemp = 0
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 100
plasma = 0
mcell = 3

parameterTimeChanger = 10
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 1/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.00001/parameterTimeChanger
e = 4/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.010/parameterTimeChanger

time = 5000

alphaValue = 0.1
for c in [0.38] :#np.linspace(0.4,0.3,10):
    virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
    plt.plot(range(time+1),virusPlot, c = 'red')
    plt.plot(range(time+1),plasmaPlot, label = c)
    plt.plot(range(time+1),mcellPlot, c = 'green')
    alphaValue += 0.1
plt.legend(['virus','plasm','mcell'])
plt.legend()
plt.yscale('log')
# plt.xscale('log')
plt.xlabel('Time cycle')
plt.ylabel('Population')
    

