import pygtk
pygtk.require('2.0')
import gtk
import cairo

class TimeCounter(gtk.DrawingArea):

    __gsignals__ = {
            "expose-event" : "override"
	}

    def __init__(self, height):
	gtk.DrawingArea.__init__(self)
	self.set_size_request(5 * height, height)
	self.height = height

    def do_expose_event(self, widget):
	cr = widget.window.cairo_create()
	
	# Counter.
	text = str("00:00")

	cr.set_font_size(self.height * 0.9)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, 
                cairo.FONT_WEIGHT_BOLD)
        width, height = cr.text_extents(text)[2:4]
        
	w = self.height
	xoff = (2 * w - width ) / 2
        yoff = (w + height) / 2

	cr.set_source_rgb(0, 0, 0)
        cr.move_to(w + xoff, yoff)
        cr.show_text(text)

    def start(self):
	pass

    def stop(self):
	pass

    def reset(self):
	pass

