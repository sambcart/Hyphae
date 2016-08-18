
def main():
    global SURF_SIZE, CELL_SIZE, MIN_RAD, NODE_RAD, BOUND_RAD, BOUND_BUFF, NODE_NUM
    global DEFAULT_NODE_KWARGS, DEFAULT_ROOT_KWARGS
    global NODE_X, NODE_Y, NODE_TH

    # Width/height of final image (in pixels)
    SURF_SIZE = 2400

    # Size of cell in nearest-neighbors grid (in pixels)
    CELL_SIZE = 2

    # Minimum node radius allowed (in pixels)
    MIN_RAD = 12

    # Radius of initial node(s)
    NODE_RAD = SURF_SIZE * 0.025

    # Radius of boundary circle
    BOUND_RAD = SURF_SIZE * 0.4

    # During initialization of the root, only nodes inside
    # the radius of BOUND_RAD * BOUND_BUFF will be created.
    # This ensures that the first few nodes aren't too close
    # to the boundary.
    BOUND_BUFF = 0.5

    # Number of initial nodes; if greater than one, the root
    # system will be composed of multiple roots.
    NODE_NUM = 1


    """
    NO SPLIT OR BRANCH (ie. SINGLE CHILD)
    (1)     |
    (2)     |

    SPLIT
    (1)     |
    (2)    / \

    BRANCH
    (1)     |
    (2)    /|

    or

    (1)     |
    (2)     |\

    or

    (1)     |
    (2)    /|\
    """


    # split_rate:                Probability that a node splits next iteration
    # branch_rate:               Probability that a node branches next iteration
    # single_child_rad_rat:      Ratio of single child's radius to parent's radius
    # split_child_rad_rat:       Ratio of split child's radius to parent's radius
    # branch_child_rad_rat:      Ratio of branch child's radius to parent's radius
    # single_child_angle_sigma:  Single child's random (standard) deviation from parent's direction of travel
    # split_child_angle_dev:     Split child's constant angular deviation from parent's direction of travel
    # branch_child_angle_dev:    Branch child's constant angular deviation from parent's direction of travel
    # child_split_k:             Ratio of child's splitting probability and parent's splitting probability
    # child_branch_k:            Ratio of child's branching probability and parent's branching probability

    DEFAULT_NODE_KWARGS = {
        "split_rate": 0.20,
        "branch_rate": 0.10,
        "single_child_rad_rat": 0.95,
        "split_child_rad_rat": 0.925,
        "branch_child_rad_rat": 0.85,
        "single_child_angle_sigma": math.pi / 18,
        "split_child_angle_dev": math.pi / 6,
        "branch_child_angle_dev": math.pi / 3,
        "child_split_k": 1.0075,
        "child_branch_k": 1.0075
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

    # x,y-position of initial node
    NODE_X  = 0
    NODE_Y  = BOUND_RAD - NODE_RAD

    # Direction of travel of initial node
    NODE_TH = math.pi * 1.5

    render = Render(SURF_SIZE, SURF_SIZE, 1.0, 0.15)
    root = initialize_root_system(node_x=NODE_X,
                                  node_y=NODE_Y,
                                  node_th=NODE_TH,
                                  **DEFAULT_ROOT_KWARGS)

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

if __name__ == "__main__":
    import math
    import time

    from modules.utils import *
    from modules.render import Render

    main()
