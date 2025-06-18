import sys
import numpy as np
import matplotlib.pyplot as plt
import random

from Grid import Grid
from StatMech import PhaseTransition


gridSize = 10
p = .5

# parse command line arguments
args = sys.argv
if len(args) > 1:
    gridSize = int(args[1])
if len(args) > 2:
    p = float(args[2])

X = [i + 1 for i in range(gridSize)]
Y = []

samples = 50

for x in X:
    subtotal = 0
    for repeat in range(samples):
        grid = Grid(x, p)
        cluster = grid.clusters[grid.maxClusterIndex]
        subtotal += grid.FurthestFrom(random.choice(cluster))[1]

    Y.append(subtotal / samples)

A = np.vstack([X, np.ones(len(X))]).T
m, c = np.linalg.lstsq(A, Y)[0]
Z = [m*x+c for x in X]

plt.plot(X, Y, label = "measured")
plt.plot(X, Z, label = f"least squares (m = {m:.2f}, c = {c:.2f})")
plt.legend()
plt.title(f"Mean eccentricity of sites in largest cluster\n({samples} samples per point, p = {p})")
plt.xlabel("Grid size")
plt.ylabel("Eccentricity")
plt.savefig(f"./output/eccentricity_scaling.png")
plt.show()
#grid.GenerateAsciiImage(print = True, onlyLargestCluster = True, seed = site)
#print(f"Largest cluster contains {grid.maxClusterSize} sites.")
#print(f"Furthest point from the site ({site.x},{site.y}) is ({furthest[0].x},{furthest[0].y}) at a distance of {furthest[1]}")