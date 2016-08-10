import math
import random
import time

if __name__ == "__main__":
    from modules.utils import *
    from modules.node import Node
    from modules.root import Root
    from modules.render import Render
    from modules.neighbors import NearestNeighborsGrid as NNG

    SURF_SIZE = 2000
    INIT_RAD  = SURF_SIZE * 0.0035
    BOUND_RAD = SURF_SIZE * 0.4
    NODE_NUM  = 8

    render = Render(SURF_SIZE, SURF_SIZE, 1.0, 0.15)

    node_kwargs = lambda: {
        "pos": random_point_rad(BOUND_RAD, 0.6),
        "angle": random_angle(),
        "radius": INIT_RAD,
        "split_rate": 0.25,
        "branch_rate": 0.25,
        "single_child_rad_rat": 0.99,
        "split_child_rad_rat": 0.97,
        "branch_child_rad_rat": 0.95,
        "single_child_angle_sigma": math.pi / 12,
        "split_child_angle_dev": math.pi / 6,
        "branch_child_angle_dev": math.pi / 3,
        "child_split_k": 1.025,
        "child_branch_k": 1.025
    }

    nngrid = NNG(SURF_SIZE, INIT_RAD)

    root_kwargs = {
        "nodes": [Node(**node_kwargs()) for _ in xrange(NODE_NUM)],
        "min_rad": 1,
        "boundary_rad": BOUND_RAD,
        "min_x": -SURF_SIZE/2,
        "max_x":  SURF_SIZE/2,
        "min_y": -SURF_SIZE/2,
        "max_y":  SURF_SIZE/2,
        "nngrid": nngrid
    }

    root = Root(**root_kwargs)

    try:
        #root.generate_frames(render)

        tic = time.time()
        root.generate()
        toc = time.time()
        root.draw(render)
        tac = time.time()
        print "Simulation took %.3f sec" % (toc - tic)
        print "Drawing took %.3f sec" % (tac - toc)
        render.save_png("img/hyphae-{}.png".format(int(time.time())), verbose=True)

    except KeyboardInterrupt as e:
        print e
        root.draw(render)
        render.save_png("img/hyphae-{}.png".format(int(time.time())), verbose=True)
