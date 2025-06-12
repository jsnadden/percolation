

# contains per-vertex data
class Site:
    def __init__(self, x, y):
        # planar coordinates
        self.x = x
        self.y = y

        # list of neighbouring sites
        self.east = None
        self.north = None
        self.west = None
        self.south = None

        # flags used in FloodFill 
        self.added = False
        self.checked = False
        self.parent = None
        self.marked = False

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