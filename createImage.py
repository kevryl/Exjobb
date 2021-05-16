# -*- coding: utf-8 -*-
"""
Created on Sun May 16 09:23:49 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt

file = 'lowDensity10DMO'
populationSize = 5000

immune = np.load('data/'+file+'immune.npy')
infected = np.load('data/'+file+'infected.npy')
susceptible = np.load('data/'+file+'susepteble.npy')
symptomatic = np.load('data/'+file+'symptomatic.npy')

infectedError = np.std(infected,axis=0)
symptomaticError = np.std(symptomatic,axis=0)
immuneError = np.std(immune,axis=0)
susceptibleError = np.std(susceptible,axis=0)
infectedMean = np.mean(infected,axis = 0)
symptomaticMean = np.mean(symptomatic,axis = 0)
immuneMean = np.mean(immune,axis = 0)
susceptibleMean = np.mean(susceptible,axis = 0)
plotLength = np.linspace(0, len(infectedMean)*5,len(infectedMean))

for mean, error, color, text in [[infectedMean, infectedError, 'red', 'Infected'],\
                           [symptomaticMean, symptomaticError, 'orange', 'Symptomatic'],\
                               [immuneMean, immuneError, 'blue', 'Immune'],\
                            [susceptibleMean, susceptibleError, 'green', 'Susceptible']]:
    plt.plot(plotLength[:-1], mean[:-1], c = color, label = text)
    ciLower = mean - 2*error
    ciLowerBounded = np.where(ciLower>0,ciLower,0)
    ciUpper = mean + 2*error
    ciUpperBounded = np.where(ciUpper<populationSize,ciUpper, populationSize)
    plt.fill_between(plotLength[:-1], ciLowerBounded[:-1], ciUpperBounded[:-1], color = color, alpha = 0.3)

if np.argmax(infectedMean < 1) != 0:
    plt.arrow(np.argmax(infectedMean < 1)*5, 10, 0, 200) 
plt.legend()
plt.xlabel('Time cycle', fontsize = 15)
plt.ylabel('Agents', fontsize = 15)
plt.grid()
