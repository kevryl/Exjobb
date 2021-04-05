# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:17:30 2021

@author: kevin
"""
import numpy as np
import matplotlib.pyplot as plt
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
    for ix in range(gridSize):
        for jx in range(gridSize):
            if gridStructure[ix][jx] != [] and len(gridStructure[ix][jx]) != 1:
                localInfected = []
                localSusepteble = []
                for agentIndex in gridStructure[ix][jx]:
                    if virus[agentIndex] != 0:
                        localInfected.append(agentIndex)
                    else:
                        localSusepteble.append(agentIndex)
                
                for localSuseptebleIndex in localSusepteble:
                    for localInfectedIndex in localInfected:
                        r = np.random.rand()
                        meetingProbability = 1/symptom[localInfectedIndex]
                        if r < infectionProbability*meetingProbability:
                            virus[localSuseptebleIndex] = virus[localSuseptebleIndex] + 100
                
                # tempGridSturcture = gridStructure[ix][jx].copy()
                # for kx in range(len(gridStructure[ix][jx])):
                #     agentIndex = gridStructure[ix][jx][kx]
                #     tempGridSturcture.pop(0) # Remove the agentIndex from tempGridStucture
                #     for otherAgentIndex in tempGridSturcture:
                #         print(agentIndex, otherAgentIndex)
    return virus

startTime = time.time()

# Variables in the model
populationSize = 2000
gridSize = int(np.sqrt(populationSize)/2)
infectionProbability = 0.1
calculationTimer = 10
vaccineProcent = 0.001
vaccineDoses = int(np.ceil(vaccineProcent*populationSize))
plasmaMax = 9000
populationPlot = [[],[],[]]
initialInfected = populationSize/100
initialImmune = populationSize/2 

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
vaccinationList = list(range(populationSize))

# Create parameters for the simulation
parameters = []
parameterTimeChanger = 10
a = np.ones(populationSize)*1/parameterTimeChanger #np.random.normal(2,0.2)
b = np.ones(populationSize)*0.5/parameterTimeChanger
c = np.ones(populationSize)*np.random.uniform(0.1,10,populationSize)/parameterTimeChanger # np.random.normal(1,0.1)
d = np.ones(populationSize)*0.001/parameterTimeChanger
e = np.ones(populationSize)*1/parameterTimeChanger
f = np.ones(populationSize)*0.5/parameterTimeChanger
g = np.ones(populationSize)*0.005/parameterTimeChanger
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
    if ix < initialInfected:
        agentVirus[ix] = 1000
    if ix < initialImmune and ix > initialInfected:
        agentMcell[ix] = 45000

# Simulation starts
for timeTicker in range(100000):
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

        agentSymptom = Symptom(agentSymptom, agentPlasma, plasmaMax)

        
        gridStructure =[[[] for x in range(gridSize)] for y in range(gridSize)]
        flooredAgentPosition = np.floor(agentPosition)
        for agentIndex in range(populationSize):
            rowIndex = flooredAgentPosition[agentIndex][0].astype('int')
            columnIndex = flooredAgentPosition[agentIndex][1].astype('int')
            gridStructure[rowIndex][columnIndex].append(agentIndex)
        

        agentVirus = DiseaseSpeading(gridSize, gridStructure, agentVirus, agentSymptom)
        
        
        if vaccinationOn == True:
            vaccineDoses = 0
            removeIndex= []
            for index, ix in enumerate(vaccinationList):
                if vaccineDoses < 3:
                    if all([agentVirus[ix] == 0, agentPlasma[ix] == 0]):
                        agentMcell[ix] = agentMcell[ix] + 50000
                        removeIndex.append(index)
                        vaccineDoses = vaccineDoses + 1
            vaccinationList = np.delete(vaccinationList,removeIndex)
            vaccinationList.tolist()
        
        totalSusepteble = 0
        totalInfected = 0
        totalImmune = 0
        for ix in range(populationSize):
            if agentVirus[ix] != 0 :
                totalInfected = totalInfected +1
            elif all([agentVirus[ix] == 0, agentPlasma[ix] > 0]):
                totalImmune = totalImmune + 1
            else: 
                totalSusepteble = totalSusepteble + 1
                
        if totalInfected == 0:
            break
        
        populationPlot[0].append(totalSusepteble)
        populationPlot[1].append(totalInfected)
        populationPlot[2].append(totalImmune)

if plotOn == True:
    plt.figure()
    n = 10
    susepteblePlot = [sum(populationPlot[0][i:i+n])//n for i in range(0,len(populationPlot[0]),n)]
    infectedPlot = [sum(populationPlot[1][i:i+n])//n for i in range(0,len(populationPlot[1]),n)]
    immunePlot = [sum(populationPlot[2][i:i+n])//n for i in range(0,len(populationPlot[2]),n)]
    plotLength = np.linspace(0,len(populationPlot[0]),len(susepteblePlot))
    plt.plot(plotLength, susepteblePlot, 'g', plotLength, infectedPlot, 'r',
             plotLength, immunePlot, 'b')
    plt.xlabel('Timecycles')
    plt.ylabel('Number of agents')
    plt.legend(['susepteble', 'infected', 'symptomatic'])
    plt.show()


executionTime = (time.time() - startTime)
print('Total execution time in seconds: ' + str(executionTime))

            