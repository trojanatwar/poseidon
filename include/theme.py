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
from gi.repository import Gtk, Gdk

sys.path.append(".")
from settings import theme_file, trans_pop
from functions import is_image_valid

def apply_css():

    # Tested on Gtk 3.18/3.20

    alpha = "popover, .popover { opacity: 0.95; }"

    theme = "#notebook.header.top, #notebook header tabs { background: url('"\
    + theme_file + "') no-repeat center; background-size: cover; }"

    css = """

    #notebook.header.top, #notebook header tabs { background: none; }
    #notebook tab { padding: 5px 10px 5px 10px; }
    #frame_main border, #frame_find border, #frame_vte border, #frame_status border,
    #frame_permission border, #frame_cert border, #frame_cookies border { border-style: none; }
    #frame_main, #frame_find, #frame_vte, #frame_status, #frame_permission, #frame_cert, #frame_cookies,
    #frame_mime border, #frame_mime { padding: 5px; }
    #entry border { border-style: solid; }
    #label_x509 { padding: 10px; }
    #frame_x509 border { border-width: 0px 0px 1px 0px; }
    #headerbar button { padding: 0px; }

    """

    if trans_pop: css += alpha

    if os.path.exists(theme_file):
        if is_image_valid(theme_file): css += theme

    cssprovider = Gtk.CssProvider()
    cssprovider.load_from_data(bytes(css.encode()))
    screen = Gdk.Screen.get_default()
    stylecontext = Gtk.StyleContext()
    stylecontext.add_provider_for_screen(screen, cssprovider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

