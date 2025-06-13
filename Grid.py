import random
from PIL import Image
import colorsys
from Site import Site

# a square grid of sites, with nearest-neighbour edges chosen at random
class Grid:
	def __init__(self, size, p):
		self.size = size
		self.p = p
		self.sites = []

		# populate vertices
		for y in range(size):
			for x in range(size):
				newSite = Site(x,y)
				self.sites.append(newSite)

		# populate edges randomly
		for s in self.sites:
			# horizontal edges
			if s.x < size - 1:
				if random.random() < self.p:
					east = self.At(s.x + 1, s.y)
					if s.east == None:
						s.east = east
						east.west = s
			# vertical edges
			if s.y < size - 1:
				if random.random() < self.p:
					south = self.At(s.x, s.y + 1)
					if s.south == None:
						s.south = south
						south.north = s

	# return the site object at specified grid point
	def At(self, x,y):
		return self.sites[y * self.size + x]

	# print ascii display of grid (highlights a spanning path, if one is found)
	# requires a sufficiently large terminal window to display correctly
	def GenerateAsciiImage(self, clusters = []):
		ansiColours = [f"\033[38;5;{i}m" for i in range(256)]

		for y in range(self.size):
			horizontal = ""
			vertical = ""
			for x in range(self.size):
				site = self.At(x,y)

				# draw site
				horizontal += ansiColours[site.clusterIndex % 256]
				horizontal += "Ｏ"
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
			print(horizontal)
			print(vertical)

	# generate bitmap image from grid
	def GenerateTilemappedImage(self, start = None, end = None):
		tiles = []
		for i in range(16):
			file = "./tiles/" + hex(i)[-1].upper() + ".png"
			tiles.append(Image.open(file))
		tiles.append(Image.open("./tiles/X.png"))
		
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

				if end and site.marked:
					image.paste(tiles[-1], (32 * x, 32 * y), tiles[-1])

		for tile in tiles:
			tile.close()
		
		return image
	
	def GenerateClusterImage(self, scale = 1, maxColours = 256):
		image = Image.new("RGB", (scale * self.size, scale * self.size))

		colours = [tuple(round(c * 255) for c in colorsys.hsv_to_rgb(h / maxColours, 1, 1)) for h in range(maxColours)]
		random.shuffle(colours)

		for y in range(self.size):
			for x in range(self.size):
				site = self.At(x,y)
				colour = colours[site.clusterIndex % maxColours]
				for j in range(scale):
					for i in range(scale):
						image.putpixel((scale * x + i, scale * y + j), colour)
		
		return image