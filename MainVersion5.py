# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 12:28:22 2021

@author: kevin
"""
#% Main

import numpy as np
import matplotlib.pyplot as plt
# matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *
from tkinter import ttk

import os

import time

def Parameters():
    Parameters.simulationTime = int(simulationTimeEntry.get())
    Parameters.calculationTimer = int(calculationTimerEntry.get())
    Parameters.populationSize = int(populationSizeEntry.get())
    Parameters.gridSizeSide = int(gridSizeSideEntry.get())
    Parameters.infectionProbability = float(infectionProbabilityEntry.get())
    Parameters.initialInfected = int(initialInfectedEntry.get())
    Parameters.initialImmune = int(initialImmuneEntry.get())
    Parameters.initialVirusCount = int(initialVirusCountEntry.get())
    Parameters.initialPlasmaCount = int(initialPlasmaCountEntry.get())
    Parameters.initialMcellCount = int(initialMcellCountEntry.get())
    Parameters.totalVaccineDoses = int(totalVaccineDosesEntry.get())
    Parameters.vaccineEfficacy = float(vaccineEfficacyEntry.get())
    
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
        plasmaTemp = Parameters.initialPlasmaCount
        mcellTemp = Parameters.initialMcellCount
    
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
    plotPlasma.plot([0,Parameters.modelTimeTotal+1],[Parameters.symptomTwo,Parameters.symptomTwo], color="black", linestyle="--", label = "Symptom")
    plotPlasma.plot([0,Parameters.modelTimeTotal+1],[Parameters.symptomThree,Parameters.symptomThree], color="black", linestyle="--")
    plotPlasma.plot([0,Parameters.modelTimeTotal+1],[Parameters.symptomFour,Parameters.symptomFour], color="black", linestyle="--")
    plotPlasma.text(0,Parameters.symptomTwo/2.5, "1")
    plotPlasma.text(0,Parameters.symptomTwo, "2")
    plotPlasma.text(0,Parameters.symptomThree, "3")
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
        if all([ix > Parameters.initialInfected, ix < Parameters.initialInfected +  Parameters.initialImmune]) == True:
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
    virus = np.where(virus > 20, virus, 0)
    plasma = np.where(plasma > 5, plasma, 0)
    mcell = np.where(mcell > 2, mcell, 2)
    return virus, plasma, mcell


def Symptom(agentSymptom, plasma):
    Parameters()
    agentSymptom = np.zeros(len(agentSymptom)).astype('int')
    agentSymptom = np.where(plasma < Parameters.symptomTwo, agentSymptom, 1)
    agentSymptom = np.where(plasma < Parameters.symptomThree, agentSymptom, 2)
    agentSymptom = np.where(plasma < Parameters.symptomFour, agentSymptom, 3)
    return agentSymptom


def DiseaseSpeading(gridStructure, virus, symptom, infectionProbabilityIndex):
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
                        meetingProbability = np.power(1/5,symptom[localInfectedIndex])
                        infectionProbability = infectionProbabilityIndex[localSuseptebleIndex]
                        if r < infectionProbability*meetingProbability:
                            virus[localSuseptebleIndex] = virus[localSuseptebleIndex] + virus[localInfectedIndex]*0.01
    return virus


def main():
    print("Run started")
    startTime = time.time()

    Parameters()
    agentPosition, agentSpeed, agentRotation, agentVirus, agentPlasma, agentMcell, agentSymptom, vaccinationList = CreatePopulation()
    modelConstants = CreateModelConstant()
    
    populationPlot = [[],[],[],[]]
    virusMeanPlot = []
    
    agentInfectionProbability = np.ones(Parameters.populationSize)*Parameters.infectionProbability
    
    if vaccinationOn.get() == True:
        vaccinationList = list(range(Parameters.populationSize))
        if diseaseModifyingOn.get() == True:
            agentVirusFake = np.zeros(Parameters.populationSize)
            agentPlasmaFake = np.zeros(Parameters.populationSize)
            agentMcellFake = np.zeros(Parameters.populationSize)
            modelConstantsVaccine = CreateModelConstant()
                
        
        
    if symptomPlotOn.get() == True:
        symptomPlot = []
        
    timecycle = 0
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
            timecycle += 1
            
            
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
            

            agentVirus = DiseaseSpeading(gridStructure, agentVirus, agentSymptom, agentInfectionProbability)
            
            if vaccinationOn.get() == True:
                if timecycle > int(vaccineTimeDelayEntry.get()):
                    vaccineDoses = 0
                    removeIndex= []
                    for index, ix in enumerate(vaccinationList):
                        if vaccineDoses < Parameters.totalVaccineDoses:
                            if all([agentVirus[ix] == 0, agentPlasma[ix] == 0]):
                                if diseaseModifyingOn.get() == True:
                                    r = np.random.rand()
                                    if r < Parameters.vaccineEfficacy:
                                        modelConstantsVaccine[5][ix] = modelConstantsVaccine[5][ix]*100
                                        modelConstantsVaccine[6][ix] = modelConstantsVaccine[6][ix]/10
                                    agentVirusFake[ix] = 100 
                                if preventiveVaccineOn.get() == True:
                                    agentInfectionProbability[ix] = agentInfectionProbability[ix]/5
                                removeIndex.append(index)
                                vaccineDoses += 1
                    if diseaseModifyingOn.get() == True:
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
                if agentVirus[ix] > 10 :
                    totalInfected += +1
                if agentPlasma[ix] > Parameters.symptomTwo:
                    totalSymptomatic +=  1
                if  agentMcell[ix] > 50000: 
                    totalImmune +=  1
                if all([agentVirus[ix] < 10, agentPlasma[ix] < Parameters.symptomTwo, agentMcell[ix] < 50000]):
                    totalSusepteble += 1         
            
            if breakOn.get() == True:
                if totalInfected == 0:
                    break
            
            
            populationPlot[0].append(totalInfected)
            populationPlot[1].append(totalSymptomatic)
            populationPlot[2].append(totalImmune)
            populationPlot[3].append(totalSusepteble)
            
            if symptomPlotOn.get() == True:
                symptomPlot.append(agentSymptom)
            if virusMeanOn.get() == True:
                virusMeanPlot.append(np.mean(agentVirus))
                
    if virusMeanOn.get() == True:
        plt.xlabel('Timecycles')
        plt.ylabel()
        plt.plot(virusMeanPlot, label = 'Virus mean')
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
        plt.plot(plotLength[:-1], immunePlot[:-1], 'b', label = 'immune')
        plt.plot(plotLength[:-1], symptomaticPlot[:-1], 'orange', label = 'symptomatic')    
        plt.plot(plotLength[:-1], susepteblePlot[:-1], 'g', label = 'susepteble')
        plt.xlabel('Timecycles', fontsize=12)
        plt.ylabel('Number of agents', fontsize=12)
        plt.legend()
        modelConstantsTextLower = 'Lower: a= {:.2f}, b= {:.2f}, c= {:.2f}, d= {:.4f}, e= {:.2f}, f= {:.2f}, g= {:.2f}'.format(Parameters.aLower, Parameters.bLower, Parameters.cLower, Parameters.dLower, Parameters.eLower, Parameters.fLower, Parameters.gLower)
        plt.figtext(0.5, -0.05, modelConstantsTextLower, ha="center", fontsize=12) 
        modelConstantsTextUpper = 'Upper: a= {:.2f}, b= {:.2f}, c= {:.2f}, d= {:.4f}, e= {:.2f}, f= {:.2f}, g= {:.2f}'.format(Parameters.aUpper, Parameters.bLower, Parameters.cUpper, Parameters.dUpper, Parameters.eUpper, Parameters.fUpper, Parameters.gUpper)
        plt.figtext(0.5, -0.10, modelConstantsTextUpper, ha="center", fontsize=12)
        vaccineText = 'Vaccine {}, preventive {}, disease modifying {}'.format(vaccinationOn.get(),preventiveVaccineOn.get(),diseaseModifyingOn.get())
        plt.figtext(0.5, -0.15, vaccineText, ha="center", fontsize=12)
        plt.show()
    
    if symptomPlotOn.get() == True:
        fig, ax = plt.subplots(2)
        ax[0].imshow(symptomPlot, cmap="twilight") #YlGn
        ax[1].imshow(np.sort(symptomPlot).tolist(), cmap="twilight")
        plt.show()
        
        
    executionTime = (time.time() - startTime)
    print('Total execution time in seconds: ' + str(executionTime))
    print("Run done")
    print("")
    
    if value_check.get() == True:
        return populationPlot
    
        
    

def multipleRuns():
    Parameters()
    print("Multiple runs started")
    print("Total number of runs {}".format(multipleRunsEntry.get()))
    print("Run number 1")
    populationPlot = main()
    n = 5
    # 0 = infected, 1 = symptomatic, 2 = immune, 3 = susepteble
    infected    = np.array([[sum(populationPlot[0][i:i+n])//n for i in range(0,len(populationPlot[1]),n)]])
    symptomatic = np.array([[sum(populationPlot[1][i:i+n])//n for i in range(0,len(populationPlot[1]),n)]])
    immune      = np.array([[sum(populationPlot[2][i:i+n])//n for i in range(0,len(populationPlot[2]),n)]])
    susepteble  = np.array([[sum(populationPlot[3][i:i+n])//n for i in range(0,len(populationPlot[3]),n)]])
    for count in range(1,int(multipleRunsEntry.get())):
        print("Run number {}".format(count+1))
        populationPlot = main()
        n = 5
        infectedPlot    = np.array([[sum(populationPlot[0][i:i+n])//n for i in range(0,len(populationPlot[1]),n)]])
        symptomaticPlot = np.array([[sum(populationPlot[1][i:i+n])//n for i in range(0,len(populationPlot[1]),n)]])
        immunePlot      = np.array([[sum(populationPlot[2][i:i+n])//n for i in range(0,len(populationPlot[2]),n)]])
        susepteblePlot  = np.array([[sum(populationPlot[3][i:i+n])//n for i in range(0,len(populationPlot[3]),n)]])
        infected    = np.append(infected,infectedPlot, axis = 0)
        symptomatic = np.append(symptomatic,symptomaticPlot, axis = 0)
        immune      = np.append(immune,immunePlot, axis = 0)
        susepteble  = np.append(susepteble,susepteblePlot, axis = 0)
    
    infectedError = np.std(infected,axis=0)
    symptomaticError = np.std(symptomatic,axis=0)
    immuneError = np.std(immune,axis=0)
    suseptebleError = np.std(susepteble,axis=0)
    infectedMean = np.mean(infected,axis = 0)
    symptomaticMean = np.mean(symptomatic,axis = 0)
    immuneMean = np.mean(immune,axis = 0)
    suseptebleMean = np.mean(susepteble,axis = 0)
    plotLength = np.linspace(0, Parameters.simulationTime,len(infectedMean))

    for mean, error, color, text in [[infectedMean, infectedError, 'red', 'infected'],\
                               [symptomaticMean, symptomaticError, 'orange', 'symptomatic'],\
                                   [immuneMean, immuneError, 'blue', 'immune'],\
                                [suseptebleMean, suseptebleError, 'green', 'susepteble']]:
        plt.plot(plotLength[:-1], mean[:-1], c = color, label = text)
        ciLower = mean - 2*error
        ciLowerBounded = np.where(ciLower>0,ciLower,0)
        ciUpper = mean + 2*error
        ciUpperBounded = np.where(ciUpper<Parameters.populationSize,ciUpper, Parameters.populationSize)
        plt.fill_between(plotLength[:-1], ciLowerBounded[:-1], ciUpperBounded[:-1], color = color, alpha = 0.3)
     
    plt.legend()
    plt.xlabel('Time cycle')
    plt.ylabel('Agents')
    modelConstantsTextLower = 'Lower: a= {:.2f}, b= {:.2f}, c= {:.2f}, d= {:.4f}, e= {:.2f}, f= {:.2f}, g= {:.2f}'.format(Parameters.aLower, Parameters.bLower, Parameters.cLower, Parameters.dLower, Parameters.eLower, Parameters.fLower, Parameters.gLower)
    plt.figtext(0.5, -0.05, modelConstantsTextLower, ha="center", fontsize=12) 
    modelConstantsTextUpper = 'Upper: a= {:.2f}, b= {:.2f}, c= {:.2f}, d= {:.4f}, e= {:.2f}, f= {:.2f}, g= {:.2f}'.format(Parameters.aUpper, Parameters.bLower, Parameters.cUpper, Parameters.dUpper, Parameters.eUpper, Parameters.fUpper, Parameters.gUpper)
    plt.figtext(0.5, -0.10, modelConstantsTextUpper, ha="center", fontsize=12)
    vaccineText = 'Vaccine {}, preventive {}, disease modifying {}'.format(vaccinationOn.get(),preventiveVaccineOn.get(),diseaseModifyingOn.get())
    plt.figtext(0.5, -0.15, vaccineText, ha="center", fontsize=12)
    
    if saveOn.get() == True:
        filename = os.path.join('/Users\kevin\Documents\GitHub\Exjobb\image',filenameEntry.get())
        plt.savefig(filename+'.png')
    plt.show()
    
    if saveOn.get() == True:
        filename = os.path.join('/Users\kevin\Documents\GitHub\Exjobb\data',filenameEntry.get())
        np.save(filename+'infected', infected)
        np.save(filename+'symptomatic', symptomatic)
        np.save(filename+'immune', immune)
        np.save(filename+'susepteble', susepteble)
    
    


def activate_enable_button():
    # multipleRunsButton.config(state=DISABLED if value_check.get() else NORMAL)
    multipleRunsButton.config(state=NORMAL if value_check.get() else DISABLED)
    multipleRunsEntry.config(state=NORMAL if value_check.get() else DISABLED)
    breakOn.set(False)
    breakOnCheck.config(state=DISABLED if value_check.get() else NORMAL)
    saveOn.set(True)

    
# if __name__ == "__main__":
# Create the base root and parent
root = Tk()
content = ttk.Frame(root, padding=(3,3,12,12))

runButton = ttk.Button(content, text = "Run",  command = lambda:[plotOn.set(True),main()])
runInitialImmuneSystemButton = ttk.Button(content, text = "Update immune system", command = PlotInitialImmuneSystem)
multipleRunsButton = ttk.Button(content, text = "Multiple runs", command = multipleRuns, state = DISABLED)

parametersLabel = ttk.Label(content, text = "Parameters", font = 15)
checkboxLabel = ttk.Label(content, text = "Features", font = 15)
immuneParametersLabel = ttk.Label(content, text = "Immune parameters")

simulationTimeLabel = ttk.Label(content, text = "Simulation time")
calculationTimerLabel = ttk.Label(content, text = "Calculation time")
populationSizeLabel = ttk.Label(content, text ="Population size")
gridSizeSideLabel = ttk.Label(content, text = "Grid size side")
infectionProbabilityLabel = ttk.Label(content, text = "Infection probability")
initialInfectedLabel = ttk.Label(content, text = "Initial Infected")
initialImmuneLabel = ttk.Label(content, text = "Initial Immune")
initialVirusCountLabel = ttk.Label(content, text = "Initial virus count")
initialPlasmaCountLabel = ttk.Label(content, text = "Initial plasma count")
initialMcellCountLabel = ttk.Label(content, text = "Initial mcell count")
totalVaccineDosesLabel = ttk.Label(content, text = "Total vaccine doses per CT")
vaccineEfficacyLabel = ttk.Label(content, text = "Vaccine efficacy")
vaccineTimeDelayLabel = ttk.Label(content, text = "Vaccine time delay")

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
modelTimeChangerLabel = ttk.Label(content, text = "Model time changer")
symptomTwoLabel = ttk.Label(content, text = "Symptom 2")
symptomThreeLabel = ttk.Label(content, text = "Symptom 3")
symptomFourLabel = ttk.Label(content, text = "Symptom 4")
multipleRunsLabel = ttk.Label(content, text = "How many runs")
filenameLabel = ttk.Label(content, text = "Name of simulation")

simulationTimeEntry = ttk.Entry(content, width = 8)
calculationTimerEntry = ttk.Entry(content, width = 8)
populationSizeEntry = ttk.Entry(content, width = 8)
gridSizeSideEntry = ttk.Entry(content, width = 8)
infectionProbabilityEntry = ttk.Entry(content, width = 8)
initialInfectedEntry = ttk.Entry(content, width = 8)
initialImmuneEntry = ttk.Entry(content, width = 8)
initialVirusCountEntry = ttk.Entry(content, width = 8)
initialPlasmaCountEntry = ttk.Entry(content, width = 8)
initialMcellCountEntry = ttk.Entry(content, width = 8)
totalVaccineDosesEntry = ttk.Entry(content, width = 8)
vaccineEfficacyEntry = ttk.Entry(content, width = 8)
vaccineTimeDelayEntry = ttk.Entry(content, width = 8)
multipleRunsEntry = ttk.Entry(content, width = 8)


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
symptomTwoEntry = ttk.Entry(content, width = 8)
symptomThreeEntry = ttk.Entry(content, width = 8)
symptomFourEntry = ttk.Entry(content, width = 8)
filenameEntry = ttk.Entry(content, width = 20)

plotOn = BooleanVar(value=1)
plotOnCheck = ttk.Checkbutton(content, text = "Agent condition plot", variable = plotOn)
vaccinationOn = BooleanVar(value = 0)
vaccinationCheck = ttk.Checkbutton(content, text = "Vaccination", variable = vaccinationOn)
diseaseModifyingOn = BooleanVar(value = 0)
diseaseModifyingCheck = ttk.Checkbutton(content, text = "Disease modifying", variable = diseaseModifyingOn)
preventiveVaccineOn = BooleanVar(value = 0)
preventiveVaccineCheck = ttk.Checkbutton(content, text = "Preventive", variable = preventiveVaccineOn)
virusMeanOn = BooleanVar(value = 0)
virusMeanCheck =  ttk.Checkbutton(content, text = "Virus mean plot", variable = virusMeanOn)
symptomPlotOn = BooleanVar(value = 0)
symptomPlotCheck = ttk.Checkbutton(content, text = "Symptom plot", variable = symptomPlotOn)
breakOn = BooleanVar(value = 0)
breakOnCheck = ttk.Checkbutton(content, text = "Break early", variable = breakOn)
value_check = IntVar()
disableCheck = ttk.Checkbutton(content, variable=value_check, text='Activate multiple runs',
                              command=activate_enable_button)
saveOn = BooleanVar(value = 0)
saveOnCheck = ttk.Checkbutton(content, variable = saveOn, text = "Save run")


# Insert default value
simulationTimeEntry.insert(0,1000)
calculationTimerEntry.insert(0,100)
populationSizeEntry.insert(0,5000)
gridSizeSideEntry.insert(0,35)
infectionProbabilityEntry.insert(0,0.02)
initialInfectedEntry.insert(0,50)
initialImmuneEntry.insert(0,0)
initialVirusCountEntry.insert(0,100)
initialPlasmaCountEntry.insert(0,0)
initialMcellCountEntry.insert(0,10)
totalVaccineDosesEntry.insert(0,5)
vaccineEfficacyEntry.insert(0,1)
vaccineTimeDelayEntry.insert(0, 0)

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
symptomTwoEntry.insert(0,100000)
symptomThreeEntry.insert(0,1000000)
symptomFourEntry.insert(0,10000000)


# Grid
content.grid(row=0, column = 0, sticky=(N, S, E, W))
runButton.grid(row = 0, column = 0)
runInitialImmuneSystemButton.grid(row = 0, column = 4)

rowIndex = 1
parametersLabel.grid(row = rowIndex, column = 0)
immuneParametersLabel.grid(row = rowIndex, column = 2)
lowerParameterLabel.grid(row = rowIndex, column = 3)
upperParameterLabel.grid(row = rowIndex, column = 4)

rowIndex += 1
simulationTimeLabel.grid(row = rowIndex, column = 0)
simulationTimeEntry.grid(row = rowIndex, column = 1)
aLabel.grid(row = rowIndex, column = 2)
aLowerEntry.grid(row = rowIndex, column = 3)
aUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
calculationTimerLabel.grid(row = rowIndex, column = 0)
calculationTimerEntry.grid(row = rowIndex, column = 1)

bLabel.grid(row = rowIndex, column = 2)
bLowerEntry.grid(row = rowIndex, column = 3)
bUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
populationSizeLabel.grid(row = rowIndex, column = 0)
populationSizeEntry.grid(row = rowIndex, column = 1)
cLabel.grid(row = rowIndex, column = 2)
cLowerEntry.grid(row = rowIndex, column = 3)
cUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
gridSizeSideLabel.grid(row = rowIndex, column = 0)
gridSizeSideEntry.grid(row = rowIndex, column = 1)
dLabel.grid(row = rowIndex, column = 2)
dLowerEntry.grid(row = rowIndex, column = 3)
dUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
infectionProbabilityLabel.grid(row = rowIndex, column = 0)
infectionProbabilityEntry.grid(row = rowIndex, column = 1)
eLabel.grid(row = rowIndex, column = 2)
eLowerEntry.grid(row = rowIndex, column = 3)
eUpperEntry.grid(row = rowIndex, column = 4)



rowIndex += 1
initialInfectedLabel.grid(row = rowIndex, column = 0)
initialInfectedEntry.grid(row = rowIndex, column = 1)
fLabel.grid(row = rowIndex, column = 2)
fLowerEntry.grid(row = rowIndex, column = 3)
fUpperEntry.grid(row = rowIndex, column = 4)

rowIndex += 1
initialImmuneLabel.grid(row = rowIndex, column = 0)
initialImmuneEntry.grid(row = rowIndex, column = 1)
gLabel.grid(row = rowIndex, column = 2)
gLowerEntry.grid(row = rowIndex, column = 3)
gUpperEntry.grid(row = rowIndex, column = 4)


rowIndex += 1
initialVirusCountLabel.grid(row = rowIndex, column = 0)
initialVirusCountEntry.grid(row = rowIndex, column = 1)
modelTimeTotalLabel.grid(row = rowIndex, column = 2)
modelTimeTotalEntry.grid(row = rowIndex, column = 3)


rowIndex += 1
initialPlasmaCountLabel.grid(row = rowIndex, column = 0)
initialPlasmaCountEntry.grid(row = rowIndex, column = 1)
modelTimeChangerLabel.grid(row = rowIndex, column = 2)
modelTimeChangerEntry.grid(row = rowIndex, column = 3)

rowIndex += 1
initialMcellCountLabel.grid(row = rowIndex, column = 0)
initialMcellCountEntry.grid(row = rowIndex, column = 1)
symptomTwoLabel.grid(row = rowIndex, column = 2)
symptomTwoEntry.grid(row = rowIndex, column = 3)



rowIndex += 1
totalVaccineDosesLabel.grid(row = rowIndex, column = 0)
totalVaccineDosesEntry.grid(row = rowIndex, column = 1)
symptomThreeLabel.grid(row = rowIndex, column = 2)
symptomThreeEntry.grid(row = rowIndex, column = 3)

rowIndex += 1
vaccineEfficacyLabel.grid(row = rowIndex, column = 0)
vaccineEfficacyEntry.grid(row = rowIndex, column = 1)
symptomFourLabel.grid(row = rowIndex, column = 2)
symptomFourEntry.grid(row = rowIndex, column = 3)

rowIndex += 1
vaccineTimeDelayLabel.grid(row = rowIndex, column = 0)
vaccineTimeDelayEntry.grid (row = rowIndex, column = 1)

rowIndex += 1
checkboxLabel.grid(row = rowIndex, column = 0)

rowIndex += 1
plotOnCheck.grid(row = rowIndex, column = 0, sticky = W)

rowIndex += 1
vaccinationCheck.grid(row = rowIndex, column = 0, sticky = W)

rowIndex += 1
diseaseModifyingCheck.grid(row = rowIndex, column = 0, sticky = W)
preventiveVaccineCheck.grid(row = rowIndex, column = 1, sticky = W)


rowIndex += 1
virusMeanCheck.grid(row = rowIndex, column = 0, sticky = W)

rowIndex += 1
symptomPlotCheck.grid(row = rowIndex, column = 0, sticky = W)

rowIndex += 1
breakOnCheck.grid(row= rowIndex, column = 0, sticky = W)


rowIndex += 1
disableCheck.grid(row = rowIndex, column = 0, sticky = W)
multipleRunsButton.grid(row = rowIndex, column = 1)

rowIndex += 1
saveOnCheck.grid(row = rowIndex, column = 0, sticky = W)
filenameLabel.grid(row = rowIndex, column = 1)
filenameEntry.grid(row = rowIndex, column = 2, columnspan = 2)


rowIndex += 1
multipleRunsLabel.grid(row = rowIndex, column = 1)
multipleRunsEntry.grid(row = rowIndex, column = 2)

# Keybindings
root.bind('<Return>', lambda e: runInitialImmuneSystemButton.invoke())
runInitialImmuneSystemButton.invoke()

root.mainloop()
