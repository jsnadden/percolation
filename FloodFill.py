

def AnalyseClusters(grid):
	# reset site data
	for site in grid.sites:
		site.onPath = False
		site.parent = None
		site.clusterIndex = -1

	# initialise cluster data
	clusters = []
	index = 0

	# search the grid for sites not yet clustered
	for site in grid.sites:
		if site.clusterIndex > -1:
			continue

		# new cluster found, initialise floodfill data
		cluster = []
		queue = [site]
		site.clusterIndex = index

		# floodfill to fill out cluster
		while queue:
			site = queue.pop(0)
			for i in range(4):
				neighbour = site.Neighbour(i)
				if neighbour:
					if neighbour.clusterIndex == -1:
						queue.append(neighbour)
						neighbour.clusterIndex = index
			cluster.append(site)
		
		clusters.append(cluster)
		index += 1
	
	return clusters


