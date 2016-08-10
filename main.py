import math
import random
import time

if __name__ == "__main__":
    from modules.utils import *
    from modules.node import Node
    from modules.root import Root
    from modules.render import Render
    from modules.collision import CollisionDetectionGrid as CDG

    size = 4000
    init_rad = 20
    boundary_rad = 1600
    node_num = 5

    render = Render(size, size, 1.0, 0.15)

    node_kwargs = lambda: {
        "pos": random_point_rad(boundary_rad, 0.8),
        "angle": random_angle(),
        "radius": init_rad,
        "split_rate": 0.25,
        "branch_rate": 0.25,
        "single_child_rad_rat": 0.98,
        "split_child_rad_rat": 0.96,
        "branch_child_rad_rat": 0.75,
        "single_child_angle_sigma": math.pi / 12,
        "split_child_angle_dev": math.pi / 6,
        "branch_child_angle_dev": math.pi / 3,
        "child_split_k": 1.025,
        "child_branch_k": 1.01
    }

    default_cdg = CDG(size, init_rad)

    root_kwargs = {
        "nodes": [Node(**node_kwargs()) for _ in xrange(node_num)],
        "min_rad": 1,
        "boundary_rad": boundary_rad,
        "min_x": -size/2,
        "max_x":  size/2,
        "min_y": -size/2,
        "max_y":  size/2,
        "cdg": default_cdg
    }

    root = Root(**root_kwargs)

    try:
        root.generate_frames(render)

        #root.generate()
        #root.draw(render)
        #render.save_png("img/hyphae-{}.png".format(int(time.time())), verbose=True)

    except KeyboardInterrupt:
        root.draw(render)
        render.save_png("img/hyphae-{}.png".format(int(time.time())), verbose=True)
