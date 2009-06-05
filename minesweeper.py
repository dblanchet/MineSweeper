import sys

try:
    import pygtk
    pygtk.require('2.0')
except:
    print "This program require PyGtk 2.0."
    sys.exit(1)
import gtk

from minefield import MineField
from minefieldview import MineFieldView
from flagcounter import FlagCounter


class MineSweeper(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title('MineSweeper')
        self.connect('destroy', gtk.main_quit)

        self.rows = 15
        self.columns = 20
        self.minecount = 40
        #self.rows = 10
        #self.columns = 10
        #self.minecount = 10

        vbox = gtk.VBox(False, 0)
        self.add(vbox)

        hbox = gtk.HBox(True, 0)
        vbox.pack_start(hbox, True, False, 10)

        button = gtk.Button('New')
        button.connect("clicked", self.on_new_button_clicked)
        hbox.pack_start(button, True, True, 10)

        self.count = FlagCounter(self.minecount, 32)
        hbox.pack_start(self.count, False, False, 10)

        minefield = MineField(self.columns, self.rows, self.minecount)
        self.view = MineFieldView(minefield)
	self.view.connect("started", self.on_started)
	self.view.connect("flagged", self.on_flagged)
	self.view.connect("done", self.on_done)
	self.view.connect("explosion", self.on_explosion)
        vbox.pack_start(self.view, True, True, 0)

        status = gtk.Statusbar()
        status.set_size_request(-1, 32)
        vbox.pack_start(status, False, True, 0)

    def on_started(self, widget):
	print "Started!"

    def on_flagged(self, widget, count):
        self.count.set_value(self.minecount - count)

    def on_done(self, widget):
	print "Done!"

    def on_explosion(self, widget):
	print "Boom!"

    def on_new_button_clicked(self, widget, *args):
        minefield = MineField(self.columns, self.rows, self.minecount)
        self.view.set_minefield(minefield)
        self.count.set_value(self.minecount)

    def run(self):
        self.show_all()
        gtk.main()


def main(argv=None):
    MineSweeper().run()


if __name__ == '__main__':
    main(sys.argv)

