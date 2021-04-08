# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 10:39:24 2021

@author: kevin
"""


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import time

# function that returns dz/dt
def model(z,t,u,a,b,d,incubationDuration):
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

startTime = time.time()
storeX = []
storeY = []

aMean = 300
aVariance = 20
bMean = 25
bVariance = 5
dMean = 5
dVariance = 1


incubationDuration = 20
diseaseDuration = 100

for a,b,d in [[aMean ,bMean ,dMean],[aMean+2*aVariance,bMean-2*bVariance,dMean+2*dVariance],[aMean-2*aVariance,bMean+2*bVariance,dMean-2*dVariance]]:
    # initial condition
    z0 = [0,0]
    # time points
    t = np.linspace(0,diseaseDuration,diseaseDuration+1)
    # step input
    u = np.zeros(diseaseDuration)
    # change to 2.0 at time = 5.0
    u[0:] = 1.0
    u[incubationDuration:] = 0


    # store solution
    x = np.empty_like(t)
    y = np.empty_like(t)
    # record initial conditions
    x[0] = z0[0]
    y[0] = z0[1]
    
    
    # solve ODE
    for i in range(1,diseaseDuration):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        z = odeint(model,z0,tspan,args=(u[i],a,b,d,incubationDuration))
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
    plt.plot(t,x,'k-')
    plt.plot(t,y,'g-')

plt.axis([0,diseaseDuration,0,1])
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

# %%
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


# function that returns dz/dt
def model(z,t,u,a,b,d,incubationDuration):
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

startTime = time.time()
storeX = []
storeY = []

aMean = 10
aVariance = 3
bMean = 25
bVariance = 5
dMean = 100
dVariance = 1


incubationDuration = 20
diseaseDuration = 100

for a,b,d in [[aMean ,bMean ,dMean],[aMean+2*aVariance,bMean-2*bVariance,dMean+2*dVariance],[aMean-2*aVariance,bMean+2*bVariance,dMean-2*dVariance]]:
    # initial condition
    z0 = [0,0]
    # time points
    t = np.linspace(0,diseaseDuration,diseaseDuration+1)
    # step input
    u = np.zeros(diseaseDuration)
    # change to 2.0 at time = 5.0
    u[0:] = 1.0
    u[incubationDuration:] = 0


    # store solution
    x = np.empty_like(t)
    y = np.empty_like(t)
    # record initial conditions
    x[0] = z0[0]
    y[0] = z0[1]
    
    
    # solve ODE
    for i in range(1,diseaseDuration):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        z = odeint(model,z0,tspan,args=(u[i],a,b,d,incubationDuration))
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
    plt.plot(t,x,'k-')
    plt.plot(t,y,'g-')

plt.axis([0,diseaseDuration,0,1])
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

# %%

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import time

# function that returns dz/dt
def model(z,t,u):
    x = z[0]
    y = z[1]
    if t < 14:
        dxdt = (-x + u - y)/a
        dydt = (-y + x)/d + c 
    else: 
        dxdt = (-x + u - y)/b
        dydt = (-y + x)/d + c 
    dzdt = [dxdt,dydt]
    return dzdt

startTime = time.time()
storeX = []
storeY = []

aMean = 15
aVariance = 5
bMean = 35
bVariance = 5
dMean = 10 
dVariance = 2


for timer in range(1000):
    # initial condition
    z0 = [0,0]
    a = np.random.normal(aMean,aVariance) # 3 30 30 100
    b = np.random.normal(bMean,bVariance) # 30 34
    c = 0
    d = np.random.normal(dMean,dVariance) # 10 100
    # number of time points
    n = 75
    # time points
    t = np.linspace(0,75,n+1)
    # step input
    u = np.zeros(n)
    # change to 2.0 at time = 5.0
    u[0:] = 1.0
    u[15:] = 0
    # store solution
    x = np.empty_like(t)
    y = np.empty_like(t)
    # record initial conditions
    x[0] = z0[0]
    y[0] = z0[1]
    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        z = odeint(model,z0,tspan,args=(u[i],))
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
    storeX.append(x)
    storeY.append(y)
    plt.plot(t,x,'b-',alpha = 0.05)
    plt.plot(t,y,'r-',alpha = 0.05)


for a,b,d in [[aMean ,bMean ,dMean],[aMean+2*aVariance,bMean-2*bVariance,dMean+2*dVariance],[aMean-2*aVariance,bMean+2*bVariance,dMean-2*dVariance]]:
    # initial condition
    z0 = [0,0]
    c = 0
    # number of time points
    n = 75
    # time points
    t = np.linspace(0,75,n)
    # step input
    u = np.zeros(n)
    # change to 2.0 at time = 5.0
    u[0:] = 1.0
    u[15:] = 0
    
    # store solution
    x = np.empty_like(t)
    y = np.empty_like(t)
    # record initial conditions
    x[0] = z0[0]
    y[0] = z0[1]
    
    
    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        z = odeint(model,z0,tspan,args=(u[i],))
        if z[1][0] < 0:
            z[1][0] = 0
        if z[1][1] < 0:
            z[1][1] = 0
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        # next initial condition
        z0 = z[1]
    plt.plot(t,x,'k-')
    plt.plot(t,y,'g-')

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))

    
# %% VACCINE


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import time

# function that returns dz/dt
def model(z,t,u):
    x = z[0]
    y = z[1]
    if t < 14:
        dxdt = (-x + u - y)/a
        dydt = (-y + x)/d + c 
    else: 
        dxdt = (-x + u - y)/b
        dydt = (-y + x)/d + c 
    dzdt = [dxdt,dydt]
    return dzdt

startTime = time.time()
storeX = []
storeY = []

aMean = 100
aVariance = 20
bMean = 25
bVariance = 5
dMean = 5
dVariance = 1


for timer in range(1000):
    # initial condition
    z0 = [0,0]
    a = np.random.normal(aMean,aVariance) # 3 30 30 100
    b = np.random.normal(bMean,bVariance) # 30 34
    c = 0
    d = np.random.normal(dMean,dVariance) # 10 100
    # number of time points
    n = 75
    # time points
    t = np.linspace(0,75,n+1)
    # step input
    u = np.zeros(n)
    # change to 2.0 at time = 5.0
    u[0:] = 1.0
    u[15:] = 0
    # store solution
    x = np.empty_like(t)
    y = np.empty_like(t)
    # record initial conditions
    x[0] = z0[0]
    y[0] = z0[1]
    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        z = odeint(model,z0,tspan,args=(u[i],))
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
    storeX.append(x)
    storeY.append(y)
    plt.plot(t,x,'b-',alpha = 0.05)
    plt.plot(t,y,'r-',alpha = 0.05)


for a,b,d in [[aMean ,bMean ,dMean],[aMean+2*aVariance,bMean-2*bVariance,dMean+2*dVariance],[aMean-2*aVariance,bMean+2*bVariance,dMean-2*dVariance]]:
    # initial condition
    z0 = [0,0]
    c = 0
    # number of time points
    n = 75
    # time points
    t = np.linspace(0,75,n)
    # step input
    u = np.zeros(n)
    # change to 2.0 at time = 5.0
    u[0:] = 1.0
    u[15:] = 0
    
    # store solution
    x = np.empty_like(t)
    y = np.empty_like(t)
    # record initial conditions
    x[0] = z0[0]
    y[0] = z0[1]
    
    
    # solve ODE
    for i in range(1,n):
        # span for next time step
        tspan = [t[i-1],t[i]]
        # solve for next step
        z = odeint(model,z0,tspan,args=(u[i],))
        if z[1][0] < 0:
            z[1][0] = 0
        if z[1][1] < 0:
            z[1][1] = 0
        # store solution for plotting
        x[i] = z[1][0]
        y[i] = z[1][1]
        # next initial condition
        z0 = z[1]
    plt.plot(t,x,'k-')
    plt.plot(t,y,'g-')

plt.axis([0,75,0,1])

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))