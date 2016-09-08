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

import os, sys, gi, requests, datetime,\
requests.exceptions as ecs, urllib.parse as urlparse
from PIL import Image
from gi.repository import Gtk
sys.path.append(".")
from settings import verify_req, icns
from dialog import *

def do_export_bookmarks(list):

    content = []

    header = "<!DOCTYPE NETSCAPE-Bookmark-file-1><!--This is an automatically generated file.\
    It will be read and overwritten. Do Not Edit! --><META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html;\
    charset=UTF-8\"><Title>{}</Title><H1>{}</H1><DL><p>".format(_("Bookmarks"), _("Bookmarks"))
    footer = "</DL><p>"

    content.append(header)

    for i in list:

        timestamp = int(datetime.datetime.strptime(i[0], "%Y-%m-%d %H:%M").timestamp())
        title = i[1]
        url = i[2]

        content.append("<DT><A HREF=\"{}\" ADD_DATE=\"{}\">{}</a>".format(url, timestamp, title))
 
    content.append(footer)
    content = ''.join([s for s in content])

    return content

def request(url, bool):

    list = []
    request = requests.get(url, verify=bool)
    source = request.content
    content_type = request.headers.get("content-type")
    list.append([source] + [content_type])

    return list

def is_image_valid(file):

    try:
        Image.open(file)
    except IOError:
        return False
    return True

def is_url_valid(url, bool):

    try:
        request = requests.get(url, verify=bool)
        if request.status_code == 200: return True
    except ecs.ConnectionError: return False
    except ecs.InvalidURL: return False

def catch_error(url, bool):

    try:
        request = requests.get(url, verify=bool, timeout=1)
        if request.status_code == 200: return True
    except ecs.RequestException as e: return e
    except ecs.SSLError as e: return e

def get_domain(url):

    return urlparse.urlunparse(urlparse.urlparse(url)[:2] + ("",) * 4).split("://",1)[1]

def minify(arg, num):

    try:
        arg = arg[:num] + (arg[num:] and '...')
    except: pass
    return arg

def get_filename(dest):

    name_split = dest.split("/")
    name = name_split[-1]
    return name

def make_icon(filename):

    icon = Gtk.Image()
    icon.set_from_file("{}{}".format(icns, filename))
   
    return icon

def make_label(x, y):

    label = Gtk.Label()
    label.set_alignment(x, y)
   
    return label

def make_label_selectable(x, y):

    label = make_label(x, y)
    label.set_selectable(True)
    label.set_can_focus(False)

    return label

def make_button(icon):

    button = Gtk.Button()
    button.set_always_show_image(True)
    button.set_image(icon)
    button.set_border_width(3)
    button.set_relief(Gtk.ReliefStyle.NONE)
    button.set_can_focus(False)

    return button

def make_modelbutton(text, xalign, yalign):

    button = Gtk.ModelButton(label=text)
    button.set_alignment(xalign, yalign)
    button.get_child().set_padding(5, 5)

    return button

def make_modelbutton_label(text, xalign, yalign):

    label = Gtk.Label()
    label.set_alignment(0.95, 0.5)
    label.set_markup("<span color='gray' size='x-small'>{}</span>".format(text))

    return label

def make_box(text, length, digit):

    label = Gtk.Label()
    label.set_markup("<span size='small'>{}</span>".format(text))
    label.set_alignment(0.0, 0.5)
    label.set_property("margin-top", 10)
    entry = Gtk.Entry()

    if length: entry.set_max_length(length)

    if digit:
        entry.set_name(str(digit))
        entry.connect("changed", digits_only)

    grid = Gtk.Grid()
    grid.attach(label, 0, 0, 1, 1)
    grid.attach(entry, 0, 1, 1, 1)
  
    return grid

def digits_only(entry):

    value = entry.get_text()
    digit = entry.get_name()
    
    if digit == str(1): value = ''.join([c for c in value if c.isdigit()])
    if digit == str(2): value = ''.join([c for c in value if c.isdigit() and value < str(2)])

    entry.set_text(value)

    return True

def timelist(action, view, bflist, button, margin, xalign, yalign, hover, icns):

    if action == 0: timelist = bflist.get_back_list_with_limit(10)
    else: timelist = bflist.get_forward_list_with_limit(10)

    popover = Gtk.Popover()
    menu = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
    menu.set_property('margin', margin)
    popover.set_relative_to(button)
    popover.set_position(Gtk.PositionType.BOTTOM)
    popover.add(menu)

    for item in timelist:

        url = item.get_uri()
        title = item.get_title()

        if item.get_title(): title = minify(title, 50)
        else: title = minify(url, 50)

        link = Gtk.ModelButton()
        link.set_alignment(xalign, yalign)
        link.set_label(title)

        link_icon = Gtk.Image()
        link_icon.set_from_file("{}text-x-generic.svg".format(icns))

        grid_timelist = Gtk.Grid()
        grid_timelist.set_column_spacing(10)
        grid_timelist.attach(link_icon, 0, 1, 1, 1)
        grid_timelist.attach(link, 1, 1, 1, 1)
        grid_timelist.set_column_homogeneous(False)

        link.connect("clicked", lambda throw_away=0, url=url: view.load_uri(url))
        link.connect("enter", lambda throw_away=0, url=url: hover.set_text(minify(url, 100)))
        link.connect("leave", lambda x: hover.set_text(""))
        
        menu.pack_start(grid_timelist, False, False, 0)

    popover.show_all()

