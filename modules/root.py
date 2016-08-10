from node import Node
from render import Render
from utils import *

class Root(object):

    def __init__(
        self,
        node,
        min_rad,
        boundary_rad,
        min_x,
        max_x,
        min_y,
        max_y,
        cdg):

        self.cdg = cdg
        self.cdg.add(node)

        self.min_rad = min_rad
        self.boundary_rad = boundary_rad
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        self.node_batch = [node]
        self.node_set = [node]
        self.edge_set = []

    def check_node(self, node):
        if node.radius < self.min_rad:
            return False

        if self.boundary_rad and Node.norm(node) + node.radius > self.boundary_rad:
            return False

        elif node.x - node.radius < self.min_x or node.x + node.radius > self.max_x:
            return False

        elif node.y - node.radius < self.min_y or node.y + node.radius > self.max_y:
            return False

        addresses = self.cdg.address_node(node)
        for neighbor in self.cdg.get_neighbors(addresses):
            if Node.intersect(node, neighbor):
                return False

        return True

    def generate(self):
        while self.node_batch:
            temp_node_batch = []
            for node in self.node_batch:
                for other in node.spawn():
                    if self.check_node(other):
                        self.cdg.add(other)
                        self.edge_set.append((node, other))
                        temp_node_batch.append(other)
            self.node_batch = temp_node_batch[:]
            self.node_set.extend(temp_node_batch)

    def draw_edge(self, node0, node1, render):
        x0 =  node0.x + render.width / 2
        y0 = -node0.y + render.height / 2
        x1 =  node1.x + render.width / 2
        y1 = -node1.y + render.height / 2
        render.line(x0, y0, x1, y1, node0.radius)

    def draw(self, render):
        for node0, node1 in self.edge_set:
            self.draw_edge(node0, node1, render)
