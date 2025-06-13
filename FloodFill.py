

# search for optimal spanning path (via FloodFill)
def FloodFill(grid, x, y):
	# initialise grid data
	for site in grid.sites:
		site.added = False
		site.checked = False
		site.parent = None
		site.marked = False    
	seed = grid.At(x,y)
	found = False
	output = None
	cluster = [seed]
	toCheck = 1
	seed.added = True
	
	while toCheck > 0:
		for site in cluster:
			if site.checked == False:
				for i in range(4):
					neighbour = site.Neighbour(i)
					if neighbour:
						if not(found) and neighbour.x == grid.size - 1:
							output = neighbour
							found = True
							neighbour.parent = site
						if not neighbour.added:
							cluster.append(neighbour)
							neighbour.added = True
							neighbour.parent = site
							toCheck += 1
				site.checked = True
				toCheck -= 1
	
	if found:
		# mark our spanning path
		x = output
		while x != None:
			x.marked = True
			x = x.parent

	return output

def FindClusters(grid):
	# initialise grid data
	for site in grid.sites:
		site.added = False
		site.checked = False
	
	clusters = []
	index = 0

	for site in grid.sites:
		if site.added:
			continue

		cluster = [site]
		toCheck = 1
		site.added = True
		site.clusterIndex = index

		while toCheck > 0:
			for site in cluster:
				if site.checked:
					continue
				for i in range(4):
					neighbour = site.Neighbour(i)
					if neighbour:
						if not neighbour.added:
							cluster.append(neighbour)
							neighbour.added = True
							neighbour.clusterIndex = index
							toCheck += 1
				site.checked = True
				toCheck -= 1
		clusters.append(cluster)
		index += 1
	return clusters


