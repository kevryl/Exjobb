# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 14:01:23 2021

@author: kevin
"""

import numpy as np
import time
import matplotlib.pyplot as plt
from scipy.integrate import odeint



def CreateGridStructure(gridSize):
    gridStructure = []
    for ix in range(gridSize):
        gridStructure.append([])
        for jx in range(gridSize):
            gridStructure[ix].append([]) 
    return gridStructure


def DiseaseSpreding(agentStatus, agentTimer, infectedList, gridStructure):
    for ix in range(len(gridStructure)):
        for jx in range(len(gridStructure)):
            if gridStructure[ix][jx] != [] and len(gridStructure[ix][jx]) != 1:
                localInfected = []
                localSusepteble = []
                for agentIndex in gridStructure[ix][jx]:
                    if agentStatus[agentIndex] == 'infected':
                        localInfected.append(agentIndex)
                    if agentStatus[agentIndex] == 'susepteble':
                        localSusepteble.append(agentIndex)
                        
                for suseptebleAgentIndex in localSusepteble:
                    for infectedAgentIndex in localInfected:
                        r = np.random.rand()
                        infectedTimeStep = agentTimer[infectedAgentIndex]
                        virusRate = agentVirus[infectedAgentIndex][infectedTimeStep]
                        if r < infectionRate*virusRate:
                            agentStatus[suseptebleAgentIndex] = 'infected'
                            infectedList.append(suseptebleAgentIndex)
                            break
                            
    return agentStatus, agentTimer, infectedList


def AgentRecover(agentStatus,agentTimer,infectedList, agentVirus):
    indexRemove = []
    for count, infectedAgentIndex in enumerate(infectedList):
        agentTimer[infectedAgentIndex] = agentTimer[infectedAgentIndex] + 1
        agentTimestep = agentTimer[infectedAgentIndex]
        if agentVirus[infectedAgentIndex][agentTimestep] < 1e-5:
            indexRemove.append(count)
            r = np.random.rand()
            if r < 0.1:
                agentStatus[infectedAgentIndex]  = 'susepteble'
            else:
                agentStatus[infectedAgentIndex]  = 'recovered'
            agentTimer[infectedAgentIndex] = 0
    infectedList = np.delete(infectedList,indexRemove).astype(int)
    infectedList = infectedList.tolist()
    return agentStatus, agentTimer, infectedList


def model(z,t,u):
    x = z[0]
    y = z[1]
    if t < 14:
        dxdt = (-x + u - y)/a
        dydt = (-y + x)/d
    else: 
        dxdt = (-x + u - y)/b
        dydt = (-y + x)/d
    dzdt = [dxdt,dydt]
    return dzdt


populationSize = 10000
gridSize = int(np.sqrt(populationSize)/2)
infectionRate = 0.05
calculationTimer = 100
diseaseDuration = 75
incubationDuration = 15

plotOn = True
deathOn = True


startTime = time.time()
setupTime = time.time()


agentPosition = np.ones([populationSize,2])
agentSpeed = np.ones(populationSize)
agentRotation = np.ones(populationSize) 
agentTimer = np.zeros(populationSize).astype(int)
agentTimer = agentTimer.tolist()
infectedList = []
agentStatus = []
agentVirus = []
agentAntibody = []
populationPlot = [[],[],[],[]]
maxInfected = 0


for ix in range(populationSize):
    agentPosition[ix][0] = np.random.uniform(0,gridSize)
    agentPosition[ix][1] = np.random.uniform(0,gridSize)
    agentSpeed[ix] = 0.2
    agentRotation[ix] = np.random.uniform(-np.pi,np.pi)

for ix in range(populationSize):
    if ix < 10:
        agentStatus.append("infected")
        infectedList.append(ix)
    else:
        agentStatus.append("susepteble")

# time points
t = np.linspace(0,diseaseDuration,diseaseDuration+1)
# step input
u = np.zeros(diseaseDuration)
# change to 2.0 at time = 5.0
u[0:] = 1.0
u[incubationDuration:] = 0
aMean = 15
aVariance = 5
bMean = 35
bVariance = 5
dMean = 10 
dVariance = 2

for ix in range(populationSize):
    # initial condition
    z0 = [0,0]
    a = np.random.normal(aMean,aVariance) # 3 30 30 100
    b = np.random.normal(bMean,bVariance) # 30 34
    d = np.random.normal(dMean,dVariance) # 10 100
    # solve ODE
    x = np.empty_like(t)
    y = np.empty_like(t)
    x[0] = z0[0]
    y[0] = z0[1]
    for i in range(1,diseaseDuration):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        z = odeint(model,z0,tspan,args=(u[i],))
        if z[1][0] < 0:
            z[1][0] = 0
        if z[1][1] < 0:
            z[1][1] = 0
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        # next initial condition
        z0 = z[1]
    x[-1] = 0
    agentVirus.append(x)
    agentAntibody.append(y)
    
executionTime = (time.time() - setupTime)
print('Set up execution time in seconds: ' + str(executionTime))

simulationTime = time.time()

for timeTicker in range(50000):
    agentMovement = np.transpose([np.cos(agentRotation), np.sin(agentRotation)]*agentSpeed)
    agentPosition = agentPosition + agentMovement
    
    # Restrict movement
    agentPosition = np.where(agentPosition<gridSize,agentPosition,0.1)
    agentPosition = np.where(agentPosition>0, agentPosition, gridSize-0.1)
    
    # Change the rotation
    agentRotation = np.random.uniform(agentRotation - np.pi/4,
                                      agentRotation + np.pi/4)
   
    if timeTicker % calculationTimer == 0 and timeTicker != 0:
        agentStatus, agentTimer, infectedList= AgentRecover(agentStatus,agentTimer,infectedList, agentVirus) 
        
        if deathOn == True:
            indexRemove = []
            for count, infectedAgentIndex in enumerate(infectedList):
                r = np.random.rand()
                if r < agentVirus[infectedAgentIndex][agentTimer[infectedAgentIndex]]/1000:
                    indexRemove.append(count)
                    agentSpeed[infectedAgentIndex] = 0
                    agentTimer[infectedAgentIndex] = 0
                    agentStatus[infectedAgentIndex] = 'dead'
            infectedList = np.delete(infectedList,indexRemove).astype(int)
            infectedList = infectedList.tolist()
        
        
        gridStructure = CreateGridStructure(gridSize)
        flooredAgentPosition = np.floor(agentPosition)
        for ix in range(populationSize):
            rowIndex = flooredAgentPosition[ix][0].astype('int')
            columnIndex = flooredAgentPosition[ix][1].astype('int')
            gridStructure[rowIndex][columnIndex].append(ix)
            
        agentStatus, agentTimer, infectedList = DiseaseSpreding(agentStatus, agentTimer, infectedList, gridStructure)
        
        totalInfected = 0
        for ix in range(populationSize):
            if agentStatus[ix] == 'infected':
                totalInfected = totalInfected + 1
            if maxInfected < totalInfected:
                maxInfected = totalInfected
        if totalInfected == 0:
            break
        
        
        if plotOn == True:
            totalSusepteble = 0
            totalInfected = 0
            totalRecovered = 0
            totalDead = 0

            for ix in range(populationSize):
                if agentStatus[ix] == 'susepteble':
                    totalSusepteble = totalSusepteble + 1
                elif agentStatus[ix] == 'infected':
                    totalInfected = totalInfected + 1
                elif agentStatus[ix] == 'recovered':
                    totalRecovered = totalRecovered + 1
                else: 
                    totalDead = totalDead + 1
            populationPlot[0].append(totalSusepteble)
            populationPlot[1].append(totalInfected)
            populationPlot[2].append(totalRecovered)
            populationPlot[3].append(totalDead)
            
plotLength = range(len(populationPlot[0]))
plt.plot(plotLength, populationPlot[0], 'g', plotLength, populationPlot[1], 'r', 
         plotLength, populationPlot[2], 'b', plotLength, populationPlot[3], 'k')
plt.xlabel('Timecycles')
plt.ylabel('Number of agents')
plt.legend(['susepteble', 'infected', 'recovered', 'dead'])
plt.show()

executionTime = (time.time() - simulationTime)
print('Simulation execution time in seconds: ' + str(executionTime))

executionTime = (time.time() - startTime)
print('Total execution time in seconds: ' + str(executionTime))

print('Share susepteble left ', populationPlot[0][-1]/populationSize)
print('Share recovered left ', populationPlot[2][-1]/populationSize)
print('Share dead left ', populationPlot[3][-1]/populationSize)
print('Peak infected share', maxInfected/populationSize)

