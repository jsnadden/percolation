

# search for spanning cluster (via FloodFill)
def FloodFill(grid, x, y):
	# initialise search data
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
				for neighbour in site.neighbours:
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