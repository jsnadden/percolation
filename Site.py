

# contains per-vertex data
class Site:
    def __init__(self, x, y):
        # grid data (position and graph adjacencies)
        self.x = x
        self.y = y
        self.east = None
        self.north = None
        self.west = None
        self.south = None

        # data for cluster analysis
        self.onPath = False
        self.parent = None
        self.clusterIndex = -1

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