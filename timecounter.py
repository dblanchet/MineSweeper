import pygtk
pygtk.require('2.0')
import gtk
import cairo

import gobject

import time

class TimeCounter(gtk.DrawingArea):

    __gsignals__ = {
            "expose-event" : "override"
        }

    def __init__(self, height):
        gtk.DrawingArea.__init__(self)
        self.set_size_request(5 * height, height)
        self.height = height
        self.elapsed = 0
        self.timeout_id = -1

    def do_expose_event(self, widget):
        cr = widget.window.cairo_create()
        
        # Counter.
        t = time.localtime(int(self.elapsed))
        text = time.strftime("%M:%S", t)

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

    def _update_time(self, msg=None):
        self.elapsed += 1
        self.queue_draw()
        return True

    def start(self):
        self.timeout_id = gobject.timeout_add(1000, self._update_time)

    def stop(self):
        if self.timeout_id > 0:
            gobject.source_remove(self.timeout_id)
            self.timeout_id = -1

    def reset(self):
        self.stop()
        self.elapsed = 0
        self.queue_draw()

