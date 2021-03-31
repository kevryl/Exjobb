# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 17:03:12 2021

@author: kevin

https://apmonitor.com/pdc/index.php/Main/SolveDifferentialEquations
"""


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# function that returns dz/dt
def model(z,t):
    dxdt = 1 * z[0] - 0.01 * z[1] * z[0]
    dydt = 1 - 0.5* z[1]
    dzdt = [dxdt,dydt]
    return dzdt

# initial condition
z0 = [20,0]

# time points
t = np.linspace(0,30)

# solve ODE
z = odeint(model,z0,t)

# plot results
plt.plot(t,z[:,0],'b-',label=r'virus')
plt.plot(t,z[:,1],'r--',label=r'antibody')
plt.ylabel('response')
plt.xlabel('time')
plt.legend(loc='best')
plt.title("ALT 1")
plt.show()

# %%

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# function that returns dz/dt
def model(z,t):
    dxdt = 1 * z[0] - 0.01 * z[1] * z[0]
    dydt = 1 * z[0]- 0.5* z[1]
    dzdt = [dxdt,dydt]
    return dzdt

# initial condition
z0 = [20,0]

# number of time points
n = 501

# time points
t = np.linspace(0,60,n)

# solve ODE
z = odeint(model,z0,t)

# plot results
plt.plot(t,z[:,0],'b-',label=r'virus')
plt.plot(t,z[:,1],'r--',label=r'antibody')
plt.ylabel('response')
plt.xlabel('time')
plt.legend(loc='best')
plt.title("ALT 2")
plt.show()


# %%

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# function that returns dz/dt
def model(z,t):
    k = 5
    p = 0.01
    d = 0.01
    c = 1
    b = 1
    dxdt = k * z[0] - p * z[1] * z[0] - d * z[0]
    dydt = c * z[0]- b* z[1]
    dzdt = [dxdt,dydt]
    return dzdt

# initial condition
z0 = [1,0]

# number of time points
n = 501

# time points
t = np.linspace(0,60,n)

# solve ODE
z = odeint(model,z0,t)

# plot results
plt.plot(t,z[:,0],'b-',label=r'$\dot{x} = kx - pxy - dx$')
plt.plot(t,z[:,1],'r--',label=r'$\dot{y} = cx - by$')
plt.ylabel('response')
plt.xlabel('time')
plt.legend(loc='best')
plt.title("ALT 3")
plt.show()
# %%

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# function that returns dz/dt
def model(z,t):
    k = 1
    p = 0.01
    c = 0.2
    b = 0.1
    if t < 10:
        dxdt = k * z[0] - p * z[1] * z[0]
        dydt = 0
    else:
        dxdt = k * z[0] - p * z[1] * z[0]
        dydt = c * z[0] - b * z[1]
    dzdt = [dxdt,dydt]
    return dzdt

# initial condition
z0 = [20,0]

# time points
t = np.linspace(0,200)

# solve ODE
z = odeint(model,z0,t)

# plot results
plt.plot(t,z[:,0],'b-',label=r'virus')
plt.plot(t,z[:,1],'r--',label=r'antibody')
plt.ylabel('response')
plt.xlabel('time')
plt.legend(loc='best')
plt.title("ALT 2")
plt.show()

