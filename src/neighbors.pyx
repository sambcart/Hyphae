cimport cython

from node cimport Node

cdef class NearestNeighborsGrid:

    def __init__(self, int size, int cell_size):
        self._surf_size = size
        self._cell_size = cell_size
        self._grid = {}

        cdef int p = int(size / cell_size) + 1
        cdef int i, j

        for i in xrange(-1, p+1):
            for j in xrange(-1, p+1):
                self._grid[i, j] = []

    @cython.boundscheck(False)
    cpdef list get_addresses(self, Node node):
        cdef list addresses = []
        cdef int i, j

        cdef int min_x = int(node.x - node.radius + self._surf_size / 2) / self._cell_size
        cdef int max_x = int(node.x + node.radius + self._surf_size / 2) / self._cell_size
        cdef int min_y = int(node.y - node.radius + self._surf_size / 2) / self._cell_size
        cdef int max_y = int(node.y + node.radius + self._surf_size / 2) / self._cell_size

        for i in xrange(min_x, max_x+1):
            for j in xrange(min_y, max_y+1):
                addresses.append( (i, j) )

        return addresses

    @cython.boundscheck(False)
    cpdef list get_neighbors(self, list addresses):
        cdef int i, j
        cdef Node neighbor
        cdef list neighbors = []

        for (i, j) in addresses:
            for neighbor in self._grid[i, j]:
                neighbors.append( neighbor )

        return neighbors

    @cython.boundscheck(False)
    cpdef void add(self, Node node):
        cdef int i, j
        cdef list addresses = self.get_addresses(node)

        for (i, j) in addresses:
            self._grid[i, j].append( node )
