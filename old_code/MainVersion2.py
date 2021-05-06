# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 12:03:18 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import ttk

import time

def Parameters():
    Parameters.gridSize = int(gridSizeEntry.get())
    Parameters.populationSize = int(populationSizeEntry.get())
    Parameters.infectionRateMild = float(infectionRateMildEntry.get())
    Parameters.calculationInterval = int(calculationIntervalEntry.get())
    Parameters.diseaseDurationMildLower = int(diseaseDurationMildLowerEntry.get())
    Parameters.diseaseDurationMildUpper = int(diseaseDurationMildUpperEntry.get())
    Parameters.timerDuration = int(timerDurationEntry.get())
    Parameters.initialInfected = int(initialInfectedEntry.get())
    

def CreatePopulation():
    Parameters()
    agentPosition = np.ones([Parameters.populationSize,2])
    agentSpeed = np.ones(Parameters.populationSize)
    agentRotation = np.ones(Parameters.populationSize) 
    agentTimer = [[],[]]
    agentStatus = []
    for ix in range(Parameters.populationSize):
        if ix < Parameters.initialInfected:
            agentStatus.append("mild")
            agentTimer[0].append(ix)
            agentTimer[1].append(np.random.randint(Parameters.diseaseDurationMildLower, Parameters.diseaseDurationMildUpper))
        else:
            agentStatus.append("susepteble") 
    
    for ix in range(Parameters.populationSize):
        agentPosition[ix][0] = np.random.uniform(0,Parameters.gridSize)
        agentPosition[ix][1] = np.random.uniform(0,Parameters.gridSize)
        agentSpeed[ix] = 0.05
        agentRotation[ix] = np.random.uniform(-np.pi,np.pi)
    
    return agentPosition, agentSpeed, agentRotation, agentTimer, agentStatus
    

def AgentRecover(agentStatus,agentTimer,calculationTimer):
    agentTimer[1] = agentTimer[1] - np.ones(len(agentTimer[1])) * Parameters.calculationInterval
    indexRemove = []
    for ix in range(len(agentTimer[1])):
        if agentTimer[1][ix] < 0:
            indexRemove.append(ix)
            agentStatus[int(agentTimer[0][ix])] = 'recovered'
    agentTimer = np.delete(agentTimer,indexRemove,1)
    agentTimer = agentTimer.tolist()
    return agentStatus, agentTimer


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
                for suseptebleAgentIndex in localSusepteble:
                    for infectedAgentIndex in localInfected:
                        r = np.random.rand()
                        if r < Parameters.infectionRateMild:
                            agentStatus[suseptebleAgentIndex] = 'mild'
                            agentTimer[0].append(suseptebleAgentIndex)
                            agentTimer[1].append(np.random.randint(Parameters.diseaseDurationMildLower, Parameters.diseaseDurationMildUpper))
                            break
                            
    return agentStatus, agentTimer

    

def main():
    startTime = time.time()
    Parameters()
    agentPosition, agentSpeed, agentRotation, agentTimer, agentStatus = CreatePopulation()
    populationPlot = [[],[],[]]
    
    for timeTicker in range(Parameters.timerDuration):
        agentMovement = np.transpose([np.cos(agentRotation), 
                                      np.sin(agentRotation)]*agentSpeed)
        agentPosition = agentPosition + agentMovement
        
        # Restrict movement
        agentPosition = np.where(agentPosition < Parameters.gridSize,agentPosition,0.1)
        agentPosition = np.where(agentPosition > 0, agentPosition, Parameters.gridSize-0.1)
        
        # Change the rotation
        agentRotation = np.random.uniform(agentRotation - np.pi/4,
                                          agentRotation + np.pi/4)
        
        if timeTicker % Parameters.calculationInterval:

            # Agents recover before infecting again
            agentStatus, agentTimer = AgentRecover(agentStatus ,agentTimer, Parameters.calculationInterval) 
            
            # Create the grid strcture 
            gridStructure = CreateGridStructure(Parameters.gridSize)
            flooredAgentPosition = np.floor(agentPosition)
            for ix in range(Parameters.populationSize):
                rowIndex = flooredAgentPosition[ix][0].astype('int')
                columnIndex = flooredAgentPosition[ix][1].astype('int')
                gridStructure[rowIndex][columnIndex].append(ix)
                
            agentStatus, agentTimer = DiseaseSpreding(agentStatus, agentTimer, gridStructure)
            
            totalInfected = 0
            for ix in range(Parameters.populationSize):
                if agentStatus[ix] == 'mild':
                    totalInfected = totalInfected + 1
            if totalInfected == 0:
                break
            
            if plotOn.get() == True:
                totalSusepteble = 0
                totalInfected = 0
                totalRecovored = 0
                for ix in range(Parameters.populationSize):
                    if agentStatus[ix] == 'susepteble':
                        totalSusepteble = totalSusepteble + 1
                    elif agentStatus[ix] == 'mild':
                        totalInfected = totalInfected + 1
                    else:
                        totalRecovored = totalRecovored + 1
                populationPlot[0].append(totalSusepteble)
                populationPlot[1].append(totalInfected)
                populationPlot[2].append(totalRecovored)
    
    if plotOn.get() == True:
        plotLength = range(len(populationPlot[0]))
        plt.plot(plotLength, populationPlot[0], 'g', plotLength, populationPlot[1], 'r', plotLength, populationPlot[2], 'b')
        plt.xlabel("Calculationcycle")
        plt.ylabel("Number of agents")
        plt.legend(["Susepteble","Infected","recovered"])
        plt.show()

    
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
    


# Create the base root and parent
root = Tk()
content = ttk.Frame(root, padding=(3,3,12,12))


# Create the widgets and canvas
runButton = ttk.Button(content, text = "run", command = main)


parametersLabel = ttk.Label(content, text = "Parameters")
gridSizeLabel = ttk.Label(content,text = "Grid size")
populationSizeLabel = ttk.Label(content, text = "Population size")
infectionRateMildLabel = ttk.Label(content, text = "Infection chance Mild")
calculationIntervalLabel = ttk.Label(content, text = "Calculation interval")
diseaseDurationMildLabel = ttk.Label(content, text = "Mild disease duration")
dashLabel = ttk.Label(content, text = "-")
timerDurationLabel = ttk.Label(content, text = "Simulation duration")
initialInfectedLabel = ttk.Label(content, text = "Inital infected")


gridSizeEntry = ttk.Entry(content, width = 8)
populationSizeEntry = ttk.Entry(content, width = 8)
infectionRateMildEntry = ttk.Entry(content, width = 8)
calculationIntervalEntry = ttk.Entry(content, width = 8)
diseaseDurationMildLowerEntry = ttk.Entry(content, width = 8)
diseaseDurationMildUpperEntry = ttk.Entry(content, width = 8)
timerDurationEntry = ttk.Entry(content,width = 8)
initialInfectedEntry = ttk.Entry(content,width = 8)

plotOn = BooleanVar()
plotOnCheck = ttk.Checkbutton(content, text = "Plot on", variable = plotOn)


# Insert deafault value
gridSizeEntry.insert(0,10)
populationSizeEntry.insert(0,1000)
infectionRateMildEntry.insert(0,0.01)
calculationIntervalEntry.insert(0,100)
diseaseDurationMildLowerEntry.insert(0,5000)
diseaseDurationMildUpperEntry.insert(0, 7500)
timerDurationEntry.insert(0,50000)
initialInfectedEntry.insert(0,5)


# Place widgets into a grid
content.grid(row=0, column = 0, sticky=(N, S, E, W))
runButton.grid(row = 0, column = 0, columnspan = 2)
plotOnCheck.grid(row = 0, column = 3)


parametersLabel.grid(row=1,column=0,columnspan = 2)

gridSizeLabel.grid(row = 2, column = 0)
gridSizeEntry.grid(row = 2, column = 1)

populationSizeLabel.grid(row = 3, column = 0)
populationSizeEntry.grid(row = 3, column = 1)

infectionRateMildLabel.grid(row = 4, column = 0)
infectionRateMildEntry.grid(row = 4, column = 1)

calculationIntervalLabel.grid(row = 5, column = 0)
calculationIntervalEntry.grid(row = 5, column = 1)

diseaseDurationMildLabel.grid(row = 6, column = 0)
diseaseDurationMildLowerEntry.grid(row = 6, column = 1)
dashLabel.grid(row = 6, column = 2)
diseaseDurationMildUpperEntry.grid(row = 6, column = 3)

timerDurationLabel.grid(row = 7, column = 0)
timerDurationEntry.grid(row = 7, column = 1)

initialInfectedLabel.grid(row = 8, column = 0)
initialInfectedEntry.grid(row = 8, column = 1)

# Keybindings
root.bind('<Return>', lambda e: runButton.invoke())

root.mainloop()
