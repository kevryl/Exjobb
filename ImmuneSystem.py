# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:39:44 2021

@author: kevin
"""
#%% Plotting the immune system 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure


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
        if virusTemp < 20: virusTemp = 0
        if plasmaTemp < 5: plasmaTemp = 0
        if mcellTemp < 2: mcellTemp = 2
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 100
plasma = 0
mcell = 3

# =============================================================================
# Chronic 
# =============================================================================
parameterTimeChanger = 8
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 1/parameterTimeChanger
c = 4/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.0002/parameterTimeChanger
e = 5.5/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.10/parameterTimeChanger
parameterRange = np.array([0.6, 1.5, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.4])/parameterTimeChanger # Chronic
symptomTwo = 1000
symptomThree = 10000
symptomFour = 30000
time = 700
fulltime = 2000

# =============================================================================
# Base case
# =============================================================================
# parameterTimeChanger = 18
# a = 1/parameterTimeChanger #np.random.normal(2,0.2)
# b = 0.5/parameterTimeChanger
# c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
# d = 0.001/parameterTimeChanger
# e = 3/parameterTimeChanger
# f = 0.5/parameterTimeChanger
# g = 0.5/parameterTimeChanger
# parameterRange = np.array([1, 2, 1.2, 1.4, 1.6, 1.8])/parameterTimeChanger # Chronic
# symptomTwo = 1000
# symptomThree = 100000
# symptomFour = 1000000
# time = 200
# fulltime = 800


fig1, ax1 = plt.subplots(1)
fig2, ax2 = plt.subplots(1)
fig3, ax3 = plt.subplots(1)
fig4, ax4 = plt.subplots(1)


for count, a in enumerate(parameterRange):
    virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,fulltime, virus, plasma, mcell)
    alphaValue = 1
    if count == 0:
        ax1.plot(range(time),virusPlot[:time], c = 'red', alpha = alphaValue, label = 'Lower', linestyle = '--')
        ax1.plot(range(time),plasmaPlot[:time], c = 'blue', alpha = alphaValue, linestyle = '--')
        ax1.plot(range(time),mcellPlot[:time], c = 'green', alpha = alphaValue, linestyle = '--')
        ax2.plot(range(time),virusPlot[:time], c = 'red', alpha = alphaValue, label = 'Antigen', linestyle = '--') 
        ax3.plot(range(time),plasmaPlot[:time], c = 'blue', alpha = alphaValue, label = 'Plasma cells', linestyle = '--')
        ax4.plot(range(fulltime),mcellPlot[:fulltime], c = 'green', alpha = alphaValue, label = 'M cells', linestyle = '--')
        
    if count == 1:
        ax1.plot(range(time),virusPlot[:time], c = 'red', alpha = alphaValue, label = 'Upper' )
        ax1.plot(range(time),plasmaPlot[:time], c = 'blue', alpha = alphaValue )
        ax1.plot(range(time),mcellPlot[:time], c = 'green', alpha = alphaValue )
        ax2.plot(range(time),virusPlot[:time], c = 'red', alpha = alphaValue )
        ax3.plot(range(time),plasmaPlot[:time], c = 'blue', alpha = alphaValue )
        ax4.plot(range(fulltime),mcellPlot[:fulltime], c = 'green', alpha = alphaValue)
        
    else:
        alphaValue = 0.3
        ax2.plot(range(time),virusPlot[:time], c = 'red', alpha = alphaValue, linestyle = '--')
        ax3.plot(range(time),plasmaPlot[:time], c = 'blue', alpha = alphaValue, linestyle = '--')
        ax4.plot(range(fulltime),mcellPlot[:fulltime], c = 'green', alpha = alphaValue, linestyle = '--')
        
ax1.set_ylabel('Cell count', fontsize = 15)
ax2.set_ylabel('Antigen', fontsize = 15)
ax3.set_ylabel('Plasma cells', fontsize = 15)
ax4.set_ylabel('M cells', fontsize = 15)

ax3.plot([0, time], [symptomTwo, symptomTwo], c = 'black')
ax3.plot([0, time], [symptomThree, symptomThree], c = 'black')
ax3.plot([0, time], [symptomFour, symptomFour], c = 'black')
ax3.text(0, symptomTwo/2, "1")
ax3.text(0, symptomTwo*1.1, "2")
ax3.text(0, symptomThree*1.1, "3")
ax3.text(0, symptomFour*1.1, "4")

ax4.plot([0, fulltime], [50000, 50000])

ax1.legend(fontsize = 15)

for axes in [ax1,ax2,ax3,ax4]:
    # if axes != ax4:
        # axes.axis([1, time, 1, 1e5])
    # if axes == ax4:
    #     axes.axis([1, fulltime, 1, 1e5])
    axes.set_xlabel('Time cycle', fontsize = 15)
    axes.set_yscale('log')
    axes.grid()


#%% m_immune
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
        if virusTemp < 20: virusTemp = 0
        if plasmaTemp < 5: plasmaTemp = 0
        if mcellTemp < 2: mcellTemp = 2
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 100
plasma = 0
mcell = 3

parameterTimeChanger = 18
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 0.5/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.001/parameterTimeChanger
e = 3/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

time = 200

alphaValue = 1
count = 0
for mcell in [2,50000]: 
    virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
    if count == 0:
        plt.plot(range(time+1),virusPlot, c = 'red', alpha = alphaValue)
        plt.plot(range(time+1),plasmaPlot, c = 'blue', alpha = alphaValue)
        plt.plot(range(time+1),mcellPlot, c = 'green', alpha = alphaValue, label = 'Agent A')
    if count == 1:
        plt.plot(range(time+1),virusPlot, c = 'red', alpha = alphaValue, linestyle = '--')
        plt.plot(range(time+1),plasmaPlot, c = 'blue', alpha = alphaValue, linestyle = '--')
        plt.plot(range(time+1),mcellPlot, c = 'green', alpha = alphaValue, linestyle = '--', label = 'Agent B')
    
    count += 1
plt.legend(fontsize = 12, loc = 'lower right')
plt.yscale('log')
# plt.xscale('log')
plt.xlabel('Time cycle', fontsize = 15)
plt.ylabel('Cells', fontsize = 15)
plt.grid()

#%% REINFECTION
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
        if virusTemp < 20: virusTemp = 0
        if plasmaTemp < 5: plasmaTemp = 0
        if mcellTemp < 2: mcellTemp = 2
        if any([ix == 500, ix == 1000]):
            virusTemp += 500
        
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 100
plasma = 0
mcell = 3

parameterTimeChanger = 18
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 0.5/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.001/parameterTimeChanger
e = 3/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

time = 2000

alphaValue = 1
count = 0
for mcell in [2]: 
    virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
    if count == 0:
        plt.plot(range(time+1),virusPlot, c = 'red', alpha = alphaValue, label = 'Antigen')
        plt.plot(range(time+1),plasmaPlot, c = 'blue', alpha = alphaValue, label = 'Plasma cells')
        plt.plot(range(time+1),mcellPlot, c = 'green', alpha = alphaValue, label = 'M cells')
    if count == 1:
        plt.plot(range(time+1),virusPlot, c = 'red', alpha = alphaValue, linestyle = '--')
        plt.plot(range(time+1),plasmaPlot, c = 'blue', alpha = alphaValue, linestyle = '--')
        plt.plot(range(time+1),mcellPlot, c = 'green', alpha = alphaValue, linestyle = '--', label = 'Agent B')
    
    count += 1
plt.legend(fontsize = 12, loc = 'lower right')
plt.yscale('log')
# plt.xscale('log')
plt.xlabel('Time cycle', fontsize = 15)
plt.ylabel('Cells', fontsize = 15)
plt.grid()



#%% VACCINATION
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
        if virusTemp < 20: virusTemp = 0
        if plasmaTemp < 5: plasmaTemp = 0
        if mcellTemp < 2: mcellTemp = 2
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 100
plasma = 0
mcell = 3

parameterTimeChanger = 18
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 0.5/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.001/parameterTimeChanger
e = 3/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

time = 25000
partTime = 200

fig1, ax1 = plt.subplots(1)
fig2, ax2 = plt.subplots(1)

alphaValue = 1
count = 0
for f, g in [[0.5/18, 0.1/18],[0.5/18*100, 0.1/18/10]]: 
    virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
    if count == 0:
        ax1.plot(range(partTime),virusPlot[:partTime], c = 'red', alpha = alphaValue)
        ax1.plot(range(partTime),plasmaPlot[:partTime], c = 'blue', alpha = alphaValue)
        ax1.plot(range(partTime),mcellPlot[:partTime], c = 'green', alpha = alphaValue, label = 'Agent C')
        ax2.plot(range(time),mcellPlot[:time], c = 'green', alpha = alphaValue, label = 'Agent C')
    if count == 1:
        ax1.plot(range(partTime),virusPlot[:partTime], c = 'red', alpha = alphaValue, linestyle = '--')
        ax1.plot(range(partTime),plasmaPlot[:partTime], c = 'blue', alpha = alphaValue, linestyle = '--')
        ax1.plot(range(partTime),mcellPlot[:partTime], c = 'green', alpha = alphaValue, linestyle = '--', label = 'Agent D')
        ax2.plot(range(time),mcellPlot[:time], c = 'green', alpha = alphaValue, linestyle = '--', label = 'Agent D')
    count += 1
    
ax2.plot([0,time],[50000,50000], label = 'm$_{immune}$', color = 'blue')

for axes in [ax1,ax2]:
    axes.legend(fontsize = 12)
    axes.set_yscale('log')
    # plt.xscale('log')
    axes.set_xlabel('Time cycle', fontsize = 15)
    axes.set_ylabel('Cells', fontsize = 15)
    axes.grid()


# %% Lower and Upper for base case

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
        if virusTemp < 20: virusTemp = 0
        if plasmaTemp < 5: plasmaTemp = 0
        if mcellTemp < 2: mcellTemp = 2
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 100
plasma = 0
mcell = 10

parameterTimeChanger = 18
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 0.5/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.001/parameterTimeChanger
e = 3/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

time = 200

alphaValue = 0.1
for a in [1/parameterTimeChanger,2/parameterTimeChanger] :#np.linspace(0.4,0.3,10):
    virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
    plt.plot(range(time+1),virusPlot, c = 'red')
    plt.plot(range(time+1),plasmaPlot, c= 'blue', label = a)
    plt.plot(range(time+1),mcellPlot, c = 'green')
    alphaValue += 0.1
plt.legend(['virus','plasm','mcell'])
plt.legend()
plt.yscale('log')
# plt.xscale('log')
plt.xlabel('Time cycle')
plt.ylabel('Population')
#%% DIFFERENT ANTIGEN progessions

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


#%% Chronic with reinfection
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
        if virusTemp < 20: virusTemp = 0
        if plasmaTemp < 5: plasmaTemp = 0
        if mcellTemp < 2: mcellTemp = 2
        if ix == partTime/2:
            virusTemp = virusTemp + 5000
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

virus = 100
plasma = 0
mcell = 3

parameterTimeChanger = 8
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 1/parameterTimeChanger
c = 4/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.0002/parameterTimeChanger
e = 5.5/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

time = 25000
partTime = 1600

fig1, ax1 = plt.subplots(1)
# fig2, ax2 = plt.subplots(1)

alphaValue = 1
count = 0
# for f, g in [[0.5/18, 0.1/18],[0.5/18*100, 0.1/18/10]]: 
virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
if count == 0:
    ax1.plot(range(partTime),virusPlot[:partTime], c = 'red', alpha = alphaValue, label = 'Agent E antigen')
    ax1.plot(range(partTime),plasmaPlot[:partTime], c = 'blue', alpha = alphaValue, label = 'Agent E plasma cells')
    ax1.plot(range(partTime),mcellPlot[:partTime], c = 'green', alpha = alphaValue, label = 'Agent E M cells')
    # ax2.plot(range(time),mcellPlot[:time], c = 'green', alpha = alphaValue, label = 'No vaccination')
if count == 1:
    ax1.plot(range(partTime),virusPlot[:partTime], c = 'red', alpha = alphaValue, linestyle = '--')
    ax1.plot(range(partTime),plasmaPlot[:partTime], c = 'blue', alpha = alphaValue, linestyle = '--')
    ax1.plot(range(partTime),mcellPlot[:partTime], c = 'green', alpha = alphaValue, linestyle = '--', label = 'Vaccination')
    # ax2.plot(range(time),mcellPlot[:time], c = 'green', alpha = alphaValue, linestyle = '--', label = 'Vaccination')
count += 1

for axes in [ax1]:
    axes.legend(fontsize = 12)
    axes.set_yscale('log')
    # plt.xscale('log')
    axes.set_xlabel('Time cycle', fontsize = 15)
    axes.set_ylabel('Cells', fontsize = 15)
    axes.grid()

#%% Chronic with Vaccination
import numpy as np
import matplotlib.pyplot as plt

def Model(a,b,c,d,e,f,g,time, virusStart, plasmaStart, mcellStart, vaccinationStart):
    virus = [virusStart]
    plasma = [plasmaStart]
    mcell = [mcellStart]
    
    virusTemp = virusStart
    plasmaTemp = plasmaStart
    mcellTemp = mcellStart
    
    fakevirus = virusStart
    plasmacellsVaccination = plasmaStart
    mcellsVaccination = mcellStart
    
    for ix in range(time):
        dvdt = a*virusTemp - b*plasmaTemp
        dpdt = virusTemp*(c + d*mcellTemp) - e*plasmaTemp
        dmdt = f*plasmaTemp - g*mcellTemp
        virusTemp = virusTemp + dvdt
        plasmaTemp = plasmaTemp + dpdt
        mcellTemp = mcellTemp + dmdt
        if virusTemp < 20: virusTemp = 0
        if plasmaTemp < 5: plasmaTemp = 0
        if mcellTemp < 2: mcellTemp = 2
        if vaccinationDelay < ix:
            if vaccinationStart == True:
                fakevirus, plasmacellsVaccination, mcellsVaccination = vaccination(fakevirus, plasmacellsVaccination, mcellsVaccination)
                mcellTemp += mcellsVaccination
            
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)    
    return virus, plasma, mcell

def vaccination(fakevirus, plasmacells, mcells):
    dvdt = a*fakevirus - b*plasmacells
    dpdt = fakevirus*(c + d*mcells) - e*plasmacells
    dmdt = f*100*plasmacells - g*mcells/10
    fakevirus = fakevirus + dvdt
    plasmacells = plasmacells + dpdt
    mcells = mcells + dmdt
    if fakevirus < 20: fakevirus = 0
    if plasmacells < 5: plasmacells = 0
    if mcells < 2: mcells = 2
    return fakevirus, plasmacells, mcells
        

virus = 100
plasma = 0
mcell = 3

parameterTimeChanger = 8
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 1/parameterTimeChanger
c = 4/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.0002/parameterTimeChanger
e = 5.5/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

time = 2500
partTime = 800
vaccinationDelay = 400

fig1, ax1 = plt.subplots(1)
# fig2, ax2 = plt.subplots(1)

alphaValue = 1
count = 0
for vaccinationStart in [False, True]: 
    virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell, vaccinationStart)
    if count == 0:
        ax1.plot(range(partTime),virusPlot[:partTime], c = 'red', alpha = alphaValue)
        ax1.plot(range(partTime),plasmaPlot[:partTime], c = 'blue', alpha = alphaValue)
        ax1.plot(range(partTime),mcellPlot[:partTime], c = 'green', alpha = alphaValue, label = 'Agent F')
        # ax2.plot(range(time),mcellPlot[:time], c = 'green', alpha = alphaValue, label = 'No vaccination')
    if count == 1:
        ax1.plot(range(partTime),virusPlot[:partTime], c = 'red', alpha = alphaValue, linestyle = '--')
        ax1.plot(range(partTime),plasmaPlot[:partTime], c = 'blue', alpha = alphaValue, linestyle = '--')
        ax1.plot(range(partTime),mcellPlot[:partTime], c = 'green', alpha = alphaValue, linestyle = '--', label = 'Agent G')
        # ax2.plot(range(time),mcellPlot[:time], c = 'green', alpha = alphaValue, linestyle = '--', label = 'Vaccination')
    count += 1

for axes in [ax1]:
    axes.legend(fontsize = 12)
    axes.set_yscale('log')
    # plt.xscale('log')
    axes.set_xlabel('Time cycle', fontsize = 15)
    axes.set_ylabel('Cells', fontsize = 15)
    axes.grid()

