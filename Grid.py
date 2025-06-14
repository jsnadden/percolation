import random
from PIL import Image
import colorsys
from Site import Site
from FloodFill import AnalyseClusters
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
	def __init__(self, size, p):
		self.size = size
		self.p = p
		self.clusters = []

		# populate grid sites
		self.sites = []
		for y in range(self.size):
			for x in range(self.size):
				self.sites.append(Site(x,y))
		
		self.Reset()
	
	def Reset(self):
		# reset site data
		for s in self.sites:
			s.east = None
			s.north = None
			s.west = None
			s.south = None

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

		self.clusters = AnalyseClusters(self)


	# return the site object at specified grid point
	def At(self, x,y):
		return self.sites[y * self.size + x]

	# print ascii display of grid
	# (requires a sufficiently large terminal window to display correctly)
	def GenerateAsciiImage(self):
		ansiColours = [f"\033[38;2;{c[0]};{c[1]};{c[2]}m" for c in rgbColours]
		lines = []

		for y in range(self.size):
			horizontal = ""
			vertical = ""
			for x in range(self.size):
				site = self.At(x,y)

				# draw site
				horizontal += ansiColours[site.clusterIndex % maxColours]
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

			lines.append(horizontal)
			lines.append(vertical)

		return AsciiImage(lines)

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
	
	def GenerateClusterImage(self, scale = 1):
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
		
		return image