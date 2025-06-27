import random
import os
from PIL import Image
import colorsys

from Site import Site
from ColourList import rgbColours, maxColours

class AsciiImage:
	def __init__(self, lines = []):
		self.lines = lines

#	def Save(self, filename = "./output/ascii.txt"):
#		contents = ""
#		for line in self.lines:
#			contents += line + "\n"
#		
#		with open(filename, "w") as file:
#			file.write(contents.encode('utf8'))
	
	def Print(self):
		for line in self.lines:
				print(line)

# a square grid of sites, with nearest-neighbour edges chosen at random
class Grid:
	def __init__(self, size, p, clusters=True, diameter=False):
		self.size = size
		self.p = p

		self.clusters = []
		self.maxClusterIndex = 0
		self.maxClusterSize = 0

		self.diameter = 0
		self.start = None
		self.end = None

		# populate grid sites
		self.sites = []
		for y in range(self.size):
			for x in range(self.size):
				self.sites.append(Site(x,y))
		
		self.Reset(clusters, diameter)
	
	def Reset(self, clusters, diameter):
		# reset site data
		for s in self.sites:
			s.east = None
			s.north = None
			s.west = None
			s.south = None
			s.onPath = False
			s.parent = None
			s.clusterIndex = -1

		# populate adjacencies randomly
		for s in self.sites:
			# horizontal edges
			if s.x < self.size - 1:
				if random.random() < self.p:
					east = self.At(s.x + 1, s.y)
					if s.east == None:
						s.east = east
						east.west = s
			# vertical edges
			if s.y < self.size - 1:
				if random.random() < self.p:
					south = self.At(s.x, s.y + 1)
					if s.south == None:
						s.south = south
						south.north = s

		if clusters:
			self.AnalyseClusters()
		else:
			self.clusters = []
			self.maxClusterIndex = 0
			self.maxClusterSize = 0

		if diameter:
			self.FindDiameter()
		else:
			self.diameter = 0
			self.start = None
			self.end = None

	def AnalyseClusters(self):
		index = 0

		# search for sites not yet clustered
		for site in self.sites:
			if site.clusterIndex >= 0:
				continue

			# new cluster found, initialise search data
			cluster = []
			queue = [site]
			site.clusterIndex = index

			# bfs to fill out cluster
			while queue:
				site = queue.pop(0)
				for i in range(4):
					neighbour = site.Neighbour(i)
					if neighbour:
						if neighbour.clusterIndex == -1:
							queue.append(neighbour)
							neighbour.clusterIndex = index
				cluster.append(site)
			
			self.clusters.append(cluster)
			clusterSize = len(cluster)
			if clusterSize > self.maxClusterSize:
				self.maxClusterSize = clusterSize
				self.maxClusterIndex = index
			
			index += 1

	# return the site object at specified grid point
	def At(self, x, y):
		return self.sites[y * self.size + x]
	
	# computes graph eccentricity (max distance to another site with the same cluster) for a given site
	# sets the eccentricity data field and returns a site of that max distance away
	def Eccentricity(self, start):
		if not start:
			return None
		
		assert start in self.sites, "Given Site object does not belong to this Grid"

		distance = 0
		end = None

		sites = self.clusters[start.clusterIndex] if self.clusters else self.sites
		for site in sites:
			site.searchFlag = False

		queue = [start]
		start.searchFlag = True

		while queue:
			distance += 1
			nextQueue = []
			for site in queue:
				end = site
				for i in range(4):
					neighbour = site.Neighbour(i)
					if neighbour:
						if not neighbour.searchFlag:
							neighbour.searchFlag = True
							nextQueue.append(neighbour)
			queue = nextQueue
		
		start.eccentricity = distance
		return end

	# find a path of maximal length (i.e. graph diameter) using breadth-first
	# sets start, end, diameter fields, no return
	def FindDiameter(self):
		diam = 0

		for site in self.sites:
			end = self.Eccentricity(site)
			ecc = site.eccentricity
			if ecc > diam:
				diam = ecc
				self.start = site
				self.end = end

		self.diameter = diam

	# print ascii display of grid
	# (requires a sufficiently large terminal window to display correctly)
	def GenerateAsciiImage(self, print = True, onlyLargestCluster = False, seed = None):
		ansiColours = [f"\033[38;2;{c[0]};{c[1]};{c[2]}m" for c in rgbColours]
		lines = []

		furthest = self.FurthestFrom(seed)[0]

		for y in range(self.size):
			horizontal = ""
			vertical = ""
			for x in range(self.size):
				site = self.At(x,y)

				if onlyLargestCluster and site.clusterIndex != self.maxClusterIndex:
					# skip
					horizontal += "    "
					vertical += "    "
				else:
					# draw site
					horizontal += ansiColours[site.clusterIndex % maxColours]
					if site == seed:
						horizontal += "Ｓ"
					elif site == furthest:
						horizontal += "Ｅ"
					elif site.onPath:
						horizontal += "＠"
					else:
						horizontal += "ｏ"
					horizontal += "\033[0m"

					# draw edges
					if x < self.size - 1:
						if site == self.At(x+1, y).west:
							horizontal += "－"
						else:
							horizontal += "  "
					if y < self.size - 1:
						if site == self.At(x, y+1).north:
							vertical += "｜"
						else:
							vertical += "  "
					vertical += "  "

			lines.append(horizontal)
			lines.append(vertical)

		image = AsciiImage(lines)
		if print:
			image.Print()
		return image

	# generate bitmap image from grid
	def GenerateTilemappedImage(self, start = None, end = None):
		tiles = []
		for i in range(16):
			file = "./tiles/" + hex(i)[-1].upper() + ".png"
			tiles.append(Image.open(file))
		#tiles.append(Image.open("./tiles/X.png"))
		
		imageSize = 32 * self.size
		image = Image.new("RGB", (imageSize, imageSize))

		for y in range(self.size):
			for x in range(self.size):
				site = self.At(x,y)

				offset = 0
				if site == start and site.x == 0:
					offset = 4
				if site == end and site.x == self.size - 1:
					offset = 1

				image.paste(tiles[site.TileIndex() + offset], (32 * x, 32 * y))

				#if end and site.marked:
				#	image.paste(tiles[-1], (32 * x, 32 * y), tiles[-1])

		for tile in tiles:
			tile.close()
		
		return image
	
	def GenerateClusterImage(self, scale = 1, save = True, show = True):
		image = Image.new("RGB", (scale * self.size, scale * self.size))

		# populate and randomise list of colours
		#colours = [tuple(round(c * 255) for c rgbColours]
		#random.shuffle(colours)

		# draw a scaleXscale block for each site, colouring based on its clusterIndex
		for y in range(self.size):
			for x in range(self.size):
				site = self.At(x,y)
				colour = rgbColours[site.clusterIndex % maxColours]
				for j in range(scale):
					for i in range(scale):
						image.putpixel((scale * x + i, scale * y + j), colour)
		
		if save:
			image.save(f"./output/clusters_{self.size}_{self.p:.2f}.png")
		if show:
			image.show()

		return image