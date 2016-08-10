from node import Node
from render import Render
from utils import *

class Root(object):

    def __init__(self, nodes, min_rad, boundary_rad, min_x, max_x, min_y, max_y, nngrid):

        self.nngrid = nngrid
        self.node_batch = []
        self.edge_set = []

        for node in nodes:
            self.nngrid.add(node)
            self.node_batch.append(node)

        self.min_rad = min_rad
        self.boundary_rad = boundary_rad
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def check_node(self, node):
        if node.radius < self.min_rad:
            return False

        if self.boundary_rad and node.norm + node.radius > self.boundary_rad:
            return False

        elif node.x - node.radius < self.min_x or node.x + node.radius > self.max_x:
            return False

        elif node.y - node.radius < self.min_y or node.y + node.radius > self.max_y:
            return False

        addresses = self.nngrid.address_node(node)
        for neighbor in self.nngrid.get_neighbors(addresses):
            if node.intersects(neighbor):
                return False

        return True

    def generate(self):
        while self.node_batch:
            print len(self.node_batch)
            temp_node_batch = []
            for node in self.node_batch:
                for other in node.spawn():
                    if self.check_node(other):
                        self.nngrid.add(other)
                        self.edge_set.append((node, other))
                        temp_node_batch.append(other)
            self.node_batch = temp_node_batch[:]

    def generate_frames(self, render):
        import time
        import os
        import sys

        img_dir = "img/hyphae-{}".format(int(time.time()))

        try:
            print "Creating folder named {}...".format(img_dir)
            time.sleep(2)
            print "Press <Ctrl>-C to cancel..."
            print "3",
            time.sleep(1)
            print "2",
            time.sleep(1)
            print "1",
            time.sleep(1)
            os.mkdir(img_dir)
            print "Done."

        except KeyboardInterrupt:
            print "Exiting."
            sys.exit()

        frame_count = 0

        while self.node_batch:
            print len(self.node_batch)
            temp_node_batch = []
            for node in self.node_batch:
                for other in node.spawn():
                    if self.check_node(other):
                        self.nngrid.add(other)
                        temp_node_batch.append(other)
                        self.draw_edge(node, other, render)
            render.save_png(img_dir + "/hyphae-{}.png".format(frame_count), verbose=False)
            self.node_batch = temp_node_batch[:]
            frame_count += 1

    def draw_edge(self, node0, node1, render):
        x0 =  node0.x + render.width / 2
        y0 = -node0.y + render.height / 2
        x1 =  node1.x + render.width / 2
        y1 = -node1.y + render.height / 2
        render.line(x0, y0, x1, y1, node1.radius)

    def draw(self, render):
        for node0, node1 in self.edge_set:
            self.draw_edge(node0, node1, render)
