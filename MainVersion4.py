# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 10:33:35 2021

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
    

def main():
    Parameters()
    print(dir(Parameters()))


if __name__ == "__main__":
    # Create the base root and parent
    root = Tk()
    content = ttk.Frame(root, padding=(3,3,12,12))
    
    runButton = ttk.Button(content, text = "Run", command = main)
    
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
    simulationTimeEntry = ttk.Entry(content, width = 8)
    calculationTimerEntry = ttk.Entry(content, width = 8)
    
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
    simulationTimeEntry.insert(0,500000)
    calculationTimerEntry.insert(0,100)
    
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
    
    rowIndex = 10
    calculationTimerLabel.grid(row = rowIndex, column = 0)
    calculationTimerEntry.grid(row = rowIndex, column = 1)
    
    
    # Keybindings
    root.bind('<Return>', lambda e: runButton.invoke())
    
    root.mainloop()
