# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 10:33:35 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt
# matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *
from tkinter import ttk

import time


def Parameters():
    Parameters.populationSize = int(populationSizeEntry.get())
    Parameters.gridSizeSide = int(gridSizeSideEntry.get())
    Parameters.initialInfected = int(initialInfectedEntry.get())
    Parameters.infectionProbability = float(infectionProbabilityEntry.get())
    Parameters.initialImmune = int(initialImmuneEntry.get())
    Parameters.plasmaMax = int(plasmaMaxEntry.get())
    Parameters.totalVaccineDoses = int(totalVaccineDosesEntry.get())
    Parameters.simulationTime = int(simulationTimeEntry.get())
    Parameters.calculationTimer = int(calculationTimerEntry.get())
    Parameters.initialVirusCount = int(initialVirusCountEntry.get())
    Parameters.initialPlasmaCount = int(initialPlasmaCountEntry.get())
    Parameters.initialMcellCount = int(initialMcellCountEntry.get())
    
    Parameters.modelTimeChanger = float(modelTimeChangerEntry.get())
    Parameters.modelTimeTotal = int(modelTimeTotalEntry.get())
    Parameters.aUpper = float(aUpperEntry.get())
    Parameters.aLower = float(aLowerEntry.get())
    
    Parameters.bUpper = float(bUpperEntry.get())
    Parameters.bLower = float(bLowerEntry.get())
    
    Parameters.cUpper = float(cUpperEntry.get())
    Parameters.cLower = float(cLowerEntry.get())
    
    Parameters.dUpper = float(dUpperEntry.get())
    Parameters.dLower = float(dLowerEntry.get())
    
    Parameters.eUpper = float(eUpperEntry.get())
    Parameters.eLower = float(eLowerEntry.get())
    
    Parameters.fUpper = float(fUpperEntry.get())
    Parameters.fLower = float(fLowerEntry.get())
    
    Parameters.gUpper = float(gUpperEntry.get())
    Parameters.gLower = float(gLowerEntry.get())
    
    
def PlotInitialImmuneSystem():
    Parameters()
    modelConstants = CreateModelConstant()
    singelConstants = [constants[0] for constants in modelConstants]
    
    # Create the figure in the GUI
    figure = Figure(figsize=(5, 4), dpi=70)
    plot = figure.add_subplot(1, 1, 1)
    plot.set_xlabel("Timecycle")
    plot.set_ylabel("Cells")
    
    virus = [Parameters.initialVirusCount]
    plasma = [Parameters.initialPlasmaCount]
    mcell = [Parameters.initialMcellCount]
    
    virusTemp = Parameters.initialVirusCount
    plasmaTemp = 0
    mcellTemp = 10
    
    
    for ix in range(Parameters.modelTimeTotal):
        virusTemp, plasmaTemp, mcellTemp = Model(singelConstants, virusTemp, plasmaTemp, mcellTemp)
        virus.append(virusTemp)
        plasma.append(plasmaTemp)
        mcell.append(mcellTemp)
    plotRange = range(Parameters.modelTimeTotal+1)
    
    plot.plot(plotRange, virus, color="red", linestyle="-", label = "virus")
    plot.plot(plotRange, plasma, color="blue", linestyle="-", label = "plasma")
    plot.plot(plotRange, mcell, color="green", linestyle="-", label = "mcell")
    plot.legend()
    canvas = FigureCanvasTkAgg(figure, content)
    canvas.get_tk_widget().grid(row = 1, column = 8,columnspan = 4, rowspan = 10, padx = 10, pady = 10)
   


def CreatePopulation():
    Parameters()
    agentPosition = np.ones([Parameters.populationSize,2])
    agentSpeed = np.ones(Parameters.populationSize)
    agentRotation = np.ones(Parameters.populationSize) 
    agentVirus = np.zeros(Parameters.populationSize)
    agentPlasma = np.zeros(Parameters.populationSize)
    agentMcell = np.zeros(Parameters.populationSize)
    agentSymptom = np.zeros(Parameters.populationSize)
    vaccinationList = list(range(Parameters.populationSize))
    
    for ix in range(Parameters.populationSize):
        agentPosition[ix][0] = np.random.uniform(0,Parameters.gridSizeSide)
        agentPosition[ix][1] = np.random.uniform(0,Parameters.gridSizeSide)
        agentSpeed[ix] = 0.2
        agentRotation[ix] = np.random.uniform(-np.pi,np.pi)
        if ix < Parameters.initialInfected:
            agentVirus[ix] = Parameters.initialVirusCount
        if ix < Parameters.initialImmune and ix > Parameters.initialInfected +  Parameters.initialImmune:
            agentPlasma[ix] = Parameters.initialPlasmaCount
            agentMcell[ix] = Parameters.initialMcellCount
    return agentPosition, agentSpeed, agentRotation, agentVirus, agentPlasma, agentMcell, agentSymptom, vaccinationList


def CreateModelConstant():
    Parameters()
    modelConstants = []
    parameterTimeChanger = Parameters.modelTimeChanger
    a = np.ones(Parameters.populationSize)*np.random.uniform(Parameters.aLower,Parameters.aUpper,Parameters.populationSize)/parameterTimeChanger #np.random.normal(2,0.2)
    b = np.ones(Parameters.populationSize)*np.random.uniform(Parameters.bLower,Parameters.bUpper,Parameters.populationSize)/parameterTimeChanger
    c = np.ones(Parameters.populationSize)*np.random.uniform(Parameters.cLower,Parameters.cUpper,Parameters.populationSize)/parameterTimeChanger # np.random.normal(1,0.1)
    d = np.ones(Parameters.populationSize)*np.random.uniform(Parameters.dLower,Parameters.dUpper,Parameters.populationSize)/parameterTimeChanger
    e = np.ones(Parameters.populationSize)*np.random.uniform(Parameters.eLower,Parameters.eUpper,Parameters.populationSize)/parameterTimeChanger
    f = np.ones(Parameters.populationSize)*np.random.uniform(Parameters.fLower,Parameters.fUpper,Parameters.populationSize)/parameterTimeChanger
    g = np.ones(Parameters.populationSize)*np.random.uniform(Parameters.gLower,Parameters.gUpper,Parameters.populationSize)/parameterTimeChanger
    modelConstants.append(a)
    modelConstants.append(b)
    modelConstants.append(c)
    modelConstants.append(d)
    modelConstants.append(e)
    modelConstants.append(f)
    modelConstants.append(g)
    return modelConstants

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
    virus = np.where(virus > 10, virus, 0)
    plasma = np.where(plasma > 10, plasma, 0)
    mcell = np.where(mcell > 2, mcell, 2)
    return virus, plasma, mcell


def Symptom(agentSymptom, plasma, plasmaMax):
    agentSymptom = np.zeros(len(agentSymptom))
    agentSymptom = np.where(plasma < 1*plasmaMax/4, agentSymptom, 1)
    agentSymptom = np.where(plasma < 2*plasmaMax/4, agentSymptom, 2)
    agentSymptom = np.where(plasma < 3*plasmaMax/4, agentSymptom, 3)
    agentSymptom = np.where(plasma < 4*plasmaMax/4, agentSymptom, 4)
    return agentSymptom


def DiseaseSpeading(gridStructure, virus, symptom):
    Parameters()
    for ix in range(Parameters.gridSizeSide):
        for jx in range(Parameters.gridSizeSide):
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
                        meetingProbability = np.power(1/2,symptom[localInfectedIndex])
                        if r < Parameters.infectionProbability*meetingProbability:
                            virus[localSuseptebleIndex] = virus[localSuseptebleIndex] + 100
    return virus


def main():
    print("")
    print("Run started")
    startTime = time.time()

    Parameters()
    agentPosition, agentSpeed, agentRotation, agentVirus, agentPlasma, agentMcell, agentSymptom, vaccinationList = CreatePopulation()
    modelConstants = CreateModelConstant()
    
    populationPlot = [[],[],[]]
    
    for timeTicker in range(Parameters.simulationTime):
        agentMovement = np.transpose([np.cos(agentRotation), np.sin(agentRotation)]*agentSpeed)
        agentPosition = agentPosition + agentMovement
        
        # Restrict movement
        agentPosition = np.where(agentPosition<Parameters.gridSizeSide,agentPosition,0.1)
        agentPosition = np.where(agentPosition>0, agentPosition, Parameters.gridSizeSide-0.1)
        

        # Change the rotation
        agentRotation = np.random.uniform(agentRotation - np.pi/4,
                                          agentRotation + np.pi/4)
        if timeTicker % Parameters.calculationTimer == 0 and timeTicker != 0:
            agentVirus, agentPlasma, agentMcell = Model(modelConstants, 
                                                        agentVirus, 
                                                        agentPlasma, 
                                                        agentMcell)
            
            agentSymptom = Symptom(agentSymptom, agentPlasma, Parameters.plasmaMax)
            
            
            gridStructure =[[[] for x in range(Parameters.gridSizeSide)] for y in range(Parameters.gridSizeSide)]
            flooredAgentPosition = np.floor(agentPosition)
            for agentIndex in range(Parameters.populationSize):
                rowIndex = flooredAgentPosition[agentIndex][0].astype('int')
                columnIndex = flooredAgentPosition[agentIndex][1].astype('int')
                gridStructure[rowIndex][columnIndex].append(agentIndex)
        
            agentVirus = DiseaseSpeading(gridStructure, agentVirus, agentSymptom)
            
            totalSusepteble = 0
            totalInfected = 0
            totalImmune = 0
            for ix in range(Parameters.populationSize):
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
            
    plt.figure()
    n = 5
    susepteblePlot = [sum(populationPlot[0][i:i+n])//n for i in range(0,len(populationPlot[0]),n)]
    infectedPlot = [sum(populationPlot[1][i:i+n])//n for i in range(0,len(populationPlot[1]),n)]
    immunePlot = [sum(populationPlot[2][i:i+n])//n for i in range(0,len(populationPlot[2]),n)]
    plotLength = np.linspace(0,len(populationPlot[0]),len(susepteblePlot))
    plt.plot(plotLength[:-1], susepteblePlot[:-1], 'g', plotLength[:-1], infectedPlot[:-1], 'r',
             plotLength[:-1], immunePlot[:-1], 'b')
    plt.xlabel('Timecycles')
    plt.ylabel('Number of agents')
    plt.legend(['susepteble', 'infected', 'symptomatic'])
    plt.show()

    executionTime = (time.time() - startTime)
    print('Total execution time in seconds: ' + str(executionTime))
    print("Run done")

# if __name__ == "__main__":
# Create the base root and parent
root = Tk()
content = ttk.Frame(root, padding=(3,3,12,12))

runButton = ttk.Button(content, text = "Run", command = main)
runInitialImmuneSystemButton = ttk.Button(content, text = "Update immune system", command = PlotInitialImmuneSystem)

parametersLabel = ttk.Label(content, text = "Parameters")
immuneParametersLabel = ttk.Label(content, text = "Immune parameters")
populationSizeLabel = ttk.Label(content, text ="Population size")
gridSizeSideLabel = ttk.Label(content, text = "Grid size side")
initialInfectedLabel = ttk.Label(content, text = "Initial Infected")
infectionProbabilityLabel = ttk.Label(content, text = "Infection probability")
initialImmuneLabel = ttk.Label(content, text = "Initial Immune")
plasmaMaxLabel = ttk.Label(content, text = "Plasma max")
totalVaccineDosesLabel = ttk.Label(content, text = "Total vaccine doses per CT")
simulationTimeLabel = ttk.Label(content, text = "Simulation time")
calculationTimerLabel = ttk.Label(content, text = "Calculation timew")
initialVirusCountLabel = ttk.Label(content, text = "Initial virus count")
initialPlasmaCountLabel = ttk.Label(content, text = "Initial plasma count")
initialMcellCountLabel = ttk.Label(content, text = "Initial mcell count")

modelTimeChangerLabel = ttk.Label(content, text = "Model time changer")
modelTimeTotalLabel = ttk.Label(content, text = "Total model time")
lowerParameterLabel = ttk.Label(content, text = "lower")
upperParameterLabel = ttk.Label(content, text = "Upper")
aLabel = ttk.Label(content, text = "a")
bLabel = ttk.Label(content, text = "b")
cLabel = ttk.Label(content, text = "c")
dLabel = ttk.Label(content, text = "d")
eLabel = ttk.Label(content, text = "e")
fLabel = ttk.Label(content, text = "f")
gLabel = ttk.Label(content, text = "g")


populationSizeEntry = ttk.Entry(content, width = 8)
gridSizeSideEntry = ttk.Entry(content, width = 8)
initialInfectedEntry = ttk.Entry(content, width = 8)
infectionProbabilityEntry = ttk.Entry(content, width = 8)
initialImmuneEntry = ttk.Entry(content, width = 8)
plasmaMaxEntry = ttk.Entry(content, width = 8)
totalVaccineDosesEntry = ttk.Entry(content, width = 8)
initialVirusCountEntry = ttk.Entry(content, width = 8)
initialPlasmaCountEntry = ttk.Entry(content, width = 8)
initialMcellCountEntry = ttk.Entry(content, width = 8)
simulationTimeEntry = ttk.Entry(content, width = 8)
calculationTimerEntry = ttk.Entry(content, width = 8)

modelTimeChangerEntry = ttk.Entry(content, width = 8)
modelTimeTotalEntry = ttk.Entry(content, width = 8)
aUpperEntry = ttk.Entry(content, width = 8)
aLowerEntry = ttk.Entry(content, width = 8)
bUpperEntry = ttk.Entry(content, width = 8)
bLowerEntry = ttk.Entry(content, width = 8)
cUpperEntry = ttk.Entry(content, width = 8)
cLowerEntry = ttk.Entry(content, width = 8)
dUpperEntry = ttk.Entry(content, width = 8)
dLowerEntry = ttk.Entry(content, width = 8)
eUpperEntry = ttk.Entry(content, width = 8)
eLowerEntry = ttk.Entry(content, width = 8)
fUpperEntry = ttk.Entry(content, width = 8)
fLowerEntry = ttk.Entry(content, width = 8)
gUpperEntry = ttk.Entry(content, width = 8)
gLowerEntry = ttk.Entry(content, width = 8)


# Insert default value
populationSizeEntry.insert(0,5000)
gridSizeSideEntry.insert(0,35)
initialInfectedEntry.insert(0,50)
infectionProbabilityEntry.insert(0,0.01)
initialImmuneEntry.insert(0,1000)
plasmaMaxEntry.insert(0,10000)
totalVaccineDosesEntry.insert(0,5)
simulationTimeEntry.insert(0,5000)
calculationTimerEntry.insert(0,100)
initialVirusCountEntry.insert(0,1000)
initialPlasmaCountEntry.insert(0,10000)
initialMcellCountEntry.insert(0,45000)

modelTimeChangerEntry.insert(0,10)
modelTimeTotalEntry.insert(0,100)
aUpperEntry.insert(0,1)
aLowerEntry.insert(0,1)
bUpperEntry.insert(0,0.5)
bLowerEntry.insert(0,0.5)
cUpperEntry.insert(0,1)
cLowerEntry.insert(0,0.1)
dUpperEntry.insert(0,0.001)
dLowerEntry.insert(0,0.001)
eUpperEntry.insert(0,3)
eLowerEntry.insert(0,3)
fUpperEntry.insert(0,0.5)
fLowerEntry.insert(0,0.5)
gUpperEntry.insert(0,1)
gLowerEntry.insert(0,1)


# Grid
content.grid(row=0, column = 0, sticky=(N, S, E, W))
runButton.grid(row = 0, column = 0, columnspan = 2)
modelTimeChangerLabel.grid(row = 0, column = 2)
modelTimeChangerEntry.grid(row = 0, column = 3)
runInitialImmuneSystemButton.grid(row = 0, column = 4)

rowIndex = 1
parametersLabel.grid(row = rowIndex, column = 0)
immuneParametersLabel.grid(row = rowIndex, column = 2)
lowerParameterLabel.grid(row = rowIndex, column = 3)
upperParameterLabel.grid(row = rowIndex, column = 4)

rowIndex = 2
populationSizeLabel.grid(row = rowIndex, column = 0)
populationSizeEntry.grid(row = rowIndex, column = 1)
aLabel.grid(row = rowIndex, column = 2)
aLowerEntry.grid(row = rowIndex, column = 3)
aUpperEntry.grid(row = rowIndex, column = 4)

rowIndex = 3
gridSizeSideLabel.grid(row = rowIndex, column = 0)
gridSizeSideEntry.grid(row = rowIndex, column = 1)
bLabel.grid(row = rowIndex, column = 2)
bLowerEntry.grid(row = rowIndex, column = 3)
bUpperEntry.grid(row = rowIndex, column = 4)

rowIndex = 4
initialInfectedLabel.grid(row = rowIndex, column = 0)
initialInfectedEntry.grid(row = rowIndex, column = 1)
cLabel.grid(row = rowIndex, column = 2)
cLowerEntry.grid(row = rowIndex, column = 3)
cUpperEntry.grid(row = rowIndex, column = 4)

rowIndex = 5
infectionProbabilityLabel.grid(row = rowIndex, column = 0)
infectionProbabilityEntry.grid(row = rowIndex, column = 1)
dLabel.grid(row = rowIndex, column = 2)
dLowerEntry.grid(row = rowIndex, column = 3)
dUpperEntry.grid(row = rowIndex, column = 4)

rowIndex = 6
initialImmuneLabel.grid(row = rowIndex, column = 0)
initialImmuneEntry.grid(row = rowIndex, column = 1)
eLabel.grid(row = rowIndex, column = 2)
eLowerEntry.grid(row = rowIndex, column = 3)
eUpperEntry.grid(row = rowIndex, column = 4)

rowIndex = 7
plasmaMaxLabel.grid(row = rowIndex, column = 0)
plasmaMaxEntry.grid(row = rowIndex, column = 1)
fLabel.grid(row = rowIndex, column = 2)
fLowerEntry.grid(row = rowIndex, column = 3)
fUpperEntry.grid(row = rowIndex, column = 4)

rowIndex = 8
totalVaccineDosesLabel.grid(row = rowIndex, column = 0)
totalVaccineDosesEntry.grid(row = rowIndex, column = 1)
gLabel.grid(row = rowIndex, column = 2)
gLowerEntry.grid(row = rowIndex, column = 3)
gUpperEntry.grid(row = rowIndex, column = 4)


rowIndex = 9
simulationTimeLabel.grid(row = rowIndex, column = 0)
simulationTimeEntry.grid(row = rowIndex, column = 1)
modelTimeTotalLabel.grid(row = rowIndex, column = 2)
modelTimeTotalEntry.grid(row = rowIndex, column = 3)


rowIndex = 10
calculationTimerLabel.grid(row = rowIndex, column = 0)
calculationTimerEntry.grid(row = rowIndex, column = 1)

rowIndex = 11
initialVirusCountLabel.grid(row = rowIndex, column = 0)
initialVirusCountEntry.grid(row = rowIndex, column = 1)

rowIndex = 12
initialPlasmaCountLabel.grid(row = rowIndex, column = 0)
initialPlasmaCountEntry.grid(row = rowIndex, column = 1)

rowIndex = 13
initialMcellCountLabel.grid(row = rowIndex, column = 0)
initialMcellCountEntry.grid(row = rowIndex, column = 1)

# Keybindings
root.bind('<Return>', lambda e: runButton.invoke())
runInitialImmuneSystemButton.invoke()

root.mainloop()
