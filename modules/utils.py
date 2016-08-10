import math
import random

def loc_gamma(a, b, c):
    return math.acos((c*c - a*a - b*b) / (-2.*a*b))

def loc_c(a, b, gamma):
    return math.sqrt(a*a + b*b - 2*a*b*math.cos(gamma))

def random_point_rad(rad, buffer):
    x = random.randint(-rad * buffer, rad * buffer)
    ymax = int(math.sqrt(buffer * buffer * rad * rad - x * x))
    ymin = -ymax
    y = random.randint(ymin, ymax)
    return (x, y)

def random_angle():
    return random.random() * 2 * math.pi

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
