import random
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
					if east not in s.neighbours:
						s.neighbours.append(east)
						east.neighbours.append(s)                
			# vertical edges
			if s.y < size - 1:
				if random.random() < self.p:
					south = self.At(s.x, s.y + 1)
					if south not in s.neighbours:
						s.neighbours.append(south)
						south.neighbours.append(s)

	def At(self, x,y):
		return self.sites[y * self.size + x]
	
	# print ascii display of grid (highlights a spanning path, if one is found)
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
					if (site in self.At(x+1, y).neighbours):
						horizontal += "－"
					else:
						horizontal += "  "
				if y < self.size - 1:
					if (site in self.At(x, y+1).neighbours):
						vertical += "｜"
					else:
						vertical += "  "
				vertical += "  "
			print(horizontal)
			print(vertical)