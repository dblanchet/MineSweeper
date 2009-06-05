import math

import cairo

class MineView(object):

    COVERED = ''
    FLAGGED = 'F'
    DOUBT = '?'
    FALSE = 'X'
    MINE = '*'
    UNCOV_MINE = '$'
    EMPTY = '0'

    def __init__(self):
        self.value = self.COVERED
        self.draw_func = {
                self.COVERED:       self._draw_covered,
                self.FLAGGED:       self._draw_flagged,
                self.DOUBT:         self._draw_doubt,
                self.FALSE:         self._draw_false,
                self.UNCOV_MINE:    self._draw_uncovered_mine,
                self.MINE:          self._draw_exploding_mine,
                self.EMPTY:         self._draw_empty,
                '1':                self._draw_count,
                '2':                self._draw_count,
                '3':                self._draw_count,
                '4':                self._draw_count,
                '5':                self._draw_count,
                '6':                self._draw_count,
                '7':                self._draw_count,
                '8':                self._draw_count
        }

    def set_value(self, value):
        self.value = value

    def draw(self, cr, columns, row, cx, cy):
        self.draw_func[self.value](cr, columns * cx, row * cy, cx)

    def _draw_doubt(self, cr, x, y, w):
        self._draw_covered(cr, x, y, w)

        # Find text size.
        cr.set_font_size(w - 4)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, 
                cairo.FONT_WEIGHT_BOLD)
        width, height = cr.text_extents(self.value)[2:4]
        xoff = (w - width ) / 2
        yoff = (w + height) / 2

        cr.set_source_rgb(0, 0, 0)
        cr.move_to(x + xoff, y + yoff)
        cr.show_text(self.value)

    def _draw_count(self, cr, x, y, w):
        self._draw_empty(cr, x, y, w)

        # Find text size.
        cr.set_font_size(w - 4)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, 
                cairo.FONT_WEIGHT_BOLD)
        width, height = cr.text_extents(self.value)[2:4]
        xoff = (w - width ) / 2
        yoff = (w + height) / 2

        # Choose color.
        colors = [
                None,
                (  0,   0,   1),
                (  0, 0.8,   0),
                (  1,   0,   0),
                (  0,   0, 0.5),
                (0.5,   0,   0),
                (  0, 0.5,   1),
                (  1,   0,   1),
                (  0,   0,   0)
            ]
        cr.set_source_rgb(*colors[int(self.value)])
        cr.move_to(x + xoff, y + yoff)
        cr.show_text(self.value)

    def _draw_empty(self, cr, x, y, w, r=0.9, g=0.9, b=0.9):
        # Background.
        cr.set_source_rgb(r, g, b)
        cr.rectangle(x, y, w, w)
        cr.fill()

        # Boundary.
        cr.set_line_width(1)
        cr.set_source_rgb(0.7, 0.7, 0.7)
        cr.rectangle(x + 0.5, y + 0.5, w - 1, w - 1)
        cr.stroke()

    def _draw_covered(self, cr, x, y, w):
        # Background.
        cr.set_source_rgb(0.7, 0.7, 0.7)
        cr.rectangle(x, y, w, w)
        cr.fill()

        cr.set_line_width(1)

        # Upper left.
        cr.set_source_rgb(0.9, 0.9, 0.9)
        cr.move_to(x + w - 0.5, y + 0.5)
        cr.line_to(x + 0.5 , y + 0.5)
        cr.line_to(x + 0.5, y + w - 0.5)
        cr.stroke()

        # Lower right.
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.move_to(x + 0.5, y + w - 0.5)
        cr.line_to(x + w - 0.5, y + w - 0.5)
        cr.line_to(x + w - 0.5, y + 0.5)
        cr.stroke()

    def _draw_uncovered_mine(self, cr, x, y, w):
        self._draw_empty(cr, x, y, w)
        self._draw_mine(cr, x, y, w)

    def _draw_exploding_mine(self, cr, x, y, w):
        self._draw_empty(cr, x, y, w, 1, 0, 0)
        self._draw_mine(cr, x, y, w)

    def _draw_mine(self, cr, x, y, w):

        # Triggers.
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(w * 0.05)

        cr.move_to(x + w * 0.5, y + w * 0.1)
        cr.line_to(x + w * 0.5, y + w * 0.9)
        cr.stroke()

        cr.move_to(x + w * 0.1, y + w * 0.5)
        cr.line_to(x + w * 0.9, y + w * 0.5)
        cr.stroke()

        cr.move_to(x + w * 0.2, y + w * 0.2)
        cr.line_to(x + w * 0.8, y + w * 0.8)
        cr.stroke()

        cr.move_to(x + w * 0.8, y + w * 0.2)
        cr.line_to(x + w * 0.2, y + w * 0.8)
        cr.stroke()

        # Main circle.
        radial = cairo.RadialGradient(x + w * 0.45, y + w * 0.45, w * 0.05,
                x + w * 0.45, y + w * 0.45, w * 0.25)
        radial.add_color_stop_rgb(0, 0.8, 0.8, 0.8)
        radial.add_color_stop_rgb(1, 0, 0, 0)
        cr.arc(x + w * 0.5, y + w * 0.5,
                w * 0.25,
                0, 2 * math.pi)
        cr.set_source(radial)
        cr.fill()

    def _draw_false(self, cr, x, y, w):
        self._draw_covered(cr, x, y, w)
        self._draw_mine(cr, x, y, w)

        cr.set_source_rgb(1, 0, 0)
        cr.set_line_width(w * 0.075)

        cr.move_to(x + w * 0.1, y + w * 0.9)
        cr.line_to(x + w * 0.9, y + w * 0.1)
        cr.stroke()

        cr.move_to(x + w * 0.9, y + w * 0.9)
        cr.line_to(x + w * 0.1, y + w * 0.1)
        cr.stroke()

    def _draw_flagged(self, cr, x, y, w):
        self._draw_covered(cr, x, y, w)
	self.draw_flag(cr, x, y, w)

    def draw_flag(self, cr, x, y, w):
        # Flag foot.
        cr.set_source_rgb(0, 0, 0)
        t_off = - math.pi * 0.5
        cr.arc(x + w * 0.5, y + w * 1.35,
                w * 0.6,
                t_off - math.pi * 0.25, t_off + math.pi * 0.25)
        cr.close_path()
        cr.fill()

        # Flag pole.
        cr.set_line_width(w * 0.075)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x + w * 0.5, y + w * 0.8)
        cr.line_to(x + w * 0.5, y + w * 0.1)
        cr.stroke()

        # Flag.
        cr.set_source_rgb(1, 0, 0)
        cr.set_line_width(w * 0.025)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.line_to(x + w * 0.1, y + w * 0.3)
        cr.line_to(x + w * 0.5, y + w * 0.5)
        cr.line_to(x + w * 0.5, y + w * 0.1)
        cr.close_path()
        cr.fill_preserve()
        cr.stroke()


if __name__ == '__main__':
    import sys
    try:
        import pygtk
        pygtk.require('2.0')
    except:
        print "This program require PyGtk 2.0."
        sys.exit(1)
    import gtk
    import cairo

    w = gtk.Window(gtk.WINDOW_TOPLEVEL)
    w.set_title('MineSweeper')
    w.connect('destroy', gtk.main_quit)

    d = gtk.DrawingArea()
    d.set_size_request(960, 384)
    w.add(d)

    def draw_all(c, y, size):
        c.set_font_size(size * 0.8)
        c.set_source_rgb(0, 0, 0)
        c.move_to(0, size * y - size * 0.1)
        c.show_text('size: %d pixels' % size)

        lst = [ MineView.COVERED, MineView.FLAGGED, MineView.DOUBT,
                MineView.FALSE, MineView.UNCOV_MINE, MineView.MINE,
                MineView.EMPTY, '1', '2', '3', '4', '5', '6', '7', '8']
        x = 0
        mv = MineView()
        for val in lst:
            mv.set_value(val)
            mv.draw(c, x, y, size, size)

            x += 1

    def draw_samples(obj, widget):
        cr = d.window.cairo_create()
        draw_all(cr, 1, 16)
        draw_all(cr, 2, 24)
        draw_all(cr, 3, 32)
        draw_all(cr, 4, 48)
        draw_all(cr, 5, 64)

    d.connect("expose-event", draw_samples)

    w.show_all()
    gtk.main()

