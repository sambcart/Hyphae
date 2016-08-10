import cairo

class Render(object):

    def __init__(self, width, height, fill_val, draw_val):
        self.width = width
        self.height = height
        self.size = max(width, height)

        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.ctx = cairo.Context(self.surface)

        self._init_ctx(fill_val, draw_val)

    def _init_ctx(self, fill_val, draw_val):
        fill_color = (fill_val,) * 3
        draw_color = (draw_val,) * 3

        self.ctx.rectangle(0, 0, self.width, self.height)
        self.ctx.set_source_rgb(*fill_color)
        self.ctx.fill()

        self.ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        self.ctx.set_source_rgb(*draw_color)

    def _ctx_stroke(self, line_width):
        self.ctx.set_line_width(line_width)
        self.ctx.stroke()

    def arc(self, cx, cy, rad, th0, th1, line_width):
        self.ctx.arc(cx, cy, rad, th0, th1)
        self._ctx_stroke(line_width)

    def line(self, from_x, from_y, to_x, to_y, line_width):
        self.ctx.move_to(from_x, from_y)
        self.ctx.line_to(to_x, to_y)
        self._ctx_stroke(line_width)

    def curve(self, from_x, from_y, x1, y1, x2, y2, to_x, to_y, line_width):
        self.ctx.move_to(from_x, from_y)
        self.ctx.curve_to(x1, y1, x2, y2, to_x, to_y)
        self._ctx_stroke(line_width)

    def save_png(self, filename, verbose=False):
        if verbose: print "Saving image to {}...".format(filename),
        self.surface.write_to_png(filename)
        if verbose: print "Done."
