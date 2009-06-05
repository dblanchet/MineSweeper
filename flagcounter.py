import pygtk
pygtk.require('2.0')
import gtk
import cairo

from mineview import MineView

class FlagCounter(gtk.DrawingArea):

    __gsignals__ = {
            "expose-event" : "override"
	}

    def __init__(self, count, height):
	gtk.DrawingArea.__init__(self)
	self.set_size_request(3 * height, height)
	self.count = count
	self.height = height

    def do_expose_event(self, widget):
	cr = widget.window.cairo_create()
	
	# Flag.
	c = MineView()
	c.draw_flag(cr, 0, 0, self.height)

	# Counter.
	text = str(self.count)

	cr.set_font_size(self.height * 0.9)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, 
                cairo.FONT_WEIGHT_BOLD)
        width, height = cr.text_extents(text)[2:4]
        
	w = self.height
	xoff = (2 * w - width ) / 2
        yoff = (w + height) / 2

	if self.count < 0:
	    cr.set_source_rgb(1, 0, 0)
	else:
	    cr.set_source_rgb(0, 0, 0)
        cr.move_to(w + xoff, yoff)
        cr.show_text(text)

    def set_value(self, value):
	self.count = value
	self.queue_draw()

