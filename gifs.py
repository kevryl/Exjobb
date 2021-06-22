# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 10:21:03 2021

@author: kevin
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import imageio


populationSize = 10
gridSizeSide = 10
agentPosition = np.ones([populationSize,2])
agentSpeed = np.ones(populationSize)
agentRotation = np.ones(populationSize) 
agentVirus = np.zeros(populationSize)
agentPlasma = np.zeros(populationSize)
agentMcell = np.zeros(populationSize)
agentSymptom = np.zeros(populationSize)
vaccinationList = list(range(populationSize))

for ix in range(populationSize):
    agentPosition[ix][0] = np.random.uniform(0,gridSizeSide)
    agentPosition[ix][1] = np.random.uniform(0,gridSizeSide)
    agentSpeed[ix] = 0.2
    agentRotation[ix] = np.random.uniform(-np.pi,np.pi)


filenames = []
for ix in range(300):
    agentMovement = np.transpose([np.cos(agentRotation), np.sin(agentRotation)]*agentSpeed)
    agentPosition = agentPosition + agentMovement
    
    # Restrict movement
    agentPosition = np.where(agentPosition<gridSizeSide,agentPosition,0.1)
    agentPosition = np.where(agentPosition>0, agentPosition, gridSizeSide-0.1)
    
    
    # Change the rotation
    agentRotation = np.random.uniform(agentRotation - np.pi/4,
                                      agentRotation + np.pi/4)
    
    plt.scatter(agentPosition[:,0],agentPosition[:,1])
    plt.axis([-0.1,gridSizeSide+0.1,-0.1,gridSizeSide+0.1])
    plt.grid()
    
    # create file name and append it to a list
    filename = f'{ix}.png'
    filenames.append(filename)
    
    # save frame
    plt.savefig(filename)
    plt.close()
    
# build gif
with imageio.get_writer('agentMovement.gif', mode='I') as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
        
# Remove files
for filename in set(filenames):
    os.remove(filename)
 
    
 #%%
 
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
        if plasmaTemp < 1: plasmaTemp = 0
        if mcellTemp < 2: mcellTemp = 2
        
        
        if gifOn == True:
            plt.plot(range(ix+1),virus, c = 'red', alpha = alphaValue, label = 'V')
            plt.plot(range(ix+1),plasma, c = 'blue', alpha = alphaValue, label = 'P')
            plt.plot(range(ix+1),mcell, c = 'green', alpha = alphaValue, label = 'M')
            plt.legend(fontsize = 12, loc = 'upper left')
            plt.yscale('log')
            plt.grid()
            plt.xlabel('Time')
            plt.ylabel('Cell count')
            plt.axis([0,time,0,1000000])    
        
            # create file name and append it to a list
            filename = f'{ix}.png'
            filenames.append(filename)
            
            # save frame
            plt.savefig(filename)
            plt.close()
            
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)
        
    return virus, plasma, mcell

virus = 50
plasma = 1
mcell = 3

gifOn= True

parameterTimeChanger = 8
a = 1/parameterTimeChanger #np.random.normal(2,0.2)
b = 0.5/parameterTimeChanger
c = 0.1/parameterTimeChanger # np.random.normal(1,0.1)
d = 0.001/parameterTimeChanger
e = 3/parameterTimeChanger
f = 0.5/parameterTimeChanger
g = 0.1/parameterTimeChanger

time = 100

alphaValue = 1

filenames = []
virusPlot, plasmaPlot, mcellPlot = Model(a,b,c,d,e,f,g,time, virus, plasma, mcell)
plt.plot(range(time+1),virusPlot, c = 'red', alpha = alphaValue)
plt.plot(range(time+1),plasmaPlot, c = 'blue', alpha = alphaValue)
plt.plot(range(time+1),mcellPlot, c = 'green', alpha = alphaValue, label = 'Agent A')
plt.yscale('log')

#%%
if gifOn == True:
    #build gif
    with imageio.get_writer('immunesystem2.gif', mode='I') as writer:
        for filename in filenames[-100:]:
            image = imageio.imread(filename)
            writer.append_data(image)
            
    # Remove files
    for filename in set(filenames[-100:]):
        os.remove(filename)



 
#%%
import moviepy.editor as mp

clip = mp.VideoFileClip("immunesystem2.gif")
clip.write_videofile("immunesystem2.mp4")

#%%
