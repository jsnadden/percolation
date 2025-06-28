import sys
import numpy as np
import matplotlib.pyplot as plt
from time import time

from Grid import Grid
from StatMech import PhaseTransition

samplesPerSize = 1
sizeCount = 10
sizeStep = 1

# parse command line arguments
args = sys.argv
if len(args) > 1:
    samplesPerSize = int(args[1])
if len(args) > 2:
    sizeCount = int(args[2])
if len(args) > 3:
    sizeStep = int(args[3])

sizes = [sizeStep * (i + 1) for i in range(sizeCount)]
diameters = []
times = []

for size in sizes:
    subtotal = 0
    startTime = time()
    for sample in range(samplesPerSize):
        grid = Grid(size, .5)
        diameter = len(grid.DiametricPath())
        subtotal += diameter
    times.append((time() - startTime)/samplesPerSize)
    diameters.append(subtotal/samplesPerSize)

timeModel = np.poly1d(np.polyfit(sizes, np.log(times), 1))
timeCoeffs = timeModel.coefficients
timeR = np.corrcoef(sizes, np.log(times))[0,1]
timeR2 = timeR * timeR

diamModel = np.poly1d(np.polyfit(sizes, diameters, 1))
diamCoeffs = diamModel.coefficients
diamR = np.corrcoef(sizes, diameters)[0,1]
diamR2 = diamR * diamR

plt.scatter(sizes, times, label = "measured", color='k')
plt.plot(sizes, np.exp(timeModel(sizes)), label = f"least-squares exponential model (log(y) = {timeCoeffs[0]:.2f} x + {timeCoeffs[1]:.2f}, r^2 = {timeR2:.2f})", color='b')
plt.legend()
plt.title(f"Mean computation time for diameter of random 2d grid subgraphs (p = 0.5) \n({samplesPerSize} samples per datum)")
plt.xlabel("Grid size")
plt.ylabel("Time (s)")
plt.savefig(f"./output/diameter_timing.png")
plt.show()
plt.clf()

plt.scatter(sizes, diameters, label = "measured", color='k')
plt.plot(sizes, diamModel(sizes), label = f"least-squares linear model (y = {diamCoeffs[0]:.2f} x + {diamCoeffs[1]:.2f}, r^2 = {diamR2:.2f})", color='b')
plt.legend()
plt.title(f"Mean diameter of random subgraphs of a 2d grid (p = 0.5) \n({samplesPerSize} samples per point)")
plt.xlabel("Grid size")
plt.ylabel("Diameter")
plt.savefig(f"./output/diameter_scaling.png")
plt.show()
plt.clf()
