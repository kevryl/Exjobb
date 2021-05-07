# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:39:44 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt

virus = 10000
tcell = 0
mcell = 50000

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


time = 100
for ix in range(time):
    dvdt = a*virus - b*tcell
    dTdt = virus*(c + d*mcell) - e*tcell
    dMdt = f*tcell - g*mcell
    virus = virus + dvdt
    tcell = tcell + dTdt
    mcell = mcell + dMdt
    if virus < 40: virus = 0
    if tcell < 40: tcell = 0
    if mcell < 40: mcell = 0
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

parameterTimeChanger = 1000000
a = 1000/parameterTimeChanger #np.random.normal(2,0.2)
b = 1/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.01/parameterTimeChanger
e = 4/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.010/parameterTimeChanger

time = 200000

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

time = 100

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
        if virusTemp < 1e7:
            dvdt = a*virusTemp - b*plasmaTemp
            dpdt = virusTemp*(c + d*mcellTemp) - e*plasmaTemp
            dmdt = f*plasmaTemp - g*mcellTemp
            virusTemp = virusTemp + dvdt
            plasmaTemp = plasmaTemp + dpdt
            mcellTemp = mcellTemp + dmdt
            if virusTemp < 10: virusTemp = 0
            if plasmaTemp < 10: plasmaTemp = 0
            if mcellTemp < 10: mcellTemp = 0
        else: 
            virusTemp = 1e8
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 1000
plasma = 0
mcell = 3


a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 1/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.00001/parameterTimeChanger
e = 4/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.010/parameterTimeChanger

case1 = np.array([1,1,1,0.001,5,0.5,0.1])/10
case2 = np.array([4,1,1,0.001,5,0.5,0.1])/40
case3 = np.array([1,1,100,0.0001,1,5,1])/150
case4 = np.array([1,2,100,0.0001,1,0.1,0.1])/150
case5 = np.array([1000,2,0.1,1,10,0.5,10])/1000
case6 = np.array([1000,2,0.1,1,10,0.5,10])/3000
case8 = np.array([1,1,4,0.0002,5.5,0.5,0.1])/3

time = 200

alphaValue = 0.1
for a,b,c,d,e,f,g in [case1,case2,case3,case4,case5,case6,case8]:
    virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
    
    plt.plot(range(time+1),virusPlot, c = 'black')
    # plt.plot(range(time+1),plasmaPlot, label = c)+
    # plt.plot(range(time+1),mcellPlot, c = 'green')
    alphaValue += 0.1
# plt.legend(['case1','case2','case3','case4','case5','case6','case8'])
plt.text(30,50, '1')
plt.text(10,10, '1')
plt.text(55,25, '2')
plt.text(78,35, '2')
plt.text(130,5e3, '4')
plt.text(16,2e6, '3')

plt.yscale('log')
plt.axis([0,time,1,1e7])
# plt.xscale('log')
plt.xlabel('Time')
plt.ylabel('Antigen')