#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Poseidon.
#
# Poseidon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Poseidon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Poseidon. If not, see <http://www.gnu.org/licenses/>.

import os, sys, gi
from gi.repository import Gtk
sys.path.append(".")
from dialog import *
from settings import width, height

class pathchooser(Gtk.Window):

    def force_save(self, content, name):

        d = Gtk.FileChooserDialog("{}: {}".format(_("Save as"), name), self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        d.set_current_name(name)
        d.set_default_size(int(width), int(height))
        response = d.run()

        if response == Gtk.ResponseType.OK:

            if os.path.exists(d.get_filename()):
                if self.do_decision(name):
                    pass
                else:
                    d.destroy()
                    return True

            with open(d.get_filename(), 'w') as f:
                f.write(content)
                f.close()

        d.destroy()

    def save(self, name, download, url):

        d = Gtk.FileChooserDialog("{}: {}".format(_("Save as"), name), self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))

        d.set_current_name(name)
        d.set_default_size(int(width), int(height))
        response = d.run()

        if response == Gtk.ResponseType.ACCEPT:
            
            if os.path.exists(d.get_filename()):
                if self.do_decision(d.get_filename()):
                    download.set_allow_overwrite(True)

            download.set_destination("file://{}".format(d.get_filename()))

        elif response == Gtk.ResponseType.CANCEL\
        or response == Gtk.ResponseType.DELETE_EVENT: download.cancel()

        d.destroy()

    def open(self, view):

        d = Gtk.FileChooserDialog(_("Open file"), self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        d.set_default_size(int(width), int(height))
        response = d.run()

        if response == Gtk.ResponseType.ACCEPT:

            view.load_uri("file://{}".format(d.get_filename()))

        d.destroy()

    def import_bookmarks(self):

        d = Gtk.FileChooserDialog(_("Import a HTML bookmark file"), self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT))

        d.set_default_size(int(width), int(height))

        filter_html = Gtk.FileFilter()
        filter_html.set_name("HTML files")
        filter_html.add_mime_type("text/html")
        d.add_filter(filter_html)

        response = d.run()

        if response == Gtk.ResponseType.ACCEPT:

            filename = d.get_filename()
            d.destroy()
            return filename

        d.destroy()

    def do_decision(self, name):
        return dialog().decision("{}?".format(_("Overwrite")),\
        "<span size='small'>\"<b>{}</b>\" {}</span>"\
        .format(name, _("already exists, wanna overwrite it?")))

