import random
from PIL import Image
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
	def AsciiPlot(self):
		for y in range(self.size):
			horizontal = ""
			vertical = ""
			for x in range(self.size):
				site = self.At(x,y)

				# draw site
				if site.marked:
					horizontal += "\033[92m"
					horizontal += "＠"
					horizontal += "\033[0m"
				elif site.added:
					horizontal += "\033[94m"
					horizontal += "Ｏ"
					horizontal += "\033[0m"
				else:
					horizontal += "ｏ"

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
	def GenerateImage(self, outputFilepath, start, end):
		tiles = []
		for i in range(16):
			file = "./tiles/" + hex(i)[-1].upper() + ".png"
			tiles.append(Image.open(file))
		
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
		
		image.save(outputFilepath)

		for tile in tiles:
			tile.close()