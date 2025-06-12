

# contains per-vertex data
class Site:
    def __init__(self, x, y):
        # planar coordinates
        self.x = x
        self.y = y
        # list of neighbouring sites
        self.neighbours = []
        # flags used in FloodFill 
        self.added = False
        self.checked = False
        self.parent = None
        self.marked = False