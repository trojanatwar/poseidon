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
from gi.repository import Gtk, Gdk, WebKit2
sys.path.append("modules")
import validators
sys.path.append(".")
from settings import search_engine
from functions import minify

def on_context_menu(self, view, menu, event, htr):

    '''
    ################
    # Custom Items #
    ################
    '''

    context = htr.get_context()
    action = WebKit2.ContextMenuAction.OUTLINE

    if context == 14 or context == 10:

        if htr.context_is_image():

            url = htr.get_image_uri()

            if "://" in url:

                item = WebKit2.ContextMenuItem().\
                new_from_stock_action_with_label(action, _("Apply as theme"))

                a = item.get_action()
                a.connect("activate", lambda x: self.apply_theme(url))
                a.set_stock_id(Gtk.STOCK_SELECT_COLOR)
                item = item.new(a)

                menu.insert(item, 0)
                menu.insert(WebKit2.ContextMenuItem().new_separator(), 1)

    if context == 130 or context == 134:

        if context == 134:
            menu.insert(WebKit2.ContextMenuItem().\
            new_from_stock_action(WebKit2.ContextMenuAction.COPY), 4)

        if not search_engine: return True

        text = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)

        if htr.context_is_selection():

            text = text.wait_for_text()
            isurl = validators.url(text)

            if isurl:
                item = WebKit2.ContextMenuItem().\
                new_from_stock_action_with_label(action, "{} \"{}\".".format(_("Go to"), minify(text, 30)))
            else:
                item = WebKit2.ContextMenuItem().\
                new_from_stock_action_with_label(action, "{} \"{}\" {}.".format(_("Search"), minify(text, 30), _("in the web")))

            a = item.get_action()

            if isurl:
                a.connect("activate", lambda x: view.load_uri(text))
                a.set_stock_id(Gtk.STOCK_OPEN)
            else:
                a.connect("activate", lambda x: view.load_uri("{}{}".format(search_engine, text)))
                a.set_stock_id(Gtk.STOCK_FIND)

            item = item.new(a)

            menu.insert(item, 0)
            menu.insert(WebKit2.ContextMenuItem().new_separator(), 1)

    '''
    #########################
    # Modify Existing Items #
    #########################
    '''

    items = menu.get_items()

    for i in items:
        if not i.is_separator():

            action = i.get_stock_action()

            #print ("ACTION: ", action, "CONTEXT: ", context) # Debug

            if action == WebKit2.ContextMenuAction.OPEN_FRAME_IN_NEW_WINDOW: menu.remove(i)

            if action == WebKit2.ContextMenuAction.OPEN_LINK_IN_NEW_WINDOW or\
               action == WebKit2.ContextMenuAction.OPEN_VIDEO_IN_NEW_WINDOW or\
               action == WebKit2.ContextMenuAction.OPEN_IMAGE_IN_NEW_WINDOW:

                if htr.context_is_link(): url = htr.get_link_uri()
                if htr.context_is_media(): url = htr.get_media_uri()
                if htr.context_is_image(): url = htr.get_image_uri()

                a = i.get_action()
                a.connect("activate", lambda x: self.open_blank(url))
                i = i.new(a)

