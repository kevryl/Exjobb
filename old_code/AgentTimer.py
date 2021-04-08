# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 13:49:04 2021

@author: kevin
"""


agentTimer = [[],[]]
populationSize = 10000

for ix in range(populationSize):
    agentTimer[0].append(ix)
    agentTimer[1].append(np.random.randint(100,200))


for timer in range(200):
    agentTimer[1] = agentTimer[1] - np.ones(len(agentTimer[1]))
    indexRemove = []
    if timer == 100:
        np.append()
    for ix in range(len(agentTimer[1])):
        if agentTimer[1][ix] < 0:
            indexRemove.append(ix)  
    agentTimer = np.delete(agentTimer,indexRemove,1)
            
print(agentTimer)

