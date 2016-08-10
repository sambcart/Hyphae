import math
import time

if __name__ == "__main__":
    from modules.utils import *
    from modules.node import Node
    from modules.root import Root
    from modules.render import Render
    from modules.collision import CollisionDetectionGrid as CDG

    size = 8000
    render = Render(size, size, 0.15, 1.0)

    default_node_kwargs = {
        "pos": (0, 0),
        "radius": size * 0.0125,
        "angle": math.pi / 2,
        "split_rate": 0.35,
        "branch_rate": 0.05,
        "single_child_rad_rat": 0.99,
        "split_child_rad_rat": 0.94,
        "branch_child_rad_rat": 0.75,
        "single_child_angle_sigma": math.pi / 12,
        "split_child_angle_dev": math.pi / 6,
        "branch_child_angle_dev": math.pi / 3,
        "child_split_k": 1.05,
        "child_branch_k": 1.075
    }

    node_kwargs = handle_cli_input(default_node_kwargs)

    default_node = Node(**node_kwargs)
    default_cdg = CDG(size, default_node.radius)

    root_kwargs = {
        "node": default_node,
        "min_rad": 8,
        "boundary_rad": size * 0.4,
        "min_x": -size/2,
        "max_x":  size/2,
        "min_y": -size/2,
        "max_y":  size/2,
        "cdg": default_cdg
    }

    root = Root(**root_kwargs)
    root.generate()
    root.draw(render)

    render.save_png("hyphae-{}.png".format(int(time.time())))
