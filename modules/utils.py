import math
import random

from node import Node
from root import Root
from neighbors import NearestNeighborsGrid as NNG

def initialize_root_system(
    surf_size,
    cell_size,
    min_rad,
    node_rad,
    bound_rad,
    bound_buff,
    node_num,
    node_kwargs):

    random_th = lambda: (random.random() - 0.5) * 2 * math.pi
    random_x = lambda r: (random.random() - 0.5) * 2 * r
    random_y = lambda r, x: (random.random() - 0.5) * 2 * math.sqrt(r*r - x*x)

    def random_node(buff_rad, node_rad, node_kwargs):
        th = random_th()
        x = random_x(buff_rad)
        y = random_y(buff_rad, x)
        return Node(x, y, node_rad, th, **node_kwargs)

    buff_rad = bound_rad * bound_buff
    min_x = min_y = -surf_size / 2
    max_x = max_y = surf_size / 2
    nodes = [random_node(buff_rad, node_rad, node_kwargs) for _ in xrange(node_num)]
    nngrid = NNG(surf_size, cell_size)

    return Root(nodes, nngrid, bound_rad, min_rad, min_x, max_x, min_y, max_y)

def handle_cli_input(default_kwargs):
    import sys

    kwargs = default_kwargs.copy()
    try:
        f_args = map(lambda f_arg: f_arg.split("="), sys.argv[1:])
        for key, val in f_args:
            assert(key in default_kwargs.keys())
            kwargs[key] = eval(val)

    except (TypeError, AssertionError, ValueError):
        print "Bad usage, using default values."
        kwargs = default_kwargs.copy()

    return kwargs
