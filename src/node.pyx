cimport cython

from libc.math cimport cos
from libc.math cimport sin
from libc.math cimport sqrt

import random

cdef class Node:

    @cython.cdivision(True)
    def __init__(self,
                 double x,
                 double y,
                 double radius,
                 float angle,
                 float split_rate,
                 float branch_rate,
                 float single_child_rad_rat,
                 float split_child_rad_rat,
                 float branch_child_rad_rat,
                 float single_child_angle_sigma,
                 float split_child_angle_dev,
                 float branch_child_angle_dev,
                 float child_split_k,
                 float child_branch_k):

        self.x = x
        self.y = y
        self.radius = radius
        self.norm = sqrt(self.x * self.x + self.y * self.y)
        self.angle = angle

        self._split_rate = split_rate
        self._branch_rate = branch_rate
        self._single_crr = single_child_rad_rat
        self._split_crr = split_child_rad_rat
        self._branch_crr = branch_child_rad_rat
        self._single_cas = single_child_angle_sigma
        self._split_cad = split_child_angle_dev
        self._branch_cad = branch_child_angle_dev
        self._child_sk = child_split_k
        self._child_bk = child_branch_k

        if split_rate + branch_rate > 1:
            self._split_rate = split_rate / (split_rate + branch_rate)
            self._branch_rate = branch_rate / (split_rate + branch_rate)

    cpdef list spawn(self):
        cdef float r_split = random.random()
        cdef float r_branch_l = random.random()
        cdef float r_branch_r = random.random()

        cdef list children = []

        if r_split < self._split_rate:
            children.extend( self._build_split() )

        else:
            children.append( self._build_single() )

            if r_branch_l < self._branch_rate:
                children.append( self._build_left_branch() )

            if r_branch_r < self._branch_rate:
                children.append( self._build_right_branch() )

        return children

    cdef list _build_split(self):
        cdef double radius = self.radius * self._split_crr
        cdef float angle_l = self.angle + self._split_cad
        cdef float angle_r = self.angle - self._split_cad
        cdef Node csp_l = self._build_child(radius, angle_l)
        cdef Node csp_r = self._build_child(radius, angle_r)
        return [ csp_l, csp_r ]

    cdef Node _build_left_branch(self):
        cdef double radius = self.radius * self._branch_crr
        cdef float angle = self.angle + self._branch_cad
        return self._build_child(radius, angle)

    cdef Node _build_right_branch(self):
        cdef double radius = self.radius * self._branch_crr
        cdef float angle = self.angle - self._branch_cad
        return self._build_child(radius, angle)

    cdef Node _build_single(self):
        cdef double radius = self.radius * self._single_crr
        cdef float angle_dev = random.gauss(0, self._single_cas)
        cdef float angle = self.angle + angle_dev
        return self._build_child(radius, angle)

    cdef Node _build_child(self, double radius, float angle):
        cdef double x = self.x + (self.radius + radius) * cos(angle)
        cdef double y = self.y + (self.radius + radius) * sin(angle)
        cdef float split_rate = self._split_rate * self._child_sk
        cdef float branch_rate = self._branch_rate * self._child_bk
        return Node(x,
                    y,
                    radius,
                    angle,
                    split_rate,
                    branch_rate,
                    self._single_crr,
                    self._split_crr,
                    self._branch_crr,
                    self._single_cas,
                    self._split_cad,
                    self._branch_cad,
                    self._child_sk,
                    self._child_bk,)

    cpdef double distance(self, Node other):
        cdef double dx = self.x - other.x
        cdef double dy = self.y - other.y
        return sqrt(dx*dx + dy*dy)

    cpdef int intersects(self, Node other):
        cdef double dx = self.x - other.x
        cdef double dy = self.y - other.y
        cdef double dist = sqrt(dx*dx + dy*dy)
        if dist <= self.radius + other.radius - 1:
            return 1
        return 0
