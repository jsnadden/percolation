import sys
import time
import numpy as np
import matplotlib.pyplot as plt

from Grid import Grid

gridSize = 10
dataPoints = 20
samples = 1

# parse command line arguments
args = sys.argv
if len(args) > 1:
    gridSize = int(args[1])
if len(args) > 2:
    dataPoints = int(args[2])
if len(args) > 3:
    samples = int(args[3])

pValues = [(i+1)/dataPoints for i in range(dataPoints)]
data = []

for p in pValues:
    x = 0
    for s in range(samples):
        grid = Grid(gridSize, p)
        clusterSizes = np.array([len(c) for c in grid.clusters])
        x += np.max(clusterSizes)
    data.append(x/samples)

plt.plot(pValues, np.array(data))
plt.title(f"Mean max cluster sizes ({gridSize}x{gridSize} grid, {samples} samples per point)")
plt.xlabel("p")
plt.ylabel("Max cluster size")
plt.savefig(f"./output/max_cluster_sizes_{gridSize}_{samples}.png")
plt.show()

#clusterImage = grid.GenerateClusterImage(10)
#clusterImage.save(f"./output/clusters_{gridSize}_{edgeProbability:.2f}.png")
#clusterImage.show()
#
#if (gridSize < 35):
#    asciiImage = grid.GenerateAsciiImage()
#    asciiImage.Print()