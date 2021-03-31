# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:39:44 2021

@author: kevin
"""

import numpy as np
import matplotlib.pyplot as plt

virus = 1000
tcell = 0
mcell = 3

a = 0.01
b = 0.03
d = 0.017
e = 0.07
f = .11
g = 0.0005
h = 0.0012

virusPlot = [virus]
tcellPlot = [tcell]
mcellPlot = [mcell]


time = 10000
for ix in range(time):
    dvdt = a*virus - b*tcell  
    dTdt = d*virus - e*tcell + f*mcell
    dMdt = g*tcell - h*mcell
    virus = virus + dvdt
    tcell = tcell + dTdt
    mcell = mcell + dMdt
    if virus < 0: virus = 0
    if tcell < 0: tcell = 0
    if mcell < 0: mcell = 0
    virusPlot.append(virus)
    tcellPlot.append(tcell)
    mcellPlot.append(mcell)
    
    
plt.plot(range(time+1),virusPlot,label = 'virus')
plt.plot(range(time+1),tcellPlot, label = 'tcell')
plt.plot(range(time+1),mcellPlot, label = 'mcell')

plt.axis([0, time, np.min([virusPlot,tcellPlot,mcellPlot]), np.max([virusPlot,tcellPlot,mcellPlot])])

#%%
virus = 0
tcell = 500
mcell = 500

a = 0.01
b = 0.03
d = 0.017
e = 0.07
f = .11
g = 0.0005
h = 0.0012

virusPlot = [virus]
tcellPlot = [tcell]
mcellPlot = [mcell]


time = 10000
for ix in range(time):
    dvdt = a*virus - b*tcell  
    dTdt = d*virus - e*tcell + f*mcell
    dMdt = g*tcell - h*mcell
    virus = virus + dvdt
    tcell = tcell + dTdt
    mcell = mcell + dMdt
    if virus < 0: virus = 0
    if tcell < 0: tcell = 0
    if mcell < 0: mcell = 0
    virusPlot.append(virus)
    tcellPlot.append(tcell)
    mcellPlot.append(mcell)
    
    
plt.plot(range(time+1),virusPlot,label = 'virus2')
plt.plot(range(time+1),tcellPlot, label = 'tcell2')
plt.plot(range(time+1),mcellPlot, label = 'mcell2')
# plt.yscale('log')
plt.legend()

#%%

import numpy as np
import matplotlib.pyplot as plt

virus = 1000
tcell = 0
mcell = 3

a = 0.01
b = 0.025
c = 0.01
d = 0.017
e = 0.07
f = .11
g = 0.0005
h = 0.0012

virusPlot = [virus]
tcellPlot = [tcell]
mcellPlot = [mcell]


time = 10000
for ix in range(time):
    dvdt = a*virus - b*tcell  - c*mcell 
    dTdt = d*virus - e*tcell + f*mcell
    dMdt = g*tcell - h*mcell
    virus = virus + dvdt
    tcell = tcell + dTdt
    mcell = mcell + dMdt
    if virus < 0: virus = 0
    if tcell < 0: tcell = 0
    if mcell < 0: mcell = 0
    virusPlot.append(virus)
    tcellPlot.append(tcell)
    mcellPlot.append(mcell)
    
    
plt.plot(range(time+1),virusPlot,label = 'virus')
plt.plot(range(time+1),tcellPlot, label = 'tcell')
plt.plot(range(time+1),mcellPlot, label = 'mcell')
plt.plot(range(time+1),np.add(tcellPlot,virusPlot), label = 'mcell')
plt.legend()


#%%

import numpy as np
import matplotlib.pyplot as plt

virus = 10000
tcell = tcellPlot[4000]
mcell = tcellPlot[4000]

a = 0.01
b = 0.025
c = 0.01
d = 0.017
e = 0.07
f = .11
g = 0.0005
h = 0.0012

virusPlot = [virus]
tcellPlot = [tcell]
mcellPlot = [mcell]


time = 10000
for ix in range(time):
    dvdt = a*virus - b*tcell  - c*mcell
    dTdt = d*virus - e*tcell + f*mcell
    dMdt = g*tcell - h*mcell
    virus = virus + dvdt
    tcell = tcell + dTdt
    mcell = mcell + dMdt
    if virus < 0: virus = 0
    if tcell < 0: tcell = 0
    if mcell < 0: mcell = 0
    virusPlot.append(virus)
    tcellPlot.append(tcell)
    mcellPlot.append(mcell)
    
    
plt.plot(range(time+1),virusPlot,label = 'virus')
plt.plot(range(time+1),tcellPlot, label = 'tcell')
plt.plot(range(time+1),mcellPlot, label = 'mcell')
plt.legend()
#%%
import numpy as np
import matplotlib.pyplot as plt

virus = 10000
tcell = 10
mcell = 10000

konstant = 1000
a = 5/konstant
b = 4/konstant
c = 5/konstant
d = 3/konstant
e = 0.5/konstant
f = 0.1/konstant


virusPlot = [virus]
tcellPlot = [tcell]
mcellPlot = [mcell]


time = konstant*10
for ix in range(time):
    dvdt = a*virus - b*tcell 
    dTdt = c*virus - d*tcell
    dMdt = e*tcell - f*mcell
    virus = virus + dvdt
    tcell = tcell + dTdt
    mcell = mcell + dMdt
    if virus < 0: virus = 0
    if tcell < 0: tcell = 0
    if mcell < 0: mcell = 0
    virusPlot.append(virus)
    tcellPlot.append(tcell)
    mcellPlot.append(mcell)
    
    
plt.plot(range(time+1),virusPlot,label = 'virus')
plt.plot(range(time+1),tcellPlot, label = 'tcell')
plt.plot(range(time+1),mcellPlot, label = 'mcell')
plt.legend()

#%%
import numpy as np
import matplotlib.pyplot as plt

virus = 10000
tcell = 10
mcell = 10

konstant = 10
a = 2.5/konstant
b = 2/konstant
c = 2/konstant
d = 2/konstant
e = 1.2/konstant
f = 0.1/konstant
g = 1/konstant


virusPlot = [virus]
tcellPlot = [tcell]
mcellPlot = [mcell]


time = konstant*10
for ix in range(time):
    dvdt = a*virus - b*tcell 
    dTdt = c*virus + d*mcell - e*tcell
    dMdt = f*tcell - g*mcell
    virus = virus + dvdt
    tcell = tcell + dTdt
    mcell = mcell + dMdt
    if virus < 0: virus = 0
    if tcell < 0: tcell = 0
    if mcell < 0: mcell = 0
    virusPlot.append(virus)
    tcellPlot.append(tcell)
    mcellPlot.append(mcell)
    
    
plt.plot(range(time+1),virusPlot,label = 'virus')
plt.plot(range(time+1),tcellPlot, label = 'tcell')
plt.plot(range(time+1),mcellPlot, label = 'mcell')
plt.legend()

