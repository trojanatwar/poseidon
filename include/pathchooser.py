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
from functions import get_domain

class pathchooser(Gtk.Window):

    def force_save(self, content, name):

        d = Gtk.FileChooserDialog("{}: {}".format(_("Save as"), name), self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        d.set_current_name(name)
        d.set_default_size(width, height)
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

        if not name: name = get_domain(url).replace(".","_")

        if not "." in name:

            mime = download.get_response().get_mime_type()
            suf = mime.split("/")
            name = "{}.{}".format(name, suf[1])

        d = Gtk.FileChooserDialog("{}: {}".format(_("Save as"), name), self,
            Gtk.FileChooserAction.SAVE,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        d.set_current_name(name)
        d.set_default_size(width, height)
        response = d.run()

        if response == Gtk.ResponseType.OK:
            
            if os.path.exists(d.get_filename()):
                if self.do_decision(d.get_filename()):
                    download.set_allow_overwrite(True)

            download.set_destination("file://{}".format(d.get_filename()))

        elif response == Gtk.ResponseType.CANCEL\
        or response == Gtk.ResponseType.DELETE_EVENT: download.cancel()

        d.destroy()

    def open(self, view, page):

        d = Gtk.FileChooserDialog("Open file", self,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        d.set_default_size(width, height)
        response = d.run()

        if response == Gtk.ResponseType.OK:

            filename = d.get_filename()
            view.load_uri("file://{}".format(filename))
            page.main_url_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, None)
            page.main_url_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.SECONDARY, None)

        d.destroy()

    def do_decision(self, name):
        return dialog().decision("{}?".format(_("Overwrite")),\
        "<span size='small'>\"<b>{}</b>\" {}</span>"\
        .format(name, _("already exists, wanna overwrite it?")))

