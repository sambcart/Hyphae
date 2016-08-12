from node cimport Node
from neighbors cimport NearestNeighborsGrid as NNG

cdef class Root:
    cdef public list edge_set
    cdef NNG _nngrid
    cdef list _node_batch
    cdef double _bound_rad, _min_rad, _min_x, _max_x, _min_y, _max_y
    cdef int _check_node(self, Node node)
    cdef list _iterate(self)
    cpdef void generate(self)
