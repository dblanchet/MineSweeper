import pygtk
pygtk.require('2.0')
import gtk

import gobject

from mineview import MineView

class MineFieldView(gtk.DrawingArea):

    __gsignals__ = {
            "expose-event" : "override",
            "explosion" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
            "started" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
            "done" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
            "flagged" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_INT,))
        }

    def __init__(self, minefield):
        gtk.DrawingArea.__init__(self)
        self.cellsize = 32
        
        self.set_minefield(minefield)

        self.connect("button_release_event", self.on_button_release_event)
        self.set_events(  gtk.gdk.EXPOSURE_MASK
                        | gtk.gdk.LEAVE_NOTIFY_MASK
                        | gtk.gdk.BUTTON_RELEASE_MASK)

    def set_minefield(self, minefield):
        self.minefield = minefield
        self.columns, self.rows = minefield.size()

        self.cells = [[MineView() for i in range(self.rows)] 
                                  for j in range(self.columns)]

        self.set_size_request(self.columns * self.cellsize,
                self.rows * self.cellsize)
        self.finished = False
        self.started = False
        self.flagged = 0
        self.uncovered = self.columns * self.rows

        self.queue_draw()

    def do_expose_event(self, widget):
        self.cr = self.window.cairo_create()
        for i in range(self.columns):
            for j in range(self.rows):
                c = self.cells[i][j]
                c.draw(self.cr, i, j, self.cellsize, self.cellsize)

    def _uncover_empty(self, column, row):

        if column < 0: return
        if row < 0: return
        if column >= self.columns: return
        if row >= self.rows: return

        val = self.minefield.get_cell(column, row)
        cell = self.cells[column][row]

        if cell.value == MineView.COVERED:
            self.cells[column][row].set_value(val)
	    self.uncovered -= 1
        else:
            return

        if val != MineView.EMPTY:
            return

        self._uncover_empty(column - 1, row)
        self._uncover_empty(column, row - 1)

        self._uncover_empty(column + 1, row)
        self._uncover_empty(column, row + 1)

        self._uncover_empty(column - 1, row - 1)
        self._uncover_empty(column + 1, row - 1)

        self._uncover_empty(column - 1, row + 1)
        self._uncover_empty(column + 1, row + 1)

    def _flag_unflagged(self):
        for i in range(self.columns):
            for j in range(self.rows):
                cell = self.cells[i][j]
		if self.minefield.get_cell(i, j) == MineView.MINE \
			and cell.value == MineView.COVERED:
		    cell.set_value(MineView.FLAGGED)
		    self.flagged += 1
	self.emit("flagged", self.flagged)
	self.queue_draw()

    def _uncover_mine(self):
        self.finished = True
        self.emit("explosion")
        for i in range(self.columns):
            for j in range(self.rows):
                cell = self.cells[i][j]
                
                val = self.minefield.get_cell(i, j)
                disp = cell.value

                if val == MineView.MINE and disp != MineView.MINE and disp != MineView.FLAGGED:
                    cell.set_value(MineView.UNCOV_MINE)
                elif val != MineView.MINE and disp == MineView.FLAGGED:
                    cell.set_value(MineView.FALSE)
    
    def _check_cell(self, column, row):
        c = self.cells[column][row]
        if c.value == MineView.COVERED:
            val = self.minefield.get_cell(column, row)
            if val == MineView.EMPTY:
                self._uncover_empty(column, row)
            elif val == MineView.MINE:
                # Boom!
                self._uncover_mine()
                c.set_value(val)
            else:
                c.set_value(val)
		self.uncovered -= 1
            self.queue_draw()
        elif c.value == MineView.FLAGGED:
            c.set_value(MineView.DOUBT)
            self.flagged -= 1
            self.emit("flagged", self.flagged)
            self.queue_draw()
        elif c.value == MineView.DOUBT:
            c.set_value(MineView.COVERED)
            self.queue_draw()
    
    def _flag_cell(self, column, row):
        c = self.cells[column][row]
        if c.value == MineView.COVERED:
            c.set_value(MineView.FLAGGED)
            self.flagged += 1
            self.emit("flagged", self.flagged)
        elif c.value == MineView.FLAGGED:
            self.flagged -= 1
            self.emit("flagged", self.flagged)
            c.set_value(MineView.DOUBT)
        elif c.value == MineView.DOUBT:
            c.set_value(MineView.COVERED)
        self.queue_draw()

    def on_button_release_event(self, widget, event):
        if self.finished:
            return

        if not self.started:
            self.emit("started")
            self.started = True

        x = event.x
        y = event.y

        row = int(y / self.cellsize)
        column = int(x / self.cellsize)
        button = event.button

        # Left click.
        if button == 1:
            self._check_cell(column, row)

        # Right click.
        if button == 3:
            self._flag_cell(column, row)

	# Stop condition.
	minecount = self.minefield.minecount
	if self.uncovered - minecount == 0:
	    if self.flagged < minecount:
		self._flag_unflagged()
	    self.finished = True
	    self.emit("done")


