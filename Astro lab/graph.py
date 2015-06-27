# Astronomical Image Processing
# David Christopher Ragusa + Aidan Boxall

import scipy.optimize as optimisation
import matplotlib.pyplot as plt
import numpy as np
import cPickle

with open('mosaiccatalog.pkl', 'rb') as catalogfile:  # with, for automatic closing
    catalog = cPickle.load(catalogfile)

mags = [item['mag'] for item in catalog]  # list of magnitudes

values, base = np.histogram(mags, bins=80)

cumulative = np.cumsum(values)  #evaluate the cumulative
cumulative_error = np.sqrt(cumulative)

# Split data into 3 sections: the lower curving section, the middle
# straight line section, and the higher roll-off section.
# This is so we can perform a fit directly in Python.

startbase = []
startcum = []
starterr = []
straightbase = []
straightcum = []
straighterr = []
endbase = []
endcum = []
enderr = []

for index in range(len(base[:-1])):
    if index in range(0,9):  # plot lower section
        startbase.append(base[index])
        startcum.append(cumulative[index])
        starterr.append(cumulative_error[index])
    elif index in range(9,45):  # plot middle straight line section
        straightbase.append(base[index])
        straightcum.append(cumulative[index])
        straighterr.append(cumulative_error[index])
    else:  # plot higher section
        endbase.append(base[index])
        endcum.append(cumulative[index])
        enderr.append(cumulative_error[index])

# convert all the lists to numpy arrays
startbase = np.array(startbase)
startcum = np.array(startcum)
starterr = np.array(starterr)
straightbase = np.array(straightbase)
straightcum = np.array(straightcum)
straighterr = np.array(straighterr)
endbase = np.array(endbase)
endcum = np.array(endcum)
enderr = np.array(enderr)

def func(x,m,c):  # straight line function
    return m*x + c

params, matrix = optimisation.curve_fit(func, straightbase, np.log10(straightcum), [0.0,0.0], straighterr)  # the actual optimisation
m, c = params
graderr = np.sqrt(matrix[0,0])
print "Gradient: %s" % m
print "Intercept: %s" % c
print "Gradient error: %s" % graderr

fit = [10**func(x,m,c) for x in straightbase]

# plot the three sections, centre in blue
plt.errorbar(straightbase, straightcum, straighterr, c='blue')
plt.errorbar(startbase, startcum, starterr, c='green')
plt.errorbar(endbase[:-1], endcum[:-1], enderr[:-1], c='green')

plt.plot(straightbase, fit, c='red')  # fit line

x1,x2,y1,y2 = plt.axis()
plt.axis((x1-0.5,22,y1,10000))

plt.yscale('log')
plt.ylabel('No. of galaxies below magnitude')
plt.xlabel('Magnitude')

plt.show()
