import argparse
import gi
import os
import sys

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class ImageWindow(Gtk.Window):
    def __init__(self, imgfile):
        Gtk.Window.__init__(self, title="Image Viewer")

        image = Gtk.Image()
        image.set_from_file(imgfile)
        self.set_default_size(image.get_pixbuf().get_width(), image.get_pixbuf().get_height())

        box = Gtk.Box(spacing=6)
        box.pack_start(image, True, True, 0)
        self.add(box)

        self.connect("destroy", Gtk.main_quit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, dest="filename", required=True)
    args = parser.parse_args(sys.argv[1:])

    if not os.path.exists(args.filename):
        sys.exit("No such filename")

    win = ImageWindow(args.filename)
    win.show_all()
    Gtk.main()
