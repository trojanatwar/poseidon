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

import os, sys, gi, requests, datetime, random,\
requests.exceptions as ecs, urllib.parse as urlparse
from PIL import Image
from gi.repository import Gtk, Gdk
sys.path.append(".")
from settings import verify_req, icns, set_user_agent,\
ua_browsers_dsc, ua_browsers_val, ua_mobile_dsc,\
ua_mobile_val, ua_crawlers_dsc, ua_crawlers_val
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
    content = "".join([s for s in content])

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
        request = requests.head(url, verify=bool)
        if request.status_code < 400: return True
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

    try: arg = arg[:num] + (arg[num:] and '...')
    except: pass
    return arg

def get_filename(dest):

    return dest.split("/")[-1]

def make_icon(filename):

    icon = Gtk.Image()
    icon.set_from_file("{}{}".format(icns, filename))
   
    return icon

def make_label(x, y):

    label = Gtk.Label()
    label.set_alignment(x, y)
   
    return label

def make_label_text(text):

    label = Gtk.Label()
    label.set_text(text)
   
    return label

def make_label_selectable(x, y):

    label = make_label(x, y)
    label.set_selectable(True)
    label.set_can_focus(False)

    return label

def make_button(icon, tooltip, toggle):

    if toggle: button = Gtk.ToggleButton()
    else: button = Gtk.Button()
    button.set_always_show_image(True)
    button.set_image(icon)
    button.set_border_width(3)
    button.set_relief(Gtk.ReliefStyle.NONE)
    button.set_can_focus(False)
    if tooltip: button.set_tooltip_text(tooltip)

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
    label.set_property("margin-bottom", 10)
    entry = Gtk.Entry()

    if length: entry.set_max_length(length)

    if digit:
        entry.set_name(str(digit))
        entry.connect("changed", digits_only)

    grid = Gtk.Grid()
    grid.attach(label, 0, 0, 1, 1)
    grid.attach(entry, 0, 1, 1, 1)
  
    return grid

def setting_element(option, title, value, tp, desc, list):

    grid = Gtk.Grid()
    label = Gtk.Label()
    label.set_alignment(0.0, 0.5)
    label.set_property("margin-bottom", 10)

    if desc: label.set_markup(\
    "{}\n<span size='small'>{}</span>".format(_(title), _(desc)))
    else: label.set_markup(_(title))

    if tp == "1":
        elem = Gtk.Entry(name=option)
        elem.set_width_chars(30)
        elem.set_text(value)

    if tp == "2":
        elem = Gtk.ComboBoxText(name=option)
        elem.set_entry_text_column(0)
        for i in list: elem.append_text(i)
        elem.set_active(int(value))

    grid.attach(label, 0, 0, 1, 1)
    grid.attach(elem, 0, 1, 1, 1)
    grid.set_property("margin", 10)

    return grid

def digits_only(entry):

    value = entry.get_text()
    digit = entry.get_name()
    
    if digit == str(1): value = "".join([c for c in value if c.isdigit()])
    if digit == str(2): value = "".join([c for c in value if c.isdigit() and value < str(2)])

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

def convert_size(B):

   B = float(B)
   KB = float(1024)
   MB = float(KB ** 2)
   GB = float(KB ** 3)
   TB = float(KB ** 4)

   if B < KB:
      return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
   elif KB <= B < MB:
      return '{0:.2f} KB'.format(B/KB)
   elif MB <= B < GB:
      return '{0:.2f} MB'.format(B/MB)
   elif GB <= B < TB:
      return '{0:.2f} GB'.format(B/GB)
   elif TB <= B:
      return '{0:.2f} TB'.format(B/TB)

def get_cache_size(path):

    if not os.path.exists(path): return convert_size(0)

    total_size = 0

    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    return convert_size(total_size)

def pass_generator(self):

    window = Gtk.Window()
    window.set_title(_("Password Generator"))
    window.set_position(Gtk.WindowPosition.CENTER)
    window.set_skip_taskbar_hint(True)
    window.set_transient_for(self)

    entry = make_box("{} (Def: 32) (Max: 99999)".format(_("Password Length")), 5, 1)
    button = Gtk.Button(label=_("Generate"))
    copy = Gtk.Button(label=_("Copy"))
    result = Gtk.TextView()
    result.set_wrap_mode(Gtk.WrapMode.WORD)
    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_size_request(500, 200)
    scrolled_window.add(result)

    bt_grid = Gtk.Grid()
    bt_grid.set_column_spacing(10)
    bt_grid.attach(button, 1, 0, 1, 1)
    bt_grid.attach(copy, 2, 0, 1, 1)
    bt_grid.set_column_homogeneous(True)

    grid = Gtk.Grid()
    grid.attach(entry, 0, 0, 1, 1)
    grid.attach(scrolled_window, 0, 1, 1, 1)
    grid.attach(bt_grid, 0, 2, 1, 1)

    entry.set_property("margin-bottom", 15)
    bt_grid.set_property("margin-top", 15)
    grid.set_property("margin", 15)

    window.add(grid)
    window.show_all()

    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    for i in entry:
        if type(i) == Gtk.Entry: entry = i

    button.connect("clicked", lambda x: pass_generate(entry.get_text(), 32, result))
    copy.connect("clicked", lambda x: clipboard.set_text(result.get_buffer().\
    get_text(result.get_buffer().get_start_iter(),result.get_buffer().get_end_iter(), False), -1))

def pass_generate(length, default_length, result):

    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789^!\$%&/()=?{[]}+~#-_.:,;<>|\\"
    password = str()

    if not length:
        length = int(default_length)
    else:
        length = int(length)

    for i in range(length):
        n = random.randrange(len(charset))
        password = password + charset[n]

    for i in range(random.randrange(1,3)):
        r = random.randrange(len(password)//2)
        password = password[0:r] + str(random.randrange(10)) + password[r+1:]

    for i in range(random.randrange(1,3)):
        r = random.randrange(len(password)//2,len(password))
        password = password[0:r] + password[r].upper() + password[r+1:]

    result.get_buffer().set_text(password)

def user_agent(self):

    window = Gtk.Window()
    window.set_title("User Agent")
    window.set_position(Gtk.WindowPosition.CENTER)
    window.set_skip_taskbar_hint(True)
    window.set_transient_for(self)

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_size_request(300, 300)

    tree = Gtk.TreeView()
    tree.connect('row-activated', self.new_user_agent)
    column = Gtk.TreeViewColumn()
    column.set_title(_("Double click item to switch"))

    cell = Gtk.CellRendererText()
    column.pack_start(cell, True)
    column.add_attribute(cell, "text", 0)

    treestore = Gtk.TreeStore(str, str)

    ua_browsers_list = []
    ua_mobile_list = []
    ua_crawlers_list = []

    treestore.append(None, ["Default", ""])

    browsers = treestore.append(None, ["Browsers", None])
    for c, i in enumerate(ua_browsers_dsc): ua_browsers_list.append([i, ua_browsers_val[c]])
    ua_browsers_list.sort()
    for c, i in enumerate(ua_browsers_list): treestore.append(browsers, [ua_browsers_list[c][0], ua_browsers_list[c][1]])

    mobile = treestore.append(None, ["Mobile Browsers", None])
    for c, i in enumerate(ua_mobile_dsc): ua_mobile_list.append([i, ua_mobile_val[c]])
    ua_mobile_list.sort()
    for c, i in enumerate(ua_mobile_list): treestore.append(mobile, [ua_mobile_list[c][0], ua_mobile_list[c][1]])

    crawlers = treestore.append(None, ["Crawlers", None])
    for c, i in enumerate(ua_crawlers_dsc): ua_crawlers_list.append([i, ua_crawlers_val[c]])
    ua_crawlers_list.sort()
    for c, i in enumerate(ua_crawlers_list): treestore.append(crawlers, [ua_crawlers_list[c][0], ua_crawlers_list[c][1]])

    tree.append_column(column)
    tree.set_model(treestore)
    scrolled_window.add(tree)

    window.add(scrolled_window)
    window.show_all()

