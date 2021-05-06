# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 16:24:10 2021

@author: kevin
"""


import numpy as np
import matplotlib.pyplot as plt
import time

py_clip = lambda x, l, u: u if x < l else l if x > u else x



pop_size = 1000
pop_test_position = np.ones([pop_size,2])
pop_test = [[],[],[]]

for ix in range(pop_size):
    pop_test_position[ix][0] = ix
    pop_test_position[ix][1] = ix
    pop_test[0].append('s')
    pop_test[1].append(np.random.uniform(-np.pi,np.pi))
    pop_test[2].append(2)
    
    
startTime = time.time()
'''
for time_ticker in range(1000):
    movement = [np.cos(pop_test[1])*pop_test[2], np.sin(pop_test[1])*pop_test[2]]
    pop_test_position = pop_test_position + np.transpose(movement)
    
    for ix in range(pop_size):
        pop_test_position[ix][0] = py_clip(pop_test_position[ix][0], 0, 100)
        pop_test_position[ix][1] = py_clip(pop_test_position[ix][1], 0, 100)
        pop_test[1][ix] = np.random.uniform(pop_test[1][ix] - np.pi/4, pop_test[1][ix] + np.pi/4)
    
    #plt.scatter(pop_test_position[:,0],pop_test_position[:,1])
    #plt.pause(0.05)
'''
for time_ticker in range(1000):
    movement = [np.cos(pop_test[1])*pop_test[2], np.sin(pop_test[1])*pop_test[2]]
    pop_test_position = pop_test_position + np.transpose(movement)
    
    pop_test_position = np.where(pop_test_position<100,pop_test_position,0)
    pop_test_position = np.where(pop_test_position<0,pop_test_position,100)
    
    for ix in range(pop_size):
        pop_test[1][ix] = np.random.uniform(pop_test[1][ix] - np.pi/4, pop_test[1][ix] + np.pi/4)
    
    #plt.scatter(pop_test_position[:,0],pop_test_position[:,1])
    #plt.pause(0.05)


executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
