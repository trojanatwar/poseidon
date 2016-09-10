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

import sys, gi, datetime
from gi.repository import Gtk
sys.path.append(".")
from settings import browser_name, version, authors, comments, website

license = """
Poseidon is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Poseidon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Poseidon. If not, see <http://www.gnu.org/licenses/>.
"""

class dialog(Gtk.Window):

    def about(self, window, logo, ver):

        dialog = Gtk.AboutDialog(self)
        dialog.set_program_name(browser_name)
        dialog.set_version("{} (WebKit {})".format(version, ver))
        dialog.set_logo(logo)
        dialog.set_authors([authors])
        dialog.set_website(website)
        dialog.set_website_label(website)
        dialog.set_comments(comments)
        dialog.set_license(license)
        dialog.set_wrap_license(True)
        dialog.set_copyright("{} © {}".format(browser_name, datetime.datetime.now().year))
        dialog.set_transient_for(window)
        dialog.run()
        dialog.destroy()

    def info(self, first, second):

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.NONE, first)
        dialog.format_secondary_markup(second)
        dialog.show_now()
        while Gtk.events_pending(): Gtk.main_iteration()
        return dialog

    def error(self, first, second):

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, first)
        dialog.format_secondary_markup(second)
        dialog.run()
        dialog.destroy()

    def decision(self, first, second):

        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, first)
        dialog.format_secondary_markup(second)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            dialog.destroy()
            return True

        dialog.destroy()

