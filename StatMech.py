import numpy as np
import matplotlib.pyplot as plt

from Grid import Grid

def PhaseTransition(gridSize = 10, dataPoints = 20, samples = 1):
	pValues = [(i+1)/dataPoints for i in range(dataPoints)]
	meanMaxClusterSize = []

	for p in pValues:
		x = 0
		for s in range(samples):
			x += Grid(gridSize, p).maxClusterSize
		meanMaxClusterSize.append(x / samples)
	
	data = [pValues, meanMaxClusterSize]
	np.savetxt("foo.csv", np.transpose(np.array(data)), delimiter=",")

	plt.plot(data[0], data[1])
	plt.title(f"Mean max cluster sizes ({gridSize}x{gridSize} grid, {samples} samples per point)")
	plt.xlabel("p")
	plt.ylabel("Max cluster size")
	plt.savefig(f"./output/max_cluster_sizes_{gridSize}_{samples}.png")
	plt.show()