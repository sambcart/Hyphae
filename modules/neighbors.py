import itertools

class NearestNeighborsGrid(object):

    def __init__(self, size, max_rad):
        self.surf_size = size
        self.cell_size = int(2 * max_rad)
        self.grid = {}

        p = size / self.cell_size + 1
        for i, j in itertools.product(xrange(-1,p+1), repeat=2):
            self.grid[i, j] = []

    def address_node(self, node):
        xmin = int(node.x - node.radius + self.surf_size / 2.) / self.cell_size
        xmax = int(node.x + node.radius + self.surf_size / 2.) / self.cell_size
        ymin = int(node.y - node.radius + self.surf_size / 2.) / self.cell_size
        ymax = int(node.y + node.radius + self.surf_size / 2.) / self.cell_size
        return itertools.product(range(xmin, xmax+1), range(ymin, ymax+1))

    def add(self, node):
        for address in self.address_node(node):
            self.grid[address].append(node)

    def get_neighbors(self, addresses):
        for address in addresses:
            for neighbor in self.grid[address]:
                yield neighbor
