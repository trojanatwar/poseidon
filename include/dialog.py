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

import sys, gi
from gi.repository import Gtk

sys.path.append(".")
from settings import browser_name, version, authors,\
translators, comments, website

class dialog(Gtk.Window):

    def fix_dialog(self, dialog):

        for i in dialog.get_children():
            if type(i) == Gtk.HeaderBar: headerbar = i

        # This is a temporary fix for the duplicate buttons bug
        # in 'Gtk.AboutDialog' when 'use_header_bar' property is set.

        if type(dialog) == Gtk.AboutDialog:
            for i in headerbar:
                if type(i) != Gtk.StackSwitcher: i.destroy()

        headerbar.set_name("nobg_headerbar")

        box = dialog.get_content_area()
        box.set_border_width(10)

    def about(self, window, logo, ver):

        dialog = Gtk.AboutDialog(self, use_header_bar=True)
        dialog.set_program_name(browser_name)
        dialog.set_version("{} (WebKit {})".format(version, ver))
        dialog.set_logo(logo)
        dialog.set_authors([authors])
        dialog.set_translator_credits(translators)
        dialog.set_website(website)
        dialog.set_website_label(website)
        dialog.set_comments(comments)
        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.set_transient_for(window)
        self.fix_dialog(dialog)
        dialog.run()
        dialog.destroy()

    def info(self, first, second):

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,\
        Gtk.ButtonsType.NONE, None, use_header_bar=True, title=first)
        dialog.set_markup(second)
        self.fix_dialog(dialog)

        dialog.show_now()
        while Gtk.events_pending(): Gtk.main_iteration()
        return dialog

    def error(self, first, second):

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,\
        Gtk.ButtonsType.NONE, None, use_header_bar=True, title=first)
        dialog.set_markup(second)
        self.fix_dialog(dialog)

        dialog.run()
        dialog.destroy()

    def decision(self, first, second):

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,\
        Gtk.ButtonsType.OK_CANCEL, None, use_header_bar=True, title=first)
        dialog.set_markup(second)
        self.fix_dialog(dialog)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            dialog.destroy()
            return True

        dialog.destroy()

