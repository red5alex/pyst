__author__ = 'are'

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

import pyst


#  find the OUT - file in calling directory
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

#  Load the out-file
filename = currentDir+"\\"+outfiles[-1]
f = pyst.PestOutFile(filename)

#  vizualization


from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.gca(projection='3d')

cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)

xs = range(0, len(f.Iterations))
verts = []

zs = range(0,len(f.getObsGroups())-1)
for z in zs:


    ys = list(range(0, len(xs)-1))

    ys = list(f.Iterations[z].startingPhis.values())

    ys[0], ys[-1] = 0, 0
    verts.append(list(zip(xs, ys)))

poly = PolyCollection(verts, facecolors = [cc('r'), cc('g'), cc('b'),
                                           cc('y')])
poly.set_alpha(0.7)
ax.add_collection3d(poly, zs=zs, zdir='y')

ax.set_xlabel('x Iteration')
ax.set_xlim3d(0, len(xs))
ax.set_ylabel('y Group')
ax.set_ylim3d(0, len(ys))
ax.set_zlabel('z Phi')
ax.set_zlim3d(0, 1)

plt.show()

"""
http://stackoverflow.com/questions/23880138/display-a-3d-bar-graph-using-transparency-and-multiple-colors-in-matplotlib
"""
"""

groups = list(f.getObsGroups())
groups.sort()
iterations = range(0, len(f.Iterations))

#with plt.style.context('fivethirtyeight'):
for grp in groups:
    if "regul_" in grp:
        phis = []
        for it in f.Iterations:
            phis.append(it.startingPhis[grp])
        plt.plot(iterations, phis, label=grp.replace("regul_",""))
        plt.legend(shadow=True, fancybox=True, loc='center left', bbox_to_anchor=(1, 0.5))
plt.yscale('log')
plt.show()
"""