cdef class Node:
    cdef public double x, y, radius, norm
    cdef public float angle
    cdef float _split_rate, _branch_rate
    cdef float _single_crr, _split_crr, _branch_crr
    cdef float _single_cas, _split_cad, _branch_cad
    cdef float _child_sk, _child_bk
    cpdef list spawn(self)
    cdef list _build_split(self)
    cdef Node _build_left_branch(self)
    cdef Node _build_right_branch(self)
    cdef Node _build_single(self)
    cdef Node _build_child(self, double radius, float angle)
    cpdef double distance(self, Node other)
    cpdef int intersects(self, Node other)
