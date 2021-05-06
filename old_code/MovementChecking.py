# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 10:50:10 2021

@author: kevin
"""
import numpy as np
import time
import matplotlib.pyplot as plt

for timerDuration in [10,20,30,50,100,200]:
    populationSize = 100000
    gridSize = 100
    plotOn = False
    
    agentPosition = np.ones([populationSize,2])
    agentSpeed = np.ones(populationSize)
    agentRotation = np.ones(populationSize) 
    
    
    for ix in range(populationSize):
        agentPosition[ix][0] = np.random.uniform(0,gridSize)
        agentPosition[ix][1] = np.random.uniform(0,gridSize)
        agentSpeed[ix] = 0.05
        agentRotation[ix] = np.random.uniform(-np.pi,np.pi)
    
    
    
    originPosition = agentPosition.copy()
    
    for timeTicker in range(timerDuration):
        agentMovement = np.transpose([np.cos(agentRotation), np.sin(agentRotation)]*agentSpeed)
        agentPosition = agentPosition + agentMovement
        
        # Restrict movement
        #agentPosition = np.where(agentPosition<gridSize,agentPosition,0.1)
        #agentPosition = np.where(agentPosition>0, agentPosition, gridSize-0.1)
        
        # Change the rotation
        agentRotation = np.random.uniform(agentRotation - np.pi/4,
                                          agentRotation + np.pi/4)
    
    x = originPosition[:,0] - agentPosition[:,0]
    y = originPosition[:,1] - agentPosition[:,1]
    norm = np.sqrt(np.power(x,2)+np.power(y,2))
    plt.hist(norm, alpha = 0.2)
    plt.legend([10,20,30,50,100,200])
    

if plotOn == True:
    plt.scatter(originPosition[:,0],originPosition[:,1], c = np.linspace(0,1,populationSize))
    plt.scatter(agentPosition[:,0],agentPosition[:,1], c = np.linspace(0,1,populationSize))
    for ix in range(populationSize):
        plt.plot([originPosition[ix,0], agentPosition[ix,0]],[originPosition[ix,1], agentPosition[ix,1]])