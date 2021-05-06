# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 13:41:13 2021

@author: kevin
"""


import numpy as np
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import ttk

import time

from subprocess import Popen


def main():
    startTime = time.time()
    Parameters()
    agentPosition, agentSpeed, agentRotation, agentTimer, agentStatus = CreatePopulation()
    
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
            # Agents recover before infectiong again
            agentStatus, agentTimer = AgentRecover(agentStatus ,agentTimer, Parameters.calculationInterval) 
            
            # Create the grid strcture 
            gridStructure = CreateGridStructure(Parameters.gridSize)
            flooredAgentPosition = np.floor(agentPosition)
            for ix in range(Parameters.populationSize):
                rowIndex = flooredAgentPosition[ix][0].astype('int')
                columnIndex = flooredAgentPosition[ix][1].astype('int')
                gridStructure[rowIndex][columnIndex].append(ix)
                
            agentStatus, agentTimer = DiseaseSpreding(agentStatus, agentTimer, gridStructure)
            
            if plotOn.get() == True:
                PlotSimulation(agentPosition,agentStatus)
    
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
    return


def Parameters():
    Parameters.gridSize = int(gridSizeEntry.get())
    
    Parameters.populationSize = int(populationSizeEntry.get())
    
    Parameters.infectionRateMild = float(infectionRateMildEntry.get())

    Parameters.calculationInterval = int(calculationIntervalEntry.get())
    
    Parameters.diseaseDurationMildLower = int(diseaseDurationMildLowerEntry.get())
    Parameters.diseaseDurationMildUpper = int(diseaseDurationMildUpperEntry.get())
    
    Parameters.timerDuration = int(timerDurationEntry.get())


def CreatePopulation():
    Parameters()
    agentPosition = np.ones([Parameters.populationSize,2])
    agentSpeed = np.ones(Parameters.populationSize)
    agentRotation = np.ones(Parameters.populationSize) 
    agentTimer = [[],[]]
    agentStatus = {}
    for ix in range(Parameters.populationSize):
        if ix < 10:
            agentStatus[ix] = "mild"
            agentTimer[0].append(ix)
            agentTimer[1].append(np.random.randint(Parameters.diseaseDurationMildLower, Parameters.diseaseDurationMildUpper))
        else:
            agentStatus[ix] = "susepteble"    
    
    for ix in range(Parameters.populationSize):
        agentPosition[ix][0] = np.random.uniform(0,Parameters.gridSize)
        agentPosition[ix][1] = np.random.uniform(0,Parameters.gridSize)
        agentSpeed[ix] = 0.2
        agentRotation[ix] = np.random.uniform(-np.pi,np.pi)
    
    return agentPosition, agentSpeed, agentRotation, agentTimer, agentStatus
    

def AgentRecover(agentStatus,agentTimer,calculationTimer):
    agentTimer[1] = agentTimer[1] - np.ones(len(agentTimer[1])) * Parameters.calculationInterval
    indexRemove = []
    for ix in range(len(agentTimer[1])):
        if agentTimer[1][ix] < 0:
            indexRemove.append(ix)
            agentStatus[agentTimer[0][ix]] = 'recovered'
    agentTimer = np.delete(agentTimer,indexRemove,1)
    return agentStatus, agentTimer


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
                
                if infectedPerGrid != 0:
                    for agentIndex in gridStructure[ix][jx]:
                        for infected in range(infectedPerGrid):
                            r = np.random.rand()
                            if r < Parameters.infectionRateMild:
                                agentStatus[agentIndex] = "mild"
                                agentTimer[0].append(agentIndex)
                                agentTimer[1].append(np.random.randint(Parameters.diseaseDurationMildLower, Parameters.diseaseDurationMildUpper))
    return agentStatus, agentTimer


def PlotSimulation(agentPosition,agentStatus):
    color = []
    for ix in range(len(agentStatus)):
        if agentStatus[ix] == "susepteble":    
            color.append("green")
        elif agentStatus[ix] == 'mild':
            color.append("red")
        else:
            color.append("blue")
        
    plt.axis([0,Parameters.gridSize,0,Parameters.gridSize])    
    plt.grid(which='major')
    plt.scatter(agentPosition[:,0],agentPosition[:,1], c = color)
    plt.pause(0.05)


def TerminateCondition(agentStatus):
    


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


gridSizeEntry = ttk.Entry(content, width = 8)
populationSizeEntry = ttk.Entry(content, width = 8)
infectionRateMildEntry = ttk.Entry(content, width = 8)
calculationIntervalEntry = ttk.Entry(content, width = 8)
diseaseDurationMildLowerEntry = ttk.Entry(content, width = 8)
diseaseDurationMildUpperEntry = ttk.Entry(content, width = 8)
timerDurationEntry = ttk.Entry(content,width = 8)

plotOn = BooleanVar()
plotOnCheck = ttk.Checkbutton(content, text = "Plot on", variable = plotOn)


# Insert deafault value
gridSizeEntry.insert(0,10)
populationSizeEntry.insert(0,200)
infectionRateMildEntry.insert(0,0.9)
calculationIntervalEntry.insert(0,20)
diseaseDurationMildLowerEntry.insert(0,1000)
diseaseDurationMildUpperEntry.insert(0, 1500)
timerDurationEntry.insert(0,5000)


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


# Keybindings
root.bind('<Return>', lambda e: runButton.invoke())

root.mainloop()
