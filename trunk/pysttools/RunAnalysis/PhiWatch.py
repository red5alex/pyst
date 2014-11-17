__author__ = 'are'

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import pyst


# find the OUT - file in calling directory
currentDir = os.getcwd()
outfiles = []

for file in os.listdir(currentDir):
    if file.endswith(".out"):
        outfiles.append(file)

if len(outfiles) > 1:
    print("Warning: More than one one out-file found, using " + outfiles[-1])

if len(outfiles) < 1:
    print("Error: No out-file found! Aborting...")
    sys.exit(1)

# Load the out-file
filename = currentDir+"\\"+outfiles[-1]
f = pyst.PestOutFile(filename)


"""
This shows an example of the "fivethirtyeight" styling, which
tries to replicate the styles from FiveThirtyEight.com.
"""

groups = f.getObsGroups()


x = np.linspace(0, 10)

iterations = []
iterations.extend(range(0, len(f.Iterations)))

#with plt.style.context('fivethirtyeight'):
for grp in groups:
    if "regul_" in grp:
        phis = []
        for it in f.Iterations:
            phis.append(it.startingPhis[grp])
        plt.plot(iterations, phis, label=grp)
        plt.legend(shadow=True, fancybox=True, loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
