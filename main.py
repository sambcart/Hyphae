import math
import time
import random

if __name__ == "__main__":
    from modules.utils import *
    from modules.render import Render

    SURF_SIZE  = 2400
    CELL_SIZE  = 2
    MIN_RAD    = 2
    NODE_RAD   = SURF_SIZE * 0.0035
    BOUND_RAD  = SURF_SIZE * 0.4
    BOUND_BUFF = 0.5
    NODE_NUM   = 3

    DEFAULT_NODE_KWARGS = {
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

    DEFAULT_ROOT_KWARGS = {
        "surf_size": SURF_SIZE,
        "cell_size": CELL_SIZE,
        "min_rad": MIN_RAD,
        "node_rad": NODE_RAD,
        "bound_rad": BOUND_RAD,
        "bound_buff": BOUND_BUFF,
        "node_num": NODE_NUM,
        "node_kwargs": DEFAULT_NODE_KWARGS
    }

    render = Render(SURF_SIZE, SURF_SIZE, 1.0, 0.15)
    root = initialize_root_system(**DEFAULT_ROOT_KWARGS)

    try:
        tic = time.time()
        root.generate()
        toc = time.time()

        print "Simulation took %.3f sec" % (toc - tic)

        tic = time.time()
        render.draw_root(root)
        toc = time.time()

        print "Drawing took %.3f sec" % (toc - tic)
        render.save_png("img/hyphae-{}.png".format(int(time.time())), verbose=True)

    except KeyboardInterrupt as e:
        print "Keyboard Interruption:"
        render.save_png("img/hyphae-{}.png".format(int(time.time())), verbose=True)
