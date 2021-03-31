# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 10:27:46 2021

@author: kevin
"""


import numpy as np
import time
import matplotlib.pyplot as plt



def CreateGridStructure(gridSize):
    gridStructure = []
    for ix in range(gridSize):
        gridStructure.append([])
        for jx in range(gridSize):
            gridStructure[ix].append([]) 
    return gridStructure


def DiseaseSpreding(agentStatus, agentTimer, gridStructure):
    for ix in range(len(gridStructure)):
        for jx in range(len(gridStructure)):
            if gridStructure[ix][jx] != [] and len(gridStructure[ix][jx]) != 1:
                localInfected = []
                localSusepteble = []
                for agentIndex in gridStructure[ix][jx]:
                    if agentStatus[agentIndex] == 'mild':
                        localInfected.append(agentIndex)
                    if agentStatus[agentIndex] == 'susepteble':
                        localSusepteble.append(agentIndex)
                
                for infectedAgentIndex in localInfected:
                    for suseptebleAgentIndex in localSusepteble:
                        r = np.random.rand()
                        if r < infectionRate:
                            agentStatus[suseptebleAgentIndex] = 'mild'
                            agentTimer[0].append(suseptebleAgentIndex)
                            agentTimer[1].append(np.random.randint(lowerDiseaseDuraion,upperDiseaseDuraion))
                            
    return agentStatus, agentTimer


def AgentRecover(agentStatus,agentTimer,calculationTimer):
    agentTimer[1] = agentTimer[1] - np.ones(len(agentTimer[1])) * calculationTimer
    indexRemove = []
    for ix in range(len(agentTimer[1])):
        if agentTimer[1][ix] < 0:
            indexRemove.append(ix)
            agentStatus[int(agentTimer[0][ix])] = 'recovered'
    agentTimer = np.delete(agentTimer,indexRemove,1)
    agentTimer = agentTimer.tolist()
    return agentStatus, agentTimer



populationSize = 30000
gridSize = int(np.sqrt(populationSize)/2)
infectionRate = 0.05
calculationTimer = 20
lowerDiseaseDuraion = 800
upperDiseaseDuraion = 1400

plotOn = True


startTime = time.time()


agentPosition = np.ones([populationSize,2])
agentSpeed = np.ones(populationSize)
agentRotation = np.ones(populationSize) 
agentTimer = [[],[]]
agentStatus = []
populationPlot = [[],[],[]]



for ix in range(populationSize):
    if ix < 50:
        agentStatus.append("mild")
        agentTimer[0].append(ix)
        agentTimer[1].append(np.random.randint(lowerDiseaseDuraion,upperDiseaseDuraion))
    else:
        agentStatus.append("susepteble")


for ix in range(populationSize):
    agentPosition[ix][0] = np.random.uniform(0,gridSize)
    agentPosition[ix][1] = np.random.uniform(0,gridSize)
    agentSpeed[ix] = 0.2
    agentRotation[ix] = np.random.uniform(-np.pi,np.pi)


for timeTicker in range(20000):
    agentMovement = np.transpose([np.cos(agentRotation), np.sin(agentRotation)]*agentSpeed)
    agentPosition = agentPosition + agentMovement
    
    # Restrict movement
    agentPosition = np.where(agentPosition<gridSize,agentPosition,0.1)
    agentPosition = np.where(agentPosition>0, agentPosition, gridSize-0.1)
    
    # Change the rotation
    agentRotation = np.random.uniform(agentRotation - np.pi/4,
                                      agentRotation + np.pi/4)
   
    if timeTicker % calculationTimer == 0 and timeTicker != 0:
        agentStatus, agentTimer = AgentRecover(agentStatus,agentTimer,calculationTimer) 
        
        gridStructure = CreateGridStructure(gridSize)
        flooredAgentPosition = np.floor(agentPosition)
        for ix in range(populationSize):
            rowIndex = flooredAgentPosition[ix][0].astype('int')
            columnIndex = flooredAgentPosition[ix][1].astype('int')
            gridStructure[rowIndex][columnIndex].append(ix)
            
        agentStatus, agentTimer = DiseaseSpreding(agentStatus, agentTimer, gridStructure)
        
        totalInfected = 0
        for ix in range(populationSize):

            if agentStatus[ix] == 'mild':
                totalInfected = totalInfected + 1
        if totalInfected == 0:
            break
        
        
        if plotOn == True:
            totalSusepteble = 0
            totalInfected = 0
            totalRecovored = 0

            for ix in range(populationSize):
                if agentStatus[ix] == 'susepteble':
                    totalSusepteble = totalSusepteble + 1
                elif agentStatus[ix] == 'mild':
                    totalInfected = totalInfected + 1
                else:
                    totalRecovored = totalRecovored + 1
            populationPlot[0].append(totalSusepteble)
            populationPlot[1].append(totalInfected)
            populationPlot[2].append(totalRecovored)
            
plotLength = range(len(populationPlot[0]))
plt.plot(plotLength, populationPlot[0], 'g', plotLength, populationPlot[1], 'r', plotLength, populationPlot[2], 'b')
plt.show()


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))