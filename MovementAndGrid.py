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
    agentTimer = agentTimer.tolist()
    for ix in range(len(gridStructure)):
        for jx in range(len(gridStructure)):
            if gridStructure[ix][jx] != [] and len(gridStructure[ix][jx]) != 1:
                infectedPerGrid = 0
                for agentIndex in gridStructure[ix][jx]:
                    if agentStatus[agentIndex] == "mild":
                        infectedPerGrid = infectedPerGrid + 1
                        gridStructure[ix][jx].remove(agentIndex)
                    
                    if agentStatus[agentIndex] == "recovered":
                        gridStructure[ix][jx].remove(agentIndex)
                
                for agentIndex in gridStructure[ix][jx]:
                    r = np.random.rand()
                    if r < infectionRate:
                        agentStatus[agentIndex] = "mild"
                        agentTimer[0].append(agentIndex)
                        agentTimer[1].append(np.random.randint(lowerDiseaseDuraion,upperDiseaseDuraion))
    return agentStatus, agentTimer


def AgentRecover(agentStatus,agentTimer,calculationTimer):
    agentTimer[1] = agentTimer[1] - np.ones(len(agentTimer[1])) * calculationTimer
    indexRemove = []
    for ix in range(len(agentTimer[1])):
        if agentTimer[1][ix] < 0:
            indexRemove.append(ix)
            agentStatus[agentTimer[0][ix]] = 'recovered'
    agentTimer = np.delete(agentTimer,indexRemove,1)
    return agentStatus, agentTimer



populationSize = 200
gridSize = 10
infectionRate = 0.02
calculationTimer = 51
lowerDiseaseDuraion = 800
upperDiseaseDuraion = 1400

plotOn = True


startTime = time.time()


agentPosition = np.ones([populationSize,2])
agentSpeed = np.ones(populationSize)
agentRotation = np.ones(populationSize) 
agentTimer = [[],[]]
agentStatus = {}



for ix in range(populationSize):
    if ix < 10:
        agentStatus[ix] = "mild"
        agentTimer[0].append(ix)
        agentTimer[1].append(np.random.randint(lowerDiseaseDuraion,upperDiseaseDuraion))
    else:
        agentStatus[ix] = "susepteble"


for ix in range(populationSize):
    agentPosition[ix][0] = np.random.uniform(0,gridSize)
    agentPosition[ix][1] = np.random.uniform(0,gridSize)
    agentSpeed[ix] = 0.2
    agentRotation[ix] = np.random.uniform(-np.pi,np.pi)


for timeTicker in range(10000):
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
                

        if plotOn == True:
            color = []
            for ix in range(len(agentStatus)):
                if agentStatus[ix] == "susepteble":    
                    color.append("green")
                elif agentStatus[ix] == 'mild':
                    color.append("red")
                else:
                    color.append("blue")
                
            plt.axis([0,gridSize,0,gridSize])    
            plt.grid(which='major')
            plt.scatter(agentPosition[:,0],agentPosition[:,1], c = color)
            plt.pause(0.005)
                    
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))