import sys
from Grid import Grid
from FloodFill import FloodFill, FindClusters

gridSize = 10
edgeProbability = .5

# parse command line arguments
args = sys.argv
if len(args) > 1:
    gridSize = int(args[1])
if len(args) > 2:
    edgeProbability = float(args[2])

# create a random grid with the specified parameters, search for a spanning path, and print an ascii depiction of the results
grid = Grid(gridSize, edgeProbability)
entrance = grid.At(0, int(gridSize / 2))
exit = FloodFill(grid, 0, int(gridSize / 2))
clusters = FindClusters(grid)
grid.GenerateClusterImage(1).save(f"./output/clusters_{gridSize}_{edgeProbability:.2f}.png")


#image = grid.GenerateImageFromTiles(entrance, exit)
#filename = "./output/" + str(gridSize) + "_" + str(edgeProbability) + ".png"
#image.save(filename)
#image.show()