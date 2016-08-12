from node cimport Node

cdef class NearestNeighborsGrid:
    cdef int _surf_size, _cell_size
    cdef dict _grid
    cpdef list get_addresses(self, Node node)
    cpdef list get_neighbors(self, list addresses)
    cpdef void add(self, Node node)
