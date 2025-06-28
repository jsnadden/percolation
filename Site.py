

# contains per-vertex data
class Site:
    def __init__(self, x, y):
        # position in grid
        self.x = x
        self.y = y

        # neighbours
        self.east = None
        self.north = None
        self.west = None
        self.south = None

        # graph-theoretic data
        self.clusterIndex = -1
        self.eccentricity = 0

        # auxilliary data for search algorithms
        self.flag = False
        self.flag2 = False
        self.parent = None


    def Neighbour(self, index):
        index = index % 4

        if index == 0:
            return self.east
        elif index == 1:
            return self.north
        elif index == 2:
            return self.west
        elif index == 3:
            return self.south
        else:
            return None
    
    def TileIndex(self):
         sum = 0
         for i in range(4):
              if self.Neighbour(i) is not None:
                   sum += 2**i
         return sum