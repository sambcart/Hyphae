import itertools

class CollisionDetectionGrid(object):

    def __init__(self, size, max_rad):
        self.surf_size = size
        self.cell_size = int(2 * max_rad)
        self.grid = {}

        p = size / self.cell_size + 1
        for i, j in itertools.product(xrange(-1,p+1), repeat=2):
            self.grid[i, j] = []

    def address_node(self, node):
        xi = (int(node.x) + self.surf_size / 2) / self.cell_size
        yi = (int(node.y) + self.surf_size / 2) / self.cell_size
        for dx, dy in itertools.product([-1,0,1], repeat=2):
            if (xi + dx, yi + dy) in self.grid:
                yield (xi + dx, yi + dy)

    def add(self, node):
        for address in self.address_node(node):
            self.grid[address].append(node)

    def get_neighbors(self, addresses):
        for address in addresses:
            for neighbor in self.grid[address]:
                yield neighbor
