#!/usr/bin/env python
#
# this is toy tool
#
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Example(Gtk.Window):
    """Using Pango to get system fonts names"""
    def list_system_fonts(self):
        """Yield system fonts families names using Pango"""
        context = self.create_pango_context()
        for fam in context.list_families():
            yield fam.get_name()


system_fonts = list(Example().list_system_fonts())
print(system_fonts)
