# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:17:30 2021

@author: kevin
"""
import numpy as np
import time

def Model(parameters, virus, plasma, mcell):
    a = parameters[0]
    b = parameters[1]
    c = parameters[2]
    d = parameters[3]
    e = parameters[4]
    f = parameters[5]
    g = parameters[6]
    dvdt = a*virus - b*plasma
    dTdt = virus*(c + d*mcell) - e*plasma
    dMdt = f*plasma - g*mcell
    virus = virus + dvdt
    plasma = plasma + dTdt
    mcell = mcell + dMdt
    virus = np.where(virus > 1, virus, 0)
    plasma = np.where(plasma > 1, plasma, 0)
    mcell = np.where(mcell > 2, mcell, 2)
    return virus, plasma, mcell


def Symptom(agentSymptom, plasma, plasmaMax):
    agentSymptom = np.where(plasma < plasmaMax, agentSymptom, 4)
    agentSymptom = np.where(plasma > plasmaMax, agentSymptom, 3)
    agentSymptom = np.where(plasma > 2*plasmaMax/3, agentSymptom, 2)
    agentSymptom = np.where(plasma > plasmaMax/3, agentSymptom,1)
    agentSymptom = np.where(plasma != 0, agentSymptom, 0)
    return agentSymptom


def CreateGridStructure(gridSize):
    gridStructure = []
    for ix in range(gridSize):
        gridStructure.append([])
        for jx in range(gridSize):
            gridStructure[ix].append([]) 
    return gridStructure

def DiseaseSpeading(gridSize, gridStructure, virus, symptom):
    for ix in range(grisSize):
        for jx in range(gridSize):
            if gridStructure[ix][jx] != [] and len(gridStructure[ix][jx]) != 1:
                for agentIndex in gridStructure[ix][jx]:
                

startTime = time.time()

# Variables in the model
populationSize = 20000
gridSize = int(np.sqrt(populationSize)/2)
infectionRate = 0.1
calculationTimer = 10
vaccineProcent = 0.001
vaccineDoses = int(np.ceil(vaccineProcent*populationSize))
plasmaMax = 9000

# Features to turn on and off
plotOn = True
deathOn = True
vaccinationOn = True

# Set up for population
agentPosition = np.ones([populationSize,2])
agentSpeed = np.ones(populationSize)
agentRotation = np.ones(populationSize) 
agentVirus = np.zeros(populationSize)
agentPlasma = np.zeros(populationSize)
agentMcell = np.zeros(populationSize)
agentSymptom = np.zeros(populationSize)


# Create parameters for the simulation
parameters = []
parameterTimeChanger = 10
a = np.ones(populationSize)*1/parameterTimeChanger #np.random.normal(2,0.2)
b = np.ones(populationSize)*0.5/parameterTimeChanger
c = np.ones(populationSize)*np.random.uniform(0.1,10,populationSize)/parameterTimeChanger # np.random.normal(1,0.1)
d = np.ones(populationSize)*0.001/parameterTimeChanger
e = np.ones(populationSize)*1/parameterTimeChanger
f = np.ones(populationSize)*0.5/parameterTimeChanger
g = np.ones(populationSize)*0.1/parameterTimeChanger
parameters.append(a)
parameters.append(b)
parameters.append(c)
parameters.append(d)
parameters.append(e)
parameters.append(f)
parameters.append(g)

# Create The population
for ix in range(populationSize):
    agentPosition[ix][0] = np.random.uniform(0,gridSize)
    agentPosition[ix][1] = np.random.uniform(0,gridSize)
    agentSpeed[ix] = 0.2
    agentRotation[ix] = np.random.uniform(-np.pi,np.pi)
    if ix < 50:
        agentVirus[ix] = 1000        

maxVirus = 0
maxPlasma = 0
# Simulation starts
for timeTicker in range(4000):
    agentMovement = np.transpose([np.cos(agentRotation), np.sin(agentRotation)]*agentSpeed)
    agentPosition = agentPosition + agentMovement
    
    # Restrict movement
    agentPosition = np.where(agentPosition<gridSize,agentPosition,0.1)
    agentPosition = np.where(agentPosition>0, agentPosition, gridSize-0.1)
    
    # Change the rotation
    agentRotation = np.random.uniform(agentRotation - np.pi/4,
                                      agentRotation + np.pi/4)
    if timeTicker % calculationTimer == 0 and timeTicker != 0:
        agentVirus, agentPlasma, agentMcell = Model(parameters, 
                                                    agentVirus, 
                                                    agentPlasma, 
                                                    agentMcell)
        if maxVirus < max(agentVirus): maxVirus = max(agentVirus)
        if maxPlasma < max(agentPlasma): maxPlasma = max(agentPlasma)
        
        agentSymptom = Symptom(agentSymptom, agentPlasma, plasmaMax)
        print(agentSymptom[:10], agentPlasma[:10].astype(int))
        
        gridStructure =[[[] for x in range(gridSize)] for y in range(gridSize)]
        flooredAgentPosition = np.floor(agentPosition)
        for agentIndex in range(populationSize):
            rowIndex = flooredAgentPosition[agentIndex][0].astype('int')
            columnIndex = flooredAgentPosition[agentIndex][1].astype('int')
            gridStructure[rowIndex][columnIndex].append(agentIndex)
            

        
print(maxVirus)
print(maxPlasma)
executionTime = (time.time() - startTime)
print('Total execution time in seconds: ' + str(executionTime))

            