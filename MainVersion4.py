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
    
    Parameters.symptomOne = int(symptomOneEntry.get())
    Parameters.symptomTwo = int(symptomTwoEntry.get())
    Parameters.symptomThree = int(symptomThreeEntry.get())
    Parameters.symptomFour = int(symptomFourEntry.get())
    
def PlotInitialImmuneSystem():
    Parameters()

    # Create the figure in the GUI
    figure = Figure(figsize=(10, 8), dpi=70)
    plotAll = figure.add_subplot(2, 2, 1)
    plotVirus = figure.add_subplot(2, 2, 2)
    plotPlasma = figure.add_subplot(2, 2, 3)
    plotMcell = figure.add_subplot(2, 2, 4)
    plotAll.set_xlabel("Timecycle")
    plotAll.set_ylabel("Cells")
    lowerConstants = np.array([Parameters.aLower, Parameters.bLower, Parameters.cLower, Parameters.dLower, Parameters.eLower, Parameters.fLower, Parameters.gLower])/Parameters.modelTimeChanger
    upperConstants = np.array([Parameters.aUpper, Parameters.bUpper, Parameters.cUpper, Parameters.dUpper, Parameters.eUpper, Parameters.fUpper, Parameters.gUpper])/Parameters.modelTimeChanger
    for count, singleConstants in enumerate([lowerConstants, upperConstants]):
        virus = [Parameters.initialVirusCount]
        plasma = [Parameters.initialPlasmaCount]
        mcell = [Parameters.initialMcellCount]
        
        virusTemp = Parameters.initialVirusCount
        plasmaTemp = 0
        mcellTemp = 10
    
        for ix in range(Parameters.modelTimeTotal):
            virusTemp, plasmaTemp, mcellTemp = Model(singleConstants, virusTemp, plasmaTemp, mcellTemp)
            virus.append(virusTemp)
            plasma.append(plasmaTemp)
            mcell.append(mcellTemp)
        plotRange = range(Parameters.modelTimeTotal+1)
        
        if count == 0:
            plotAll.plot(plotRange, virus, color="red", linestyle="--", label = "lower", alpha = 0.5)
            plotAll.plot(plotRange, plasma, color="blue", linestyle="--", alpha = 0.5)
            plotAll.plot(plotRange, mcell, color="green", linestyle="--", alpha = 0.5)
            plotVirus.plot(plotRange, virus, color="red", linestyle="--", label = "virus, lower", alpha = 0.5)
            plotPlasma.plot(plotRange, plasma, color="blue", linestyle="--", label = "plasma, lower", alpha = 0.5)
            plotMcell.plot(plotRange, mcell, color="green", linestyle="--", label = "mcell, lower",alpha = 0.5)
        else: 
            plotAll.plot(plotRange, virus, color="red", linestyle="-", label = "upper")
            plotAll.plot(plotRange, plasma, color="blue", linestyle="-")
            plotAll.plot(plotRange, mcell, color="green", linestyle="-")
            plotVirus.plot(plotRange, virus, color="red", linestyle="-", label = "virus, upper")
            plotPlasma.plot(plotRange, plasma, color="blue", linestyle="-", label = "plasma, upper")
            plotMcell.plot(plotRange, mcell, color="green", linestyle="-", label = "mcell, upper") #"f = {:f}".format(singleConstants[5]) 
    plotPlasma.plot([0,Parameters.modelTimeTotal+1],[Parameters.symptomOne,Parameters.symptomOne], color="black", linestyle="--", label = "Symptom")
    plotPlasma.plot([0,Parameters.modelTimeTotal+1],[Parameters.symptomTwo,Parameters.symptomTwo], color="black", linestyle="--")
    plotPlasma.plot([0,Parameters.modelTimeTotal+1],[Parameters.symptomThree,Parameters.symptomThree], color="black", linestyle="--")
    plotPlasma.plot([0,Parameters.modelTimeTotal+1],[Parameters.symptomFour,Parameters.symptomFour], color="black", linestyle="--")
    plotPlasma.text(Parameters.modelTimeTotal,Parameters.symptomOne, "1")
    plotPlasma.text(0,Parameters.symptomTwo, "2")
    plotPlasma.text(Parameters.modelTimeTotal,Parameters.symptomThree, "3")
    plotPlasma.text(0,Parameters.symptomFour, "4")
    for plot in [plotAll,plotVirus,plotPlasma, plotMcell]:
        plot.legend()
        plot.grid()
        plot.set_yscale('log')
    canvas = FigureCanvasTkAgg(figure, content)
    canvas.get_tk_widget().grid(row = 1, column = 8,columnspan = 40, rowspan = 100, padx = 10, pady = 10)
   


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


def Symptom(agentSymptom, plasma):
    Parameters()
    agentSymptom = np.zeros(len(agentSymptom))
    agentSymptom = np.where(plasma < Parameters.symptomOne, agentSymptom, 1)
    agentSymptom = np.where(plasma < Parameters.symptomTwo, agentSymptom, 2)
    agentSymptom = np.where(plasma < Parameters.symptomThree, agentSymptom, 3)
    agentSymptom = np.where(plasma < Parameters.symptomFour, agentSymptom, 4)
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
                            virus[localSuseptebleIndex] = virus[localSuseptebleIndex] + virus[localInfectedIndex]*0.01
    return virus

def DiseaseSpeadingQuarantine(gridStructure, virus, symptom):
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
                        meetingProbability = np.power(1/2,symptom[localInfectedIndex])/100
                        if r < Parameters.infectionProbability*meetingProbability:
                            virus[localSuseptebleIndex] = virus[localSuseptebleIndex] + virus[localInfectedIndex]*0.01
    return virus

def main():
    print("")
    print("Run started")
    startTime = time.time()

    Parameters()
    agentPosition, agentSpeed, agentRotation, agentVirus, agentPlasma, agentMcell, agentSymptom, vaccinationList = CreatePopulation()
    modelConstants = CreateModelConstant()
    
    populationPlot = [[],[],[],[]]
    virusMeanPlot = []
    
    if vaccinationOn.get() == True:
        vaccinationList = list(range(Parameters.populationSize))
        agentVirusFake = np.zeros(Parameters.populationSize)
        agentPlasmaFake = np.zeros(Parameters.populationSize)
        agentMcellFake = np.zeros(Parameters.populationSize)
        modelConstantsVaccine = CreateModelConstant()
        modelConstantsVaccine[5] = modelConstantsVaccine[5]/10


    if quarantineOn.get() == True:
        startQuarantine = False
        quarantineTime = 0
        totalInfected = 0
        
        
    if symptomPlotOn.get() == True:
        symptomPlot = []

    ##### SIMULAION START #####        
    for timeTicker in range(Parameters.simulationTime*Parameters.calculationTimer):
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
            
            agentSymptom = Symptom(agentSymptom, agentPlasma)
            
            gridStructure =[[[] for x in range(Parameters.gridSizeSide)] for y in range(Parameters.gridSizeSide)]
            flooredAgentPosition = np.floor(agentPosition)
            for agentIndex in range(Parameters.populationSize):
                rowIndex = flooredAgentPosition[agentIndex][0].astype('int')
                columnIndex = flooredAgentPosition[agentIndex][1].astype('int')
                gridStructure[rowIndex][columnIndex].append(agentIndex)
            
            if quarantineOn.get() == True:
                if totalInfected/Parameters.populationSize > 0.3:
                    startQuarantine = True
                if quarantineTime > 360:
                    startQuarantine = False
                if startQuarantine == True:
                    agentVirus = DiseaseSpeadingQuarantine(gridStructure, agentVirus, agentSymptom)
                    quarantineTime += 1
                else:
                    agentVirus = DiseaseSpeading(gridStructure, agentVirus, agentSymptom)
            else:
                agentVirus = DiseaseSpeading(gridStructure, agentVirus, agentSymptom)
            
            if vaccinationOn.get() == True:
                vaccineDoses = 0
                removeIndex= []
                for index, ix in enumerate(vaccinationList):
                    if vaccineDoses < Parameters.totalVaccineDoses:
                        if all([agentVirus[ix] == 0, agentPlasma[ix] == 0]):
                            agentVirusFake[ix] = 100 
                            removeIndex.append(index)
                            vaccineDoses = vaccineDoses + 1
                agentVirusFake, agentPlasmaFake, agentMcellFake = Model(modelConstantsVaccine, 
                                                                        agentVirusFake, 
                                                                        agentPlasmaFake, 
                                                                        agentMcellFake)
                agentMcell += agentMcellFake
                vaccinationList = np.delete(vaccinationList,removeIndex)
                vaccinationList.tolist()
                
            totalInfected = 0
            totalSymptomatic = 0
            totalImmune = 0
            totalSusepteble = 0
            for ix in range(Parameters.populationSize):
                if agentVirus[ix] > 0 :
                    totalInfected += +1
                elif all([agentVirus[ix] == 0, agentPlasma[ix] > Parameters.symptomOne]):
                    totalSymptomatic +=  1
                elif all([agentVirus[ix] == 0, agentPlasma[ix] == 0, agentMcell[ix] > 5000]): 
                    totalImmune +=  1
                else:
                    totalSusepteble += 1            
            if totalInfected == 0:
                break
            virusMeanPlot.append(np.mean(agentVirus))
            
            populationPlot[0].append(totalInfected)
            populationPlot[1].append(totalSymptomatic)
            populationPlot[2].append(totalImmune)
            populationPlot[3].append(totalSusepteble)
            if symptomPlotOn.get() == True:
                symptomPlot.append(np.sort(agentSymptom).tolist())

    if virusMeanOn.get() == True:
        plt.plot(virusMeanPlot)
        plt.show()
        
    if plotOn.get() == True:    
        plt.figure()
        n = 5
        infectedPlot    = [sum(populationPlot[0][i:i+n])//n for i in range(0,len(populationPlot[1]),n)]
        symptomaticPlot = [sum(populationPlot[1][i:i+n])//n for i in range(0,len(populationPlot[1]),n)]
        immunePlot      = [sum(populationPlot[2][i:i+n])//n for i in range(0,len(populationPlot[2]),n)]
        susepteblePlot  = [sum(populationPlot[3][i:i+n])//n for i in range(0,len(populationPlot[3]),n)]
        plotLength = np.linspace(0,len(populationPlot[0]),len(susepteblePlot))
        plt.plot(plotLength[:-1], infectedPlot[:-1], 'r', label = 'infected')
        plt.plot(plotLength[:-1], immunePlot[:-1], 'b', label = 'symptomatic')
        plt.plot(plotLength[:-1], symptomaticPlot[:-1], 'orange', label = 'immune')    
        plt.plot(plotLength[:-1], susepteblePlot[:-1], 'g', label = 'susepteble')
        plt.xlabel('Timecycles', fontsize=12)
        plt.ylabel('Number of agents', fontsize=12)
        plt.legend()
        modelConstantsTextLower = 'Lower: a= {:.2f}, b= {:.2f}, c= {:.2f}, d= {:.3f}, e= {:.2f}, f= {:.2f}, g= {:.2f}'.format(Parameters.aLower, Parameters.bLower, Parameters.cLower, Parameters.dLower, Parameters.eLower, Parameters.fLower, Parameters.gLower)
        plt.figtext(0.5, -0.05, modelConstantsTextLower, ha="center", fontsize=12) 
        modelConstantsTextUpper = 'Upper: a= {:.2f}, b= {:.2f}, c= {:.2f}, d= {:.3f}, e= {:.2f}, f= {:.2f}, g= {:.2f}'.format(Parameters.aUpper, Parameters.bLower, Parameters.cUpper, Parameters.dUpper, Parameters.eUpper, Parameters.fUpper, Parameters.gUpper)
        plt.figtext(0.5, -0.10, modelConstantsTextUpper, ha="center", fontsize=12)  
        plt.show()
    
    if symptomPlotOn.get() == True:
        fig, ax = plt.subplots()
        im = ax.imshow(symptomPlot, cmap="YlGn")
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

parametersLabel = ttk.Label(content, text = "Parameters", font = 15)
checkboxLabel = ttk.Label(content, text = "Features", font = 15)
immuneParametersLabel = ttk.Label(content, text = "Immune parameters")
populationSizeLabel = ttk.Label(content, text ="Population size")
gridSizeSideLabel = ttk.Label(content, text = "Grid size side")
initialInfectedLabel = ttk.Label(content, text = "Initial Infected")
infectionProbabilityLabel = ttk.Label(content, text = "Infection probability")
initialImmuneLabel = ttk.Label(content, text = "Initial Immune")
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
symptomOneLabel = ttk.Label(content, text = "Symptom 1")
symptomTwoLabel = ttk.Label(content, text = "Symptom 2")
symptomThreeLabel = ttk.Label(content, text = "Symptom 3")
symptomFourLabel = ttk.Label(content, text = "Symptom 4")


populationSizeEntry = ttk.Entry(content, width = 8)
gridSizeSideEntry = ttk.Entry(content, width = 8)
initialInfectedEntry = ttk.Entry(content, width = 8)
infectionProbabilityEntry = ttk.Entry(content, width = 8)
initialImmuneEntry = ttk.Entry(content, width = 8)
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
symptomOneEntry = ttk.Entry(content, width = 8)
symptomTwoEntry = ttk.Entry(content, width = 8)
symptomThreeEntry = ttk.Entry(content, width = 8)
symptomFourEntry = ttk.Entry(content, width = 8)

plotOn = BooleanVar(value=1)
plotOnCheck = ttk.Checkbutton(content, text = "Agent condition plot", variable = plotOn)
vaccinationOn = BooleanVar(value = 0)
vaccinationCheck = ttk.Checkbutton(content, text = "Vaccination", variable = vaccinationOn)
virusMeanOn = BooleanVar(value = 0)
virusMeanCheck =  ttk.Checkbutton(content, text = "Virus mean plot", variable = virusMeanOn)
symptomPlotOn = BooleanVar(value = 0)
symptomPlotCheck = ttk.Checkbutton(content, text = "Symptom plot", variable = symptomPlotOn)
quarantineOn = BooleanVar(value = 0)
quarantineCheck = ttk.Checkbutton(content, text = "Quarantine", variable = quarantineOn)

# Insert default value
populationSizeEntry.insert(0,5000)
gridSizeSideEntry.insert(0,35)
initialInfectedEntry.insert(0,50)
infectionProbabilityEntry.insert(0,0.02)
initialImmuneEntry.insert(0,1000)

totalVaccineDosesEntry.insert(0,5)
simulationTimeEntry.insert(0,1000)
calculationTimerEntry.insert(0,100)
initialVirusCountEntry.insert(0,1000)
initialPlasmaCountEntry.insert(0,10000)
initialMcellCountEntry.insert(0,45000)

modelTimeChangerEntry.insert(0,18)
modelTimeTotalEntry.insert(0,200)
aUpperEntry.insert(0,3)
aLowerEntry.insert(0,0.9)
bUpperEntry.insert(0,0.5)
bLowerEntry.insert(0,0.5)
cUpperEntry.insert(0,0.1)
cLowerEntry.insert(0,0.1)
dUpperEntry.insert(0,0.001)
dLowerEntry.insert(0,0.001)
eUpperEntry.insert(0,3)
eLowerEntry.insert(0,3)
fUpperEntry.insert(0,0.5)
fLowerEntry.insert(0,0.5)
gUpperEntry.insert(0,0.1)
gLowerEntry.insert(0,0.1)
symptomOneEntry.insert(0,10000)
symptomTwoEntry.insert(0,100000)
symptomThreeEntry.insert(0,1000000)
symptomFourEntry.insert(0,10000000)


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

rowIndex += 1
populationSizeLabel.grid(row = rowIndex, column = 0)
populationSizeEntry.grid(row = rowIndex, column = 1)
aLabel.grid(row = rowIndex, column = 2)
aLowerEntry.grid(row = rowIndex, column = 3)
aUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
gridSizeSideLabel.grid(row = rowIndex, column = 0)
gridSizeSideEntry.grid(row = rowIndex, column = 1)
bLabel.grid(row = rowIndex, column = 2)
bLowerEntry.grid(row = rowIndex, column = 3)
bUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
initialInfectedLabel.grid(row = rowIndex, column = 0)
initialInfectedEntry.grid(row = rowIndex, column = 1)
cLabel.grid(row = rowIndex, column = 2)
cLowerEntry.grid(row = rowIndex, column = 3)
cUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
infectionProbabilityLabel.grid(row = rowIndex, column = 0)
infectionProbabilityEntry.grid(row = rowIndex, column = 1)
dLabel.grid(row = rowIndex, column = 2)
dLowerEntry.grid(row = rowIndex, column = 3)
dUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
initialImmuneLabel.grid(row = rowIndex, column = 0)
initialImmuneEntry.grid(row = rowIndex, column = 1)
eLabel.grid(row = rowIndex, column = 2)
eLowerEntry.grid(row = rowIndex, column = 3)
eUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
totalVaccineDosesLabel.grid(row = rowIndex, column = 0)
totalVaccineDosesEntry.grid(row = rowIndex, column = 1)
fLabel.grid(row = rowIndex, column = 2)
fLowerEntry.grid(row = rowIndex, column = 3)
fUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
simulationTimeLabel.grid(row = rowIndex, column = 0)
simulationTimeEntry.grid(row = rowIndex, column = 1)
gLabel.grid(row = rowIndex, column = 2)
gLowerEntry.grid(row = rowIndex, column = 3)
gUpperEntry.grid(row = rowIndex, column = 4)


rowIndex += 1
calculationTimerLabel.grid(row = rowIndex, column = 0)
calculationTimerEntry.grid(row = rowIndex, column = 1)
modelTimeTotalLabel.grid(row = rowIndex, column = 2)
modelTimeTotalEntry.grid(row = rowIndex, column = 3)


rowIndex += 1
initialVirusCountLabel.grid(row = rowIndex, column = 0)
initialVirusCountEntry.grid(row = rowIndex, column = 1)
symptomOneLabel.grid(row = rowIndex, column = 2)
symptomOneEntry.grid(row = rowIndex, column = 3)

rowIndex += 1
initialPlasmaCountLabel.grid(row = rowIndex, column = 0)
initialPlasmaCountEntry.grid(row = rowIndex, column = 1)
symptomTwoLabel.grid(row = rowIndex, column = 2)
symptomTwoEntry.grid(row = rowIndex, column = 3)

rowIndex += 1
initialMcellCountLabel.grid(row = rowIndex, column = 0)
initialMcellCountEntry.grid(row = rowIndex, column = 1)
symptomThreeLabel.grid(row = rowIndex, column = 2)
symptomThreeEntry.grid(row = rowIndex, column = 3)


rowIndex += 1
checkboxLabel.grid(row = rowIndex, column = 0)
symptomFourLabel.grid(row = rowIndex, column = 2)
symptomFourEntry.grid(row = rowIndex, column = 3)

rowIndex += 1
plotOnCheck.grid(row = rowIndex, column = 0, sticky = W)

rowIndex += 1
vaccinationCheck.grid(row = rowIndex, column = 0, sticky = W)

rowIndex += 1
virusMeanCheck.grid(row = rowIndex, column = 0, sticky = W)

rowIndex += 1
symptomPlotCheck.grid(row = rowIndex, column = 0, sticky = W)

rowIndex += 1
quarantineCheck.grid(row = rowIndex, column = 0, sticky = W)

# Keybindings
root.bind('<Return>', lambda e: runInitialImmuneSystemButton.invoke())
runInitialImmuneSystemButton.invoke()

root.mainloop()
