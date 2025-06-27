import sys
import numpy as np
import matplotlib.pyplot as plt

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

def ComputeMeanDiameter(size):
    subtotal = 0
    for sample in range(samplesPerSize):
        grid = Grid(size, .5, False, True)
        subtotal += grid.diameter
    return subtotal / samplesPerSize

diameters = [ComputeMeanDiameter(size) for size in sizes] 

#A = np.vstack([[size for size in sizes], np.ones(len(sizes))]).T
#m, c = np.linalg.lstsq(A, diameters)[0]
#predictions = [m*x + c for x in sizes]

model = np.poly1d(np.polyfit(sizes, diameters, 1))
coeffs = model.coefficients
r = np.corrcoef(sizes, diameters)[0,1]
polyline = np.linspace(0, sizeCount * sizeStep, sizeCount)

plt.scatter(sizes, diameters, label = "measured", color='k')
plt.plot(polyline, model(polyline), label = f"least-squares linear model (y = {coeffs[0]:.2f} x + {coeffs[1]:.2f}, r^2 = {r*r:.2f})", color='r')
plt.legend()
plt.title(f"Mean diameter of random grid subgraphs (p = 0.5) \n({samplesPerSize} samples per datum)")
plt.xlabel("Grid size")
plt.ylabel("Diameter")
plt.savefig(f"./output/diameter_scaling.png")
plt.show()
