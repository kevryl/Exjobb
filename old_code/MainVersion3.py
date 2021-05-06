# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 16:18:43 2021

@author: kevin
"""


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkinter import *
from tkinter import ttk

from scipy.integrate import odeint

import time


def Parameters():
    Parameters.simulationEndTime = int(simulationEndTimeEntry.get())
    Parameters.cycleTime = int(cycleTimeEntry.get())
    Parameters.populationSize = int(populationSizeEntry.get())
    Parameters.gridSize = int(gridSizeEntry.get())
    Parameters.infectionRate = float(infectionRateEntry.get())
    Parameters.diseaseDuration = int(diseaseDurationEntry.get())
    Parameters.incubationDuration = int(incubationDurationEntry.get())
    Parameters.initalInfected = int(initialInfectedEntry.get())
    Parameters.immuneDuration = int(immuneDurationEntry.get())
    Parameters.vaccineProcent = float(vaccineProcentEntry.get())
    Parameters.vaccineDoses = int(np.ceil(Parameters.vaccineProcent*Parameters.populationSize))
    
    Parameters.aMean = float(aMeanEntry.get())
    Parameters.bMean = float(bMeanEntry.get())
    Parameters.dMean = float(dMeanEntry.get())
    Parameters.aVariance = float(aVarianceEntry.get())
    Parameters.bVariance = float(bVarianceEntry.get())
    Parameters.dVariance = float(dVarianceEntry.get())
    
    Parameters.aMeanVaccine = float(aMeanVaccineEntry.get())
    Parameters.bMeanVaccine = float(bMeanVaccineEntry.get())
    Parameters.dMeanVaccine = float(dMeanVaccineEntry.get())
    Parameters.aVarianceVaccine = float(aVarianceVaccineEntry.get())
    Parameters.bVarianceVaccine = float(bVarianceVaccineEntry.get())
    Parameters.dVarianceVaccine = float(dVarianceVaccineEntry.get())
    

def PlotInitialImmuneSystem():
    Parameters()
    aMean = Parameters.aMean
    aVariance = Parameters.aVariance
    bMean = Parameters.bMean
    bVariance = Parameters.bVariance
    dMean = Parameters.dMean
    dVariance = Parameters.dVariance
    figure = Figure(figsize=(5, 4), dpi=70)
    plot = figure.add_subplot(1, 1, 1)
    plot.set_xlabel("Timecycle")
    plot.set_ylabel("Virus load")
    for a,b,d in [[aMean ,bMean ,dMean],[aMean+2*aVariance,bMean-2*bVariance,dMean+2*dVariance],[aMean-2*aVariance,bMean+2*bVariance,dMean-2*dVariance]]:
        # initial condition
        z0 = [0,0]
        # time points
        t = np.linspace(0,Parameters.diseaseDuration,Parameters.diseaseDuration+1)
        # step input
        u = np.zeros(Parameters.diseaseDuration)
        # change to 2.0 at time = 5.0
        u[0:] = 1.0
        u[Parameters.incubationDuration:] = 0
        # store solution
        x = np.empty_like(t)
        y = np.empty_like(t)
        # record initial conditions
        x[0] = z0[0]
        y[0] = z0[1]
        # solve ODE
        for i in range(1,Parameters.diseaseDuration):
            # span for next time step
            tspan = [t[i-1],t[i]]
            # solve for next step
            z = odeint(model,z0,tspan,args=(u[i],a,b,d,Parameters.incubationDuration))
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
        y[-1] = 0
        plot.axis([0,Parameters.diseaseDuration,0,1])
        if a == aMean:
            plot.plot(t, x, color="red", linestyle="-", label = "infected")
        else:
            plot.plot(t, x, color="red", linestyle="--")
        
    aMean = Parameters.aMeanVaccine
    aVariance = Parameters.aVarianceVaccine
    bMean = Parameters.bMeanVaccine
    bVariance = Parameters.bVarianceVaccine
    dMean = Parameters.dMeanVaccine
    dVariance = Parameters.dVarianceVaccine
    for a,b,d in [[aMean ,bMean ,dMean],[aMean+2*aVariance,bMean-2*bVariance,dMean+2*dVariance],[aMean-2*aVariance,bMean+2*bVariance,dMean-2*dVariance]]:
        # initial condition
        z0 = [0,0]
        # time points
        t = np.linspace(0,Parameters.diseaseDuration,Parameters.diseaseDuration+1)
        # step input
        u = np.zeros(Parameters.diseaseDuration)
        # change to 2.0 at time = 5.0
        u[0:] = 1.0
        u[Parameters.incubationDuration:] = 0
        # store solution
        x = np.empty_like(t)
        y = np.empty_like(t)
        # record initial conditions
        x[0] = z0[0]
        y[0] = z0[1]
        # solve ODE
        for i in range(1,Parameters.diseaseDuration):
            # span for next time step
            tspan = [t[i-1],t[i]]
            # solve for next step
            z = odeint(model,z0,tspan,args=(u[i],a,b,d,Parameters.incubationDuration))
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
        y[-1] = 0
        plot.axis([0,Parameters.diseaseDuration,0,1])
        if a == aMean:
            plot.plot(t, x, color="orange", linestyle="-", label = "Vaccinated")
        else:
            plot.plot(t, x, color="orange", linestyle="--")
    plot.legend()
    canvas = FigureCanvasTkAgg(figure, content)
    canvas.get_tk_widget().grid(row = 1, column = 8,columnspan = 4, rowspan = 10, padx = 10, pady = 10)


def CreatePopulation():
    agentPosition = np.ones([Parameters.populationSize,2])
    agentSpeed = np.ones(Parameters.populationSize)
    agentRotation = np.ones(Parameters.populationSize) 
    agentTimer = np.zeros(Parameters.populationSize).astype(int)
    agentTimer = agentTimer.tolist()
    agentTimerSuseptble =  np.zeros(Parameters.populationSize).astype(int)
    agentTimerSuseptble = agentTimerSuseptble.tolist()
    agentStatus = []
    infectedList = []
    immunityList = []
    for ix in range(Parameters.populationSize):
        agentPosition[ix][0] = np.random.uniform(0,Parameters.gridSize)
        agentPosition[ix][1] = np.random.uniform(0,Parameters.gridSize)
        agentSpeed[ix] = 0.2
        agentRotation[ix] = np.random.uniform(-np.pi,np.pi)
    for ix in range(Parameters.populationSize):
        if ix < 10:
            agentStatus.append("infected")
            infectedList.append(ix)
        else:
            agentStatus.append("susepteble")
    return agentPosition, agentSpeed, agentRotation, agentTimer, agentTimerSuseptble, agentStatus, infectedList, immunityList

    
def CreateDemografi():
    Parameters()
    demografi = []
    for ix in range(Parameters.populationSize):
        r = np.random.rand()
        if r < 0.1771:
            demografi.append(np.random.randint(0,14))
        elif 0.1771 < r < 0.2851: 
            demografi.append(np.random.randint(15,24))
        elif 0.2851 < r < 0.6752:
            demografi.append(np.random.randint(25,54))
        elif 0.6752 < r < 0.7942:
            demografi.append(np.random.randint(55,64))
        elif 0.7942 < r:
            demografi.append(np.random.randint(65,100))
    return demografi
    
    
def model(z,t,u,a,b,d,incubationDuration):
    if a < 0: a = 1e-6
    if b < 0: b = 1e-6
    if d < 0: d = 1e-6
    
    x = z[0]
    y = z[1]
    if t < incubationDuration-1:
        dxdt = (-x + u - y)/a
        dydt = (-y + x)/d
    else: 
        dxdt = (-x + u - y)/b
        dydt = (-y + x)/d
    dzdt = [dxdt,dydt]
    return dzdt


def immuneSystem(aMean, aVariance, bMean, bVariance, dMean, dVariance):
    Parameters()
    virus = []
    antibody = []
    # time points
    t = np.linspace(0,Parameters.diseaseDuration,Parameters.diseaseDuration+1)
    # step input
    u = np.zeros(Parameters.diseaseDuration)
    # change to 2.0 at time = 5.0
    u[0:] = 1.0
    u[Parameters.incubationDuration:] = 0
    for ix in range(Parameters.populationSize):
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
        for i in range(1,Parameters.diseaseDuration):
            # span for next time step
            tspan = [t[i-1],t[i]]
            # solve for next step
            z = odeint(model,z0,tspan,args=(u[i],a,b,d,Parameters.incubationDuration))
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
        virus.append(x)
        antibody.append(y)
    return virus, antibody


def AgentRecover(agentStatus,agentTimer,infectedList, agentVirus, immunityList):
    indexRemove = []
    for count, infectedAgentIndex in enumerate(infectedList):
        agentTimer[infectedAgentIndex] = agentTimer[infectedAgentIndex] + 1
        agentTimestep = agentTimer[infectedAgentIndex]
        if agentVirus[infectedAgentIndex][agentTimestep] < 1e-5:
            indexRemove.append(count)
            if agentStatus[infectedAgentIndex] == 'vaccinated, infected':
                agentStatus[infectedAgentIndex] = 'vaccinated'
            elif agentStatus[infectedAgentIndex] == 'infected':
                agentStatus[infectedAgentIndex]  = 'immune'
                immunityList.append(infectedAgentIndex)
            agentTimer[infectedAgentIndex] = 0
    infectedList = np.delete(infectedList,indexRemove).astype(int)
    infectedList = infectedList.tolist()
    return agentStatus, agentTimer, infectedList, immunityList


def AgentSusepteble(agentStatus, agentTimerSuseptble, immunityList):
    Parameters()
    indexRemove = []
    for count, recoveredAgentIndex in enumerate(immunityList):
        agentTimerSuseptble[recoveredAgentIndex] = agentTimerSuseptble[recoveredAgentIndex] + 1
        if agentTimerSuseptble[recoveredAgentIndex] == Parameters.immuneDuration:
            if agentStatus[recoveredAgentIndex] == 'immune':
                indexRemove.append(count)
                agentStatus[recoveredAgentIndex] = 'susepteble'
                agentTimerSuseptble[recoveredAgentIndex] = 0
                
            elif agentStatus[recoveredAgentIndex] == 'vaccinated, immune':
                indexRemove.append(count)
                agentStatus[recoveredAgentIndex] = 'vaccinated'
                agentTimerSuseptble[recoveredAgentIndex] = 0
    immunityList = np.delete(immunityList, indexRemove).astype(int)
    immunityList = immunityList.tolist()
    return agentStatus, agentTimerSuseptble, immunityList


def AgentDeathDemografi(infectedList, agentStatus, agentVirus, agentVirusVaccine, agentSpeed, agentTimer, demografi):
    indexRemove = []
    for count, infectedAgentIndex in enumerate(infectedList):
        r = np.random.rand()
        if agentStatus[infectedAgentIndex] == 'infected':
            deathChance = agentVirus[infectedAgentIndex][agentTimer[infectedAgentIndex]]*demografi[infectedAgentIndex]/10000
            if r < deathChance:
                indexRemove.append(count)
                agentSpeed[infectedAgentIndex] = 0
                agentTimer[infectedAgentIndex] = 0
                agentStatus[infectedAgentIndex] = 'dead'
        elif agentStatus[infectedAgentIndex] =='vaccinated, infected':
            deathChance = agentVirusVaccine[infectedAgentIndex][agentTimer[infectedAgentIndex]]*demografi[infectedAgentIndex]/10000
            if r < deathChance:
                    indexRemove.append(count)
                    agentSpeed[infectedAgentIndex] = 0
                    agentTimer[infectedAgentIndex] = 0
                    agentStatus[infectedAgentIndex] = 'dead'
    infectedList = np.delete(infectedList,indexRemove).astype(int)
    infectedList = infectedList.tolist()
    return infectedList, agentStatus, agentSpeed, agentTimer


def AgentDeath(infectedList, agentStatus, agentVirus, agentVirusVaccine, agentSpeed, agentTimer):
    indexRemove = []
    for count, infectedAgentIndex in enumerate(infectedList):
        r = np.random.rand()
        if agentStatus[infectedAgentIndex] == 'infected':
            if r < agentVirus[infectedAgentIndex][agentTimer[infectedAgentIndex]]/1000:
                indexRemove.append(count)
                agentSpeed[infectedAgentIndex] = 0
                agentTimer[infectedAgentIndex] = 0
                agentStatus[infectedAgentIndex] = 'dead'
        elif agentStatus[infectedAgentIndex] =='vaccinated, infected':
            if r < agentVirusVaccine[infectedAgentIndex][agentTimer[infectedAgentIndex]]/1000:
                    indexRemove.append(count)
                    agentSpeed[infectedAgentIndex] = 0
                    agentTimer[infectedAgentIndex] = 0
                    agentStatus[infectedAgentIndex] = 'dead'
    infectedList = np.delete(infectedList,indexRemove).astype(int)
    infectedList = infectedList.tolist()
    return infectedList, agentStatus, agentSpeed, agentTimer


def CreateGridStructure(gridSize):
    gridStructure = []
    for ix in range(gridSize):
        gridStructure.append([])
        for jx in range(gridSize):
            gridStructure[ix].append([]) 
    return gridStructure


def DiseaseSpreding(agentStatus, agentTimer, infectedList, gridStructure, agentVirus, agentVirusVaccine):
    Parameters()
    for ix in range(len(gridStructure)):
        for jx in range(len(gridStructure)):
            if gridStructure[ix][jx] != [] and len(gridStructure[ix][jx]) != 1:
                localInfected = []
                localSusepteble = []
                localVaccinated = []
                localInfectedVaccinated = []
                for agentIndex in gridStructure[ix][jx]:
                    if agentStatus[agentIndex] == 'infected':
                        localInfected.append(agentIndex)
                    if agentStatus[agentIndex] == 'susepteble':
                        localSusepteble.append(agentIndex)
                    if agentStatus[agentIndex] == 'vaccinated':
                        localVaccinated.append(agentIndex)
                    if agentStatus[agentIndex] == 'vaccinated, infected':
                        localInfectedVaccinated.append(agentIndex)
                
                # SUSEBTEBLE
                for suseptebleAgentIndex in localSusepteble:
                    for infectedAgentIndex in localInfected:
                        r = np.random.rand()
                        infectedTimeStep = agentTimer[infectedAgentIndex]
                        virusRate = agentVirus[infectedAgentIndex][infectedTimeStep]
                        infection = Parameters.infectionRate*virusRate
                        meeting = 1-virusRate
                        if r < infection*meeting:
                            agentStatus[suseptebleAgentIndex] = 'infected'
                            infectedList.append(suseptebleAgentIndex)
                            break
                        
                    for infectedVaccinatedAgentIndex in localInfectedVaccinated:
                        r = np.random.rand()
                        infectedTimeStep = agentTimer[infectedVaccinatedAgentIndex]
                        virusRateVaccine = agentVirusVaccine[infectedVaccinatedAgentIndex][infectedTimeStep]
                        infection = Parameters.infectionRate*virusRateVaccine
                        meeting = 1-virusRateVaccine
                        if r < infection*meeting:
                            agentStatus[suseptebleAgentIndex] = 'infected'
                            infectedList.append(suseptebleAgentIndex)
                            break
                # VACCINATED
                for vaccinatedAgentIndex in localVaccinated:
                    for infectedAgentIndex in localInfected:
                        r = np.random.rand()
                        infectedTimeStep = agentTimer[infectedAgentIndex]
                        virusRate = agentVirus[infectedAgentIndex][infectedTimeStep]
                        infection = Parameters.infectionRate*virusRate
                        meeting = 1-virusRate
                        if r < infection*meeting:
                            agentStatus[vaccinatedAgentIndex] = 'vaccinated, infected'
                            infectedList.append(vaccinatedAgentIndex)
                            break
                    for infectedVaccinatedAgentIndex in localInfectedVaccinated:
                        r = np.random.rand()
                        infectedTimeStep = agentTimer[infectedVaccinatedAgentIndex]
                        virusRateVaccine = agentVirusVaccine[infectedVaccinatedAgentIndex][infectedTimeStep]
                        infection = Parameters.infectionRate * virusRateVaccine
                        meeting = 1 - virusRateVaccine
                        if r < infection*meeting:
                            agentStatus[vaccinatedAgentIndex] = 'vaccinated, infected'
                            infectedList.append(vaccinatedAgentIndex)
                            break
                
    return agentStatus, agentTimer, infectedList


def main():
    print(" ")
    print("Run started")
    startTime = time.time()
    setupTime = time.time()
    Parameters()
    agentPosition, agentSpeed, agentRotation, agentTimer, agentTimerSuseptble, agentStatus, infectedList, immunityList = CreatePopulation()

    agentVirus, agentAntibody = immuneSystem(Parameters.aMean, 
                                             Parameters.aVariance, 
                                             Parameters.bMean, 
                                             Parameters.bVariance, 
                                             Parameters.dMean, 
                                             Parameters.dVariance)
    agentVirusVaccine, agentAntibodyVaccine = immuneSystem(Parameters.aMeanVaccine, 
                                                           Parameters.aVarianceVaccine, 
                                                       Parameters.bMeanVaccine, 
                                                       Parameters.bVarianceVaccine, 
                                                       Parameters.dMeanVaccine, 
                                                       Parameters.dVarianceVaccine)

    populationPlot = [[],[],[],[],[]]
    maxInfected = 0
    
    if demografiOn.get() == True:
        demografi = CreateDemografi()
    
    
    executionTime = (time.time() - setupTime)
    print('Set up execution time in seconds: ' + str(executionTime))
    simulationTime = time.time()
    for timeTicker in range(Parameters.simulationEndTime):
        agentMovement = np.transpose([np.cos(agentRotation), 
                                      np.sin(agentRotation)]*agentSpeed)
        agentPosition = agentPosition + agentMovement
        
        # Restrict movement
        agentPosition = np.where(agentPosition<Parameters.gridSize,
                                 agentPosition,
                                 0.1)
        agentPosition = np.where(agentPosition>0, 
                                 agentPosition, 
                                 Parameters.gridSize-0.1)
        
        # Change the rotation
        agentRotation = np.random.uniform(agentRotation - np.pi/4,
                                          agentRotation + np.pi/4)
        if timeTicker % Parameters.cycleTime == 0 and timeTicker != 0:
            agentStatus, agentTimer, infectedList, immunityList = AgentRecover(agentStatus, 
                                                                               agentTimer, 
                                                                               infectedList, 
                                                                               agentVirus, 
                                                                               immunityList)
            
            agentStatus, agentTimerSuseptble, immunityList =  AgentSusepteble(agentStatus, 
                                                                              agentTimerSuseptble, 
                                                                              immunityList)
    
            gridStructure = CreateGridStructure(Parameters.gridSize)
            flooredAgentPosition = np.floor(agentPosition)
            for ix in range(Parameters.populationSize):
                rowIndex = flooredAgentPosition[ix][0].astype('int')
                columnIndex = flooredAgentPosition[ix][1].astype('int')
                gridStructure[rowIndex][columnIndex].append(ix)
            
            agentStatus, agentTimer, infectedList = DiseaseSpreding(agentStatus, 
                                                                    agentTimer, 
                                                                    infectedList, 
                                                                    gridStructure, 
                                                                    agentVirus, 
                                                                    agentVirusVaccine)

            if deathOn.get() == True:
                if demografiOn.get() == True:
                    infectedList, agentStatus, agentSpeed, agentTimer = AgentDeathDemografi(infectedList, 
                                                                                            agentStatus, 
                                                                                            agentVirus, 
                                                                                            agentVirusVaccine, 
                                                                                            agentSpeed, 
                                                                                            agentTimer, 
                                                                                            demografi)
                else: 
                    infectedList, agentStatus, agentSpeed, agentTimer = AgentDeath(infectedList, 
                                                                                   agentStatus, 
                                                                                   agentVirus, 
                                                                                   agentVirusVaccine, 
                                                                                   agentSpeed, 
                                                                                   agentTimer)
                
            if vaccinationOn.get() == True:
                distributedVaccine = 0
                for ix in range(Parameters.populationSize):
                    if agentStatus[ix] == 'susepteble':
                        agentStatus[ix] = 'vaccinated'
                        distributedVaccine = distributedVaccine + 1
                    elif agentStatus[ix] == 'immune':
                        agentStatus[ix] = 'vaccinated, immune'
                        distributedVaccine = distributedVaccine + 1
                    if distributedVaccine == Parameters.vaccineDoses:
                        break
                
            totalSusepteble = 0
            totalInfected = 0
            totalRecovered = 0
            totalDead = 0
            totalVaccinated = 0
            for ix in range(Parameters.populationSize):
                if agentStatus[ix] == 'susepteble':
                    totalSusepteble = totalSusepteble + 1
                elif any([agentStatus[ix] == 'infected', agentStatus[ix] == 'vaccinated, infected']):
                    totalInfected = totalInfected + 1
                    if maxInfected < totalInfected:
                        maxInfected = totalInfected
                elif agentStatus[ix] == 'immune':
                    totalRecovered = totalRecovered + 1
                elif agentStatus[ix] == 'dead': 
                    totalDead = totalDead + 1
                else:
                    totalVaccinated = totalVaccinated + 1
            populationPlot[0].append(totalSusepteble)
            populationPlot[1].append(totalInfected)
            populationPlot[2].append(totalRecovered)
            populationPlot[3].append(totalDead)
            populationPlot[4].append(totalVaccinated)
            
            if totalInfected == 0:
                break
            
            
    if plotOn.get() == True:
        plotLength = range(len(populationPlot[0]))
        plt.figure()
        plt.plot(plotLength, populationPlot[0], 'g', plotLength, populationPlot[1], 'r',
                 plotLength, populationPlot[2], 'b', plotLength, populationPlot[4], 'orange')
        plt.xlabel('Timecycles')
        plt.ylabel('Number of agents')
        plt.legend(['susepteble', 'infected', 'immune','vaccinated'])
        plt.show()
    
    executionTime = (time.time() - simulationTime)
    print('Simulation execution time in seconds: ' + str(executionTime))
    
    executionTime = (time.time() - startTime)
    print('Total execution time in seconds: ' + str(executionTime))

    print('Share susepteble left ', populationPlot[0][-1]/Parameters.populationSize)
    print('Share recovered left ', populationPlot[2][-1]/Parameters.populationSize)
    print('Share dead left ', populationPlot[3][-1]/Parameters.populationSize)
    print('Share vaccinated left', populationPlot[4][-1]/Parameters.populationSize)
    print('Peak infected share', maxInfected/Parameters.populationSize)
    print(' ')
    

# Create the base root and parent
root = Tk()
content = ttk.Frame(root, padding=(3,3,12,12))

runButton = ttk.Button(content, text = "Run", command = main)
PlotInitialImmuneSystem = ttk.Button(content, text = "Update immune system", command = PlotInitialImmuneSystem)

parametersLabel = ttk.Label(content, text = "Parameters")
simulationEndTimeLabel = ttk.Label(content, text = "Simulation duration")
cycleTimeLabel = ttk.Label(content, text = "Calculation interval")
populationSizeLabel = ttk.Label(content, text = "Population size")
gridSizeLabel = ttk.Label(content,text = "Grid size")
infectionRateLabel = ttk.Label(content, text = "Infection rate")
diseaseDurationLabel = ttk.Label(content, text = "Disease duration")
incubationDurationLabel = ttk.Label(content, text = "Incubation period")
initialInfectedLabel = ttk.Label(content, text = "Inital infected")
immuneDurationLabel = ttk.Label(content, text = "Immune duration")
vaccineProcentLabel = ttk.Label(content, text = "Vaccine procent of population/CT")


infectedImmuneLabel = ttk.Label(content, text = "Infected immune response")
aMeanLabel = ttk.Label(content, text = "a mean")
bMeanLabel = ttk.Label(content, text = "b mean")
dMeanLabel = ttk.Label(content, text = "d mean")
aMeanVaccineLabel = ttk.Label(content, text = "a mean")
bMeanVaccineLabel = ttk.Label(content, text = "b mean")
dMeanVaccineLabel = ttk.Label(content, text = "d mean")


aVarianceLabel = ttk.Label(content, text = "a variance")
bVarianceLabel = ttk.Label(content, text = "b variance")
dVarianveLabel = ttk.Label(content, text = "d variance")
aVarianceVaccineLabel = ttk.Label(content, text = "a variance")
bVarianceVaccineLabel = ttk.Label(content, text = "b variance")
dVarianveVaccineLabel = ttk.Label(content, text = "d variance")


vaccineImmuneLabel = ttk.Label(content, text = "Vaccine immune response")


simulationEndTimeEntry = ttk.Entry(content, width = 8)
cycleTimeEntry = ttk.Entry(content, width = 8)
populationSizeEntry = ttk.Entry(content, width = 8)
gridSizeEntry = ttk.Entry(content, width = 8)
infectionRateEntry = ttk.Entry(content, width = 8)
diseaseDurationEntry = ttk.Entry(content, width = 8)
incubationDurationEntry = ttk.Entry(content,width = 8)
initialInfectedEntry = ttk.Entry(content,width = 8)
immuneDurationEntry = ttk.Entry(content,width = 8)
vaccineProcentEntry = ttk.Entry(content,width = 8)

aMeanEntry = ttk.Entry(content, width = 8)
bMeanEntry = ttk.Entry(content, width = 8)
dMeanEntry = ttk.Entry(content, width = 8)
aVarianceEntry = ttk.Entry(content, width = 8)
bVarianceEntry = ttk.Entry(content, width = 8)
dVarianceEntry = ttk.Entry(content, width = 8)

aMeanVaccineEntry = ttk.Entry(content, width = 8)
bMeanVaccineEntry = ttk.Entry(content, width = 8)
dMeanVaccineEntry = ttk.Entry(content, width = 8)
aVarianceVaccineEntry = ttk.Entry(content, width = 8)
bVarianceVaccineEntry = ttk.Entry(content, width = 8)
dVarianceVaccineEntry = ttk.Entry(content, width = 8)


plotOn = BooleanVar(value=1)
plotOnCheck = ttk.Checkbutton(content, text = "Plot on", variable = plotOn)
deathOn = BooleanVar(value=1)
deathOnCheck = ttk.Checkbutton(content, text = "Death on", variable = deathOn)
vaccinationOn = BooleanVar(value=1)
vaccinationOnCheck = ttk.Checkbutton(content, text = "Vaccination on", variable = vaccinationOn)
demografiOn = BooleanVar(value = 0)
demografiOnCheck = ttk.Checkbutton(content, text = "Demografi on", variable = demografiOn)


# Insert deafault value
simulationEndTimeEntry.insert(0,500000)
cycleTimeEntry.insert(0,100)
populationSizeEntry.insert(0,5000)
gridSizeEntry.insert(0,35)
infectionRateEntry.insert(0,0.1)
diseaseDurationEntry.insert(0, 100)
incubationDurationEntry.insert(0,20)
initialInfectedEntry.insert(0,50)
immuneDurationEntry.insert(0,100)
vaccineProcentEntry.insert(0,0.001)

aMeanEntry.insert(0, 25)
bMeanEntry.insert(0, 50)
dMeanEntry.insert(0, 10)
aVarianceEntry.insert(0, 5)
bVarianceEntry.insert(0, 5)
dVarianceEntry.insert(0, 2)

aMeanVaccineEntry.insert(0, 300)
bMeanVaccineEntry.insert(0, 25)
dMeanVaccineEntry.insert(0, 5)
aVarianceVaccineEntry.insert(0, 20)
bVarianceVaccineEntry.insert(0, 5)
dVarianceVaccineEntry.insert(0, 1)


# Place widgets into a grid
content.grid(row=0, column = 0, sticky=(N, S, E, W))
runButton.grid(row = 0, column = 0, columnspan = 2)
plotOnCheck.grid(row = 0, column = 3)


parametersLabel.grid(row=1,column=0,columnspan = 2)
infectedImmuneLabel.grid(row = 1, column = 4,columnspan = 4)

simulationEndTimeLabel.grid(row = 2, column = 0)
simulationEndTimeEntry.grid(row = 2, column = 1)
aMeanLabel.grid(row = 2, column = 4)
aMeanEntry.grid(row = 2, column = 5)
aVarianceLabel.grid(row = 2, column = 6)
aVarianceEntry.grid(row = 2, column = 7)

cycleTimeLabel.grid(row = 3, column = 0)
cycleTimeEntry.grid(row = 3, column = 1)
bMeanLabel.grid(row = 3, column = 4)
bMeanEntry.grid(row = 3, column = 5)
bVarianceLabel.grid(row = 3, column = 6)
bVarianceEntry.grid(row = 3, column = 7)

populationSizeLabel.grid(row = 4, column = 0)
populationSizeEntry.grid(row = 4, column = 1)
dMeanLabel.grid(row = 4, column = 4)
dMeanEntry.grid(row = 4, column = 5)
dVarianveLabel.grid(row = 4, column = 6)
dVarianceEntry.grid(row = 4, column = 7)

gridSizeLabel.grid(row = 5, column = 0)
gridSizeEntry.grid(row = 5, column = 1)
PlotInitialImmuneSystem.grid(row = 5, column = 4, columnspan = 2)

infectionRateLabel.grid(row = 6, column = 0)
infectionRateEntry.grid(row = 6, column = 1)
vaccineImmuneLabel.grid(row = 6, column = 4, columnspan = 4)

diseaseDurationLabel.grid(row = 7, column = 0)
diseaseDurationEntry.grid(row = 7, column = 1)
aMeanVaccineLabel.grid(row = 7, column = 4)
aMeanVaccineEntry.grid(row = 7, column = 5)
aVarianceVaccineLabel.grid(row = 7, column = 6)
aVarianceVaccineEntry.grid(row = 7, column = 7)

incubationDurationLabel.grid(row = 8, column = 0)
incubationDurationEntry.grid(row = 8, column = 1)
bMeanVaccineLabel.grid(row = 8, column = 4)
bMeanVaccineEntry.grid(row = 8, column = 5)
bVarianceVaccineLabel.grid(row = 8, column = 6)
bVarianceVaccineEntry.grid(row = 8, column = 7)

initialInfectedLabel.grid(row = 9, column = 0)
initialInfectedEntry.grid(row = 9, column = 1)
dMeanVaccineLabel.grid(row = 9, column = 4)
dMeanVaccineEntry.grid(row = 9, column = 5)
dVarianveVaccineLabel.grid(row = 9, column = 6)
dVarianceVaccineEntry.grid(row = 9, column = 7)

immuneDurationLabel.grid(row = 10, column = 0)
immuneDurationEntry.grid(row = 10, column = 1)

vaccineProcentLabel.grid(row = 11, column = 0)
vaccineProcentEntry.grid(row = 11, column = 1)

deathOnCheck.grid(row = 12, column = 0, sticky = W)

vaccinationOnCheck.grid(row = 13, column = 0, sticky = W)

demografiOnCheck.grid(row = 14, column = 0, sticky = W)

# Keybindings
root.bind('<Return>', lambda e: runButton.invoke())
PlotInitialImmuneSystem.invoke()

root.mainloop()
