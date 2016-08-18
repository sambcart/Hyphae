from node cimport Node
from neighbors cimport NearestNeighborsGrid as NNG

cdef class Root:

    def __init__(self, list nodes, NNG nngrid, double bound_rad, double min_rad, double min_x, double max_x, double min_y, double max_y):

        self.edge_set = []

        self._nngrid = nngrid
        self._node_batch = []

        cdef Node node

        for node in nodes:
            self._nngrid.add( node )
            self._node_batch.append( node )

        self._bound_rad = bound_rad
        self._min_rad = min_rad
        self._min_x = min_x
        self._max_x = max_x
        self._min_y = min_y
        self._max_y = max_y

    cdef int _check_node(self, Node node):
        if node.radius < self._min_rad:
            return 0

        if self._bound_rad and node.norm + node.radius > self._bound_rad:
            return 0

        elif node.x - node.radius < self._min_x or node.x + node.radius > self._max_x:
            return 0

        elif node.y - node.radius < self._min_y or node.y + node.radius > self._max_y:
            return 0

        cdef Node neighbor
        cdef list addresses = self._nngrid.get_addresses(node)
        cdef list neighbors = self._nngrid.get_neighbors(addresses)

        for neighbor in neighbors:
            if node.intersects(neighbor):
                return 0

        return 1

    cdef list _iterate(self):
        cdef list temp_node_batch = []
        cdef Node node, other

        for node in self._node_batch:
            for other in node.spawn():
                if self._check_node(other):
                    self._nngrid.add(other)
                    self.edge_set.append((node, other))
                    temp_node_batch.append(other)

        return temp_node_batch

    cpdef void generate(self):
        while self._node_batch:
            self._node_batch = self._iterate()
