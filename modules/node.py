import math
import random

class Node(object):

    def __init__(
        self,
        pos,
        radius,
        angle,
        split_rate,
        branch_rate,
        single_child_rad_rat,
        split_child_rad_rat,
        branch_child_rad_rat,
        single_child_angle_sigma,
        split_child_angle_dev,
        branch_child_angle_dev,
        child_split_k,
        child_branch_k):

        self.x, self.y = self.pos = pos
        self.radius = radius
        self.angle = angle
        self.split_rate = split_rate
        self.branch_rate = branch_rate

        self._single_crr = single_child_rad_rat
        self._split_crr = split_child_rad_rat
        self._branch_crr = branch_child_rad_rat
        self._single_cas = single_child_angle_sigma
        self._split_cad = split_child_angle_dev
        self._branch_cad = branch_child_angle_dev
        self._child_sk = child_split_k
        self._child_bk = child_branch_k

        if split_rate + branch_rate > 1:
            self.split_rate = float(split_rate) / (split_rate + branch_rate)
            self.branch_rate = float(branch_rate) / (split_rate + branch_rate)

        """
        if single_child_rad_rat > 1:
            self._single_crr = 0.99

        if split_child_rad_rat > 1:
            self._split_crr = 0.94

        if branch_child_rad_rat > 1:
            self._branch_crr = 0.75

        if single_child_angle_sigma > math.pi:
            self._single_cas = math.pi / 12

        if split_child_angle_dev > math.pi:
            _rad = self.radius * self._split_crr
            a = self.radius + _rad
            c = _rad + _rad + 1
            self._split_cad = loc_gamma(a, a, c) / 2.

        if branch_child_angle_dev > math.pi:
            self._branch_cad = math.pi / 3
        """

        self.consts = {
            "single_child_rad_rat": self._single_crr,
            "split_child_rad_rat": self._split_crr,
            "branch_child_rad_rat": self._branch_crr,
            "single_child_angle_sigma": self._single_cas,
            "split_child_angle_dev": self._split_cad,
            "branch_child_angle_dev": self._branch_cad,
            "child_split_k": self._child_sk,
            "child_branch_k": self._child_bk
        }

    def spawn(self):
        if random.random() < self.split_rate:
            ch0, ch1 = self._build_split()
            yield ch0
            yield ch1

        else:
            yield self._build_single()

            if random.random() < self.branch_rate:
                yield self._build_left_branch()

            if random.random() < self.branch_rate:
                yield self._build_right_branch()

    def _build_split(self):
        radius = self.radius * self._split_crr
        angle_l = self.angle + self._split_cad
        angle_r = self.angle - self._split_cad
        return [self._build_child(radius, angle_l),
                self._build_child(radius, angle_r)]

    def _build_left_branch(self):
        radius = self.radius * self._branch_crr
        angle = self.angle + self._branch_cad
        return self._build_child(radius, angle)

    def _build_right_branch(self):
        radius = self.radius * self._branch_crr
        angle = self.angle - self._branch_cad
        return self._build_child(radius, angle)

    def _build_single(self):
        radius = self.radius * self._single_crr
        angle = self.angle + random.gauss(0, self._single_cas)
        return self._build_child(radius, angle)

    def _build_child(self, radius, angle):
        x = self.x + (self.radius + radius) * math.cos(angle)
        y = self.y + (self.radius + radius) * math.sin(angle)
        split_rate = self.split_rate * self._child_sk
        branch_rate = self.branch_rate * self._child_bk
        return Node((x, y), radius, angle, split_rate, branch_rate, **self.consts)

    @staticmethod
    def norm(node):
        return math.sqrt(node.x*node.x + node.y*node.y)

    @staticmethod
    def distance(node1, node2):
        dx = node1.x - node2.x
        dy = node1.y - node2.y
        return math.sqrt(dx*dx + dy*dy)

    @staticmethod
    def intersect(node1, node2):
        return Node.distance(node1, node2) <= node1.radius + node2.radius - 1
