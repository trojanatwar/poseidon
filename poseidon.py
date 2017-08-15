#!/usr/bin/env python
# -*- coding: utf-8 -*-
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


import sys, gi, getopt, os, subprocess,\
sqlite3 as lite, time, datetime, re, html

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib
from os import path

sys.path.append("modules")
import validators

sys.path.append("include")
from settings import *
from theme import *
from functions import *
from pathchooser import *
from database import *
from dialog import *

'''
########################################
# Start Missing Dependencies Detection #
########################################
'''

try: gi.require_version('WebKit2', '4.0')
except:
    dialog().error(_("WebKit2 is missing"),\
    "<span size='small'>{} {} WebKit2 {}.</span>"\
    .format(browser_name, _("requires"), _("installed on your system")))
    exit()
else:
    from gi.repository import WebKit2
    from menu import *

try: gi.require_version('GtkSource', '3.0')
except:
    dialog().error(_("GtkSourceView 3 is missing"),\
    "<span size='small'>{} {} GtkSourceView 3 {}.</span>"\
    .format(browser_name, _("requires"), _("installed on your system")))
    exit()
else: from gi.repository.GtkSource import LanguageManager, Buffer,\
View, SearchContext, SearchSettings

try: from OpenSSL import crypto
except:
    dialog().error(_("pyOpenSSL is missing"),\
     "<span size='small'>{} {} pyOpenSSL {}.</span>"\
    .format(browser_name, _("requires"), _("installed on your system")))
    exit()
else: from secure import secure, certificate, cert_declarations

try: import socks
except:
    dialog().error(_("PySocks is missing"),\
     "<span size='small'>{} {} PySocks {}.</span>"\
    .format(browser_name, _("requires"), _("installed on your system")))
    exit()

'''
######################################
# End Missing Dependencies Detection #
######################################
'''

browser = __file__.replace(".py", "")

'''
######################
# Get WebKit Version #
######################
'''

try: webkit_ver = WebKit2.get_major_version(), WebKit2.get_minor_version(), WebKit2.get_micro_version()
except: webkit_ver = None

wk12 = (2,12,3)
wk16 = (2,16,0)

if webkit_ver and webkit_ver < wk12: webkit_ver = None

'''
######################
# Set WebKit Context #
######################
'''

web_context = WebKit2.WebContext.get_default()
web_context.set_web_extensions_directory(path.abspath("{}/{}/".format(path.dirname(__file__), lib_path)))

if adkiller: write_file(adk_file, "1")
else: write_file(adk_file, "0")

if process_model == 0: pmodel = WebKit2.ProcessModel.SHARED_SECONDARY_PROCESS
if process_model == 1: pmodel = WebKit2.ProcessModel.MULTIPLE_SECONDARY_PROCESSES
web_context.set_process_model(pmodel)

'''
########
# Misc #
########
'''

mem_url = []
local_ip = "127.0.0.1"


'''
###################
# BrowserTab INIT #
###################
'''

class BrowserTab(Gtk.VBox):
    def __init__(self, *args, **kwargs):
        super(BrowserTab, self).__init__(*args, **kwargs)

        '''
        #############
        # Is Defcon #
        #############
        '''

        if self.get_name() == "defcon": self.is_defcon = True
        else: self.is_defcon = False

        '''
        ################
        # Show WebView #
        ################
        '''

        webview = WebKit2.WebView.new_with_context(web_context)

        self.show()

        '''
        ###################
        # WebKit Settings #
        ###################
        '''

        settings = webview.get_settings()

        settings.set_property("allow-file-access-from-file-urls", set_allow_file_access_from_file_urls)
        settings.set_property("allow-modal-dialogs", set_allow_modal_dialogs)
        settings.set_property("auto-load-images", set_auto_load_images)
        settings.set_property("cursive-font-family", font_list[set_cursive_font_family])
        settings.set_property("default-charset", charset_list[set_default_charset])
        settings.set_property("default-font-family", font_list[set_default_font_family])
        settings.set_property("default-font-size", int(set_default_font_size))
        settings.set_property("default-monospace-font-size", int(set_default_monospace_font_size))
        settings.set_property("draw-compositing-indicators", set_draw_compositing_indicators)
        settings.set_property("enable-accelerated-2d-canvas", set_enable_accelerated_2d_canvas)
        settings.set_property("enable-caret-browsing", set_enable_caret_browsing)
        settings.set_property("enable-developer-extras", set_enable_developer_extras)
        settings.set_property("enable-dns-prefetching", set_enable_dns_prefetching)
        settings.set_property("enable-frame-flattening", set_enable_frame_flattening)
        settings.set_property("enable-fullscreen", set_enable_fullscreen)
        settings.set_property("enable-html5-database", set_enable_html5_database)
        settings.set_property("enable-html5-local-storage", set_enable_html5_local_storage)
        settings.set_property("enable-hyperlink-auditing", set_enable_hyperlink_auditing)
        settings.set_property("enable-java", set_enable_java)
        settings.set_property("enable-javascript", set_enable_javascript)
        settings.set_property("enable-media-stream", set_enable_media_stream)
        settings.set_property("enable-mediasource", set_enable_mediasource)
        settings.set_property("enable-offline-web-application-cache", set_enable_offline_web_application_cache)
        settings.set_property("enable-page-cache", set_enable_page_cache)
        settings.set_property("enable-plugins", set_enable_plugins)
        settings.set_property("enable-resizable-text-areas", set_enable_resizable_text_areas)
        settings.set_property("enable-site-specific-quirks", set_enable_site_specific_quirks)
        settings.set_property("enable-smooth-scrolling", set_enable_smooth_scrolling)
        settings.set_property("enable-spatial-navigation", set_enable_spatial_navigation)
        settings.set_property("enable-tabs-to-links", set_enable_tabs_to_links)
        settings.set_property("enable-webaudio", set_enable_webaudio)
        settings.set_property("enable-webgl", set_enable_webgl)
        settings.set_property("enable-write-console-messages-to-stdout", set_enable_write_console_messages_to_stdout)
        settings.set_property("enable-xss-auditor", set_enable_xss_auditor)
        settings.set_property("fantasy-font-family", font_list[set_fantasy_font_family])
        settings.set_property("javascript-can-access-clipboard", set_javascript_can_access_clipboard)
        settings.set_property("javascript-can-open-windows-automatically", set_javascript_can_open_windows_automatically)
        settings.set_property("load-icons-ignoring-image-load-setting", set_load_icons_ignoring_image_load_setting)
        settings.set_property("media-playback-allows-inline", set_media_playback_allows_inline)
        settings.set_property("media-playback-requires-user-gesture", set_media_playback_requires_user_gesture)
        settings.set_property("minimum-font-size", set_minimum_font_size)
        settings.set_property("monospace-font-family", font_list[set_monospace_font_family])
        settings.set_property("pictograph-font-family", font_list[set_pictograph_font_family])
        settings.set_property("print-backgrounds", set_print_backgrounds)
        settings.set_property("sans-serif-font-family", font_list[set_sans_serif_font_family])
        settings.set_property("serif-font-family", font_list[set_serif_font_family])
        settings.set_property("user-agent", set_user_agent)
        settings.set_property("zoom-text-only", set_zoom_text_only)

        '''
        ########################################
        # Deprecated Symbols for WebKit 2.16.x #
        ########################################
        '''

        if webkit_ver < wk16:

            settings.set_property("enable-private-browsing", self.is_defcon)

        '''
        #######################
        # Set WebKit Settings #
        #######################
        '''

        webview.set_settings(settings)

        '''
        #########
        # Other #
        #########
        '''

        if not self.is_defcon:

            data_manager = WebKit2.WebsiteDataManager()
            cache_path = data_manager.get_disk_cache_directory()
            web_context.new_with_website_data_manager(data_manager)
            web_context.set_cache_model(cache_model)
            web_context.set_favicon_database_directory(cache_path)

        else: web_context.set_cache_model(0)

        controller = webview.get_find_controller()
        bflist = webview.get_back_forward_list()
        download_icon = make_icon("go-down.svg")
        scrolled_window = Gtk.ScrolledWindow(name="webview")
        scrolled_window.set_shadow_type(Gtk.ShadowType.IN)
        apply_css()

        '''
        ##################
        # Navigation Box #
        ##################
        '''

        main_url_entry = Gtk.Entry(name="entry")
        main_url_entry.connect("button-press-event", self.on_url_entry_button_press)

        go_back = make_button(make_icon("go-previous.svg"), None, False)
        go_back.connect("button-press-event", self.on_go_back_press)
        go_back.connect("button-release-event", self.on_go_back_release)

        go_forward = make_button(make_icon("go-next.svg"), None, False)
        go_forward.connect("button-press-event", self.on_go_forward_press)
        go_forward.connect("button-release-event", self.on_go_forward_release)

        refresh = make_button(make_icon("refresh.svg"), None, False)
        refresh.connect("clicked", lambda x: webview.reload())

        cancel = make_button(make_icon("cancel.svg"), None, False)
        cancel.connect("clicked", lambda x: webview.stop_loading())

        if home_page:
            home = make_button(make_icon("go-home.svg"), None, False)
            home.connect("clicked", lambda x: webview.load_uri(home_page))

        go_button = make_button(make_icon("go-up.svg"), None, False)

        download_button = make_button(download_icon, None, True)
        bookmarks_button = make_button(make_icon("bookmarks.svg"), None, True)
        tools = make_button(make_icon("open-menu.svg"), None, True)

        url_box = Gtk.HBox(name="frame_main")
        url_box.pack_start(go_back, False, False, 0)
        url_box.pack_start(go_forward, False, False, 0)
        url_box.pack_start(refresh, False, False, 0)
        url_box.pack_start(cancel, False, False, 0)
        if home_page: url_box.pack_start(home, False, False, 0)
        url_box.pack_start(main_url_entry, True, True, 10)
        url_box.pack_start(go_button, False, False, 0)
        url_box.pack_start(download_button, False, False, 0)
        url_box.pack_start(bookmarks_button, False, False, 0)
        url_box.pack_start(tools, False, False, 0)

        '''
        ################
        # Autocomplete #
        ################
        '''

        if autocomplete_policy != 0:

            entrycompletion = Gtk.EntryCompletion()
            entrycompletion.set_text_column(0)

            if autocomplete_policy == 1:

                liststore = Gtk.ListStore(str, str)
                entrycompletion.set_minimum_key_length(2)

            else: liststore = Gtk.ListStore(str)

            entrycompletion.set_model(liststore)
            main_url_entry.set_completion(entrycompletion)

            if autocomplete_policy == 1: entrycompletion.connect('match-selected', self.on_autocomplete_match)
            else:
                if search_engine: entrycompletion.connect('match-selected', self.on_autocomplete_search)

        '''
        ################
        # Progress Box #
        ################
        '''

        progress_box = Gtk.HBox()
        pbar = Gtk.ProgressBar()
        progress_box.pack_start(pbar, True, True, 0)

        '''
        ############
        # Find Box #
        ############
        '''

        find_box = Gtk.HBox(name="frame_find")

        find_entry = Gtk.Entry()
        find_entry.set_width_chars(30)
        find_entry.connect("activate", lambda x: self.on_finder())
        find_entry.connect("changed", lambda x: self.on_finder())
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("{}system-search.svg".format(icns))
        find_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, pixbuf)

        prev_button = make_button(make_icon("go-up.svg"), None, False)
        prev_button.connect("clicked", lambda x: controller.search_previous())

        next_button = make_button(make_icon("go-down.svg"), None, False)
        next_button.connect("clicked", lambda x: controller.search_next())

        close_button = make_button(make_icon("close-panel.svg"), None, False)
        close_button.connect("clicked", lambda x: self.on_close_finder())

        find_box.pack_start(find_entry, False, False, 10)
        find_box.pack_start(prev_button, False, False, 0)
        find_box.pack_start(next_button, False, False, 0)
        find_box.pack_start(close_button, False, False, 0)

        find_revealer = revealize(find_box)

        '''
        ###########
        # VTE Box #
        ###########
        '''

        frame_vte = Gtk.Frame(name="frame_vte")

        vte_sw = Gtk.ScrolledWindow()
        vte_sw.set_size_request(-1,300)

        close_vte_button = make_button(make_icon("close.svg"), None, False)
        close_vte_button.connect("clicked", lambda x: [self.on_close_terminal(vte_sw, vte_revealer), iconified_vte.hide()])

        hide_vte_button = make_button(make_icon("minimize.svg"), None, False)
        hide_vte_button.connect("clicked", lambda x: [reveal(vte_revealer, False), iconified_vte.show()])

        vte_box = Gtk.HBox()
        vte_box.pack_end(close_vte_button, False, True, 0)
        vte_box.pack_end(hide_vte_button, False, True, 0)

        grid = Gtk.Grid()
        grid.set_column_spacing(0)
        grid.attach(vte_box, 0, 1, 1, 1)
        grid.attach(vte_sw, 0, 2, 1, 1)
        grid.set_column_homogeneous(True)

        frame_vte.add(grid)
        vte_revealer = revealize(frame_vte)

        '''
        ##############
        # Status Box #
        ##############
        '''

        link_hover = make_label(0.0, 0.5)

        iconified_vte = Gtk.EventBox()
        iconified_vte.add(make_icon("terminal.svg"))

        status_box = Gtk.HBox(False, name="frame_status")
        status_box.pack_start(link_hover, True, True, 10)
        status_box.pack_end(iconified_vte, False, True, 0)

        '''
        ##################
        # Permission Box #
        ##################
        '''

        permission_box = Gtk.HBox(name="frame_permission")
        permission_message = make_label(0.0, 0.5)
        allow_button = make_button(make_icon("object-select.svg"), None, False)
        deny_button = make_button(make_icon("window-close.svg"), None, False)

        permission_box.pack_start(permission_message, True, True, 10)
        permission_box.pack_start(allow_button, False, False, 0)
        permission_box.pack_start(deny_button, False, False, 0)

        allow_button.connect("clicked", lambda x: self.on_allow(self.perm_request))
        deny_button.connect("clicked", lambda x: self.on_deny(self.perm_request))

        permission_revealer = revealize(permission_box)

        '''
        ###################
        # Certificate Box #
        ###################
        '''

        cert_box = Gtk.HBox()
        cert_message = make_label(0.0, 0.5)
        allow_cert_button = make_button(make_icon("object-select.svg"), None, False)
        deny_cert_button = make_button(make_icon("window-close.svg"), None, False)

        cert_box.pack_start(cert_message, True, True, 10)
        cert_box.pack_start(allow_cert_button, False, False, 0)
        cert_box.pack_start(deny_cert_button, False, False, 0)

        frame_cert = Gtk.Frame(name="frame_cert")
        frame_cert.add(cert_box)
        cert_revealer = revealize(frame_cert)

        deny_cert_button.connect("clicked", lambda x: reveal(cert_revealer, False))

        '''
        #################
        # Start Packing #
        #################
        '''

        self.pack_start(url_box, False, False, 0)
        self.pack_start(permission_revealer, False, False, 0)
        self.pack_start(cert_revealer, False, False, 0)
        self.pack_start(progress_box, False, False, 0)
        self.pack_start(scrolled_window, True, True, 0)
        self.pack_start(vte_revealer, False, False, 0)
        self.pack_start(find_revealer, False, False, 0)
        self.pack_start(status_box, False, False, 0)

        '''
        ###############
        # End Packing #
        ###############
        '''

        url_box.show_all()
        status_box.show_all()
        iconified_vte.hide()

        cancel.hide()
        refresh.set_sensitive(False)
        go_back.set_sensitive(False)
        go_forward.set_sensitive(False)
        main_url_entry.set_icon_sensitive(Gtk.EntryIconPosition.SECONDARY, True)

        '''
        ###########
        # Selfize #
        ###########
        '''

        self.security = None
        self.webview = webview
        self.controller = controller
        self.scrolled_window = scrolled_window
        self.main_url_entry = main_url_entry
        self.go_back = go_back
        self.go_forward = go_forward
        self.go_button = go_button
        self.refresh = refresh
        self.cancel = cancel
        self.download_icon = download_icon
        self.download_button = download_button
        self.bookmarks_button = bookmarks_button
        self.tools = tools
        self.url_box = url_box
        self.pbar = pbar
        self.progress_box = progress_box
        self.find_entry = find_entry
        self.find_revealer = find_revealer
        self.vte_revealer = vte_revealer
        self.vte_sw = vte_sw
        self.iconified_vte = iconified_vte
        self.link_hover = link_hover
        self.permission_revealer = permission_revealer
        self.permission_message = permission_message
        self.allow_button = allow_button
        self.deny_button = deny_button
        self.cert_revealer = cert_revealer
        self.cert_message = cert_message
        self.allow_cert_button = allow_cert_button
        self.deny_cert_button = deny_cert_button
        self.bflist = bflist

        if not self.is_defcon: self.cache_path = cache_path

        scrolled_window.add(webview)
        scrolled_window.show_all()

        '''
        ###########
        # Signals #
        ###########
        '''

        try:
            self.webview.connect("mouse-target-changed", self.on_mouse_target_changed)
            self.webview.connect("permission-request", self.on_permission_request)
            self.webview.connect("insecure-content-detected", lambda x, y: self.is_insecure())
            self.webview.connect("notify::favicon", self.on_favicon)
            self.webview.connect("notify::uri", self.on_uri_changed)
            self.webview.connect("notify::estimated-load-progress", self.on_estimated_load_progress)
            self.controller.connect("counted-matches", self.on_counted_matches)
            if autocomplete_policy != 0: self.main_url_entry.connect("changed",\
            lambda x: self.on_entry_timeout(main_url_entry.get_text(), liststore))
        except: pass

    def on_estimated_load_progress(self, view, load):

        prog = view.get_estimated_load_progress()

        if prog == 1.0: self.progress_box.hide()
        else: self.progress_box.show_all()

        self.pbar.set_fraction(prog)

        return True

    def on_url_entry_button_press(self, widget, event):

        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3:
            url_entry_menu(widget)
            return True

    def stop_ac_timeout(self, query, liststore):

        try:
            if self.ac_timeout_id:
                GObject.source_remove(self.ac_timeout_id)
                self.ac_timeout_id = 0
        except ValueError: pass
        except: pass

        if query and liststore: autocomplete(query, liststore)

        return True

    def on_entry_timeout(self, query, liststore):

        self.stop_ac_timeout(None, None)
        self.ac_timeout_id = GObject.timeout_add(300, lambda x: self.stop_ac_timeout(query, liststore), None)

        return True

    def on_autocomplete_search(self, completion, model, iter):

        self.webview.load_uri("{}{}".format(search_engine, model[iter][0]))

        return True

    def on_autocomplete_match(self, completion, model, iter):

        self.webview.load_uri(model[iter][1])

        return True

    def on_close_terminal(self, scrolled_window, widget):

        scrolled_window.get_children()[0].destroy()
        reveal(widget, False)

        return True

    def on_uri_changed(self, view, uri):

       url = view.get_uri()
       if url: self.main_url_entry.set_text(url)

       try:
           reveal(self.permission_revealer, False)
           reveal(self.cert_revealer, False)
       except: pass

       return True

    def on_go_back_press(self, widget, event):

        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1: self.timeout_id = GObject.timeout_add(500, self.on_go_back)
            if event.button == 3: self.on_go_back()

    def on_go_forward_press(self, widget, event):

        if event.type == Gdk.EventType.BUTTON_PRESS:
            if event.button == 1: self.timeout_id = GObject.timeout_add(500, self.on_go_forward)
            if event.button == 3: self.on_go_forward()

    def on_go_back(self):

        stop_timeout(self)
        timelist(0, self.webview, self.bflist, self.go_back,\
        15, 0.0, 0.5, self.link_hover, icns, self.is_defcon)

    def on_go_forward(self):

        stop_timeout(self)
        timelist(1, self.webview, self.bflist, self.go_forward,\
        15, 0.0, 0.5, self.link_hover, icns, self.is_defcon)

    def on_go_back_release(self, widget, event):

        stop_timeout(self)
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1: self.webview.go_back()

    def on_go_forward_release(self, widget, event):

        stop_timeout(self)
        if event.type == Gdk.EventType.BUTTON_RELEASE and event.button == 1: self.webview.go_forward()

    def on_allow(self, request):

        WebKit2.PermissionRequest.allow(request)
        reveal(self.permission_revealer, False)

        return True

    def on_deny(self, request):

        WebKit2.PermissionRequest.deny(request)
        reveal(self.permission_revealer, False)

        return True

    def on_permission_request(self, view, request):

        if type(request) == WebKit2.GeolocationPermissionRequest:

            if geolocation_policy == 0: request.allow()
            elif geolocation_policy == 1: request.deny()
            elif geolocation_policy == 2:

                self.perm_request = request
                self.permission_message.set_markup("<span size='small'>{}</span>"\
                .format(_("Give the approval for geolocation?")))

                self.permission_revealer.show_all()
                reveal(self.permission_revealer, True)

        return True

    def on_counted_matches(self, controller, count):

        self.controller.search(self.find_entry.get_text(), find, count)

        return True

    def on_close_finder(self):

        reveal(self.find_revealer, False)
        self.controller.search_finish()

        return True

    def on_favicon(self, view, event):

        icon = view.get_favicon()

        if icon:
            icon = Gdk.pixbuf_get_from_surface(icon, 0, 0, icon.get_width(), icon.get_height())
            self.main_url_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, icon)
        else: self.main_url_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, None)

        return True

    def on_mouse_target_changed(self, view, htr, mod):

        del mem_url[:]

        if view and htr.context_is_link():
            self.link_hover.set_text(minify(htr.get_link_uri(), 100))
            mem_url.append(htr.get_link_uri())
        else:
            self.link_hover.set_text("")
            mem_url.append("")

        return True

    def on_finder(self):

        self.controller.count_matches(self.find_entry.get_text(), find, 0)

        return True

    '''
    ###########
    # Methods #
    ###########
    '''

    def is_secure(self):

        if not validators.url(self.webview.get_uri()): return

        self.security = 0
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("{}ssl-tls-secure.svg".format(icns))
        self.main_url_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.SECONDARY, pixbuf)

        return True

    def is_nosecure(self):

        if not validators.url(self.webview.get_uri()): return

        self.security = 1
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("{}ssl-tls-nosecure.svg".format(icns))
        self.main_url_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.SECONDARY, pixbuf)

        return True

    def is_insecure(self):

        if not validators.url(self.webview.get_uri()): return

        self.security = 2
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("{}ssl-tls-insecure.svg".format(icns))
        self.main_url_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.SECONDARY, pixbuf)

        return True
                
'''
################
# Browser INIT #
################
'''

class Browser(Gtk.Window):
    def __init__(self, *args, **kwargs):
        super(Browser, self).__init__(*args, **kwargs)

        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file("{}poseidon-logo.svg".format(icns))
        self.set_icon(self.pixbuf)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(int(width), int(height))
        self.maximize()

        '''
        ##############
        # Header Bar #
        ##############
        '''

        headerbar = build_headerbar(browser_name, "headerbar", 1)
        headerbar.set_decoration_layout("menu:minimize,maximize,close")
        self.set_titlebar(headerbar)

        logo_button_hb = make_button(make_icon("poseidon-logo.png"), None, False)
        logo_button_hb.connect("clicked", self.on_logo)

        headerbar.pack_start(logo_button_hb)

        '''
        #############
        # Is Defcon #
        #############
        '''

        self.is_defcon = False

        try:

            if sys.argv[1] == "-i":
                headerbar.set_subtitle(_("Defcon Mode"))
                self.is_defcon = True

        except: pass

        '''
        ############
        # Notebook #
        ############
        '''

        self.current_page = 0

        notebook = Gtk.Notebook(name="notebook")
        notebook.set_scrollable(True)

        context = notebook.get_style_context()
        context.add_class("notebook")

        self.tabs = []
        
        if not tab_cb: self.tabs.append((self.create_tab(), Gtk.Label(tab_name)))

        if tab_cb:
            tab_box = make_tab_box(tab_name)
            page_tuple = (self.create_tab(), tab_box)
            self.tabs.append(page_tuple)

        notebook.append_page(*self.tabs[0])

        if tab_cb:
            for i in tab_box:
                if type(i) == gi.overrides.Gtk.Button:
                    i.connect("clicked", self.close_clicked_tab, page_tuple[0])

            self.sensitive_tab(False)

        addtab = make_button(make_icon("list-add.svg"), "{} [Ctrl+T]".format(_("Open a new tab")), False)
        addtab.connect("clicked", lambda x: self.open_new_tab())

        remtab = make_button(make_icon("list-remove.svg"), "{} [Ctrl+W]".format(_("Close current tab")), False)
        remtab.connect("clicked", lambda x: self.close_current_tab())
        remtab.set_sensitive(False)

        close = make_button(make_icon("close.svg"), None, False)
        close.connect("clicked", lambda x: quit(self))

        minimize = make_button(make_icon("minimize.svg"), None, False)
        minimize.connect("clicked", lambda x: self.iconify())

        maximize = make_button(make_icon("maximize.svg"), None, False)
        maximize.connect("clicked", lambda x: self.on_maximize())

        logo_button = make_button(make_icon("poseidon-logo.png"), None, False)
        logo_button.connect("clicked", self.on_logo)

        logo_menu = Gtk.PopoverMenu()
        logo_menu.set_position(Gtk.PositionType.BOTTOM)

        open_button = make_modelbutton_markup(_("Open"),\
        _("Open a file or import bookmarks"), 0.0, 0.5)
        open_button.connect("clicked", lambda x: self.open())

        save_button = make_modelbutton_markup(_("Save"),\
        _("Save a file, export bookmarks or save an HTML source file"), 0.0, 0.5)
        save_button.connect("clicked", lambda x: self.save())

        about_button = make_modelbutton("{} {} ...".format(_("About"), browser_name), 0.0, 0.5)
        about_button.connect("clicked", lambda x: self.on_about())

        logo_menu_grid = Gtk.Grid()
        logo_menu_grid.set_property("margin", 5)
        logo_menu_grid.attach(open_button, 0, 1, 1, 1)
        logo_menu_grid.attach(save_button, 0, 2, 1, 1)
        logo_menu_grid.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 3, 1, 1)
        logo_menu_grid.attach(about_button, 0, 4, 1, 1)
        logo_menu_grid.set_column_homogeneous(True)

        logo_menu.add(logo_menu_grid)

        action_box_logo = Gtk.HBox()
        action_box_logo.pack_start(logo_button, False, False, 0)
        action_box_logo.pack_start(Gtk.Separator.new(Gtk.Orientation.VERTICAL), False, False, 0)

        action_box_tabs = Gtk.HBox()
        action_box_tabs.pack_start(Gtk.Separator.new(Gtk.Orientation.VERTICAL), False, False, 0)
        action_box_tabs.pack_start(remtab, False, False, 0)
        action_box_tabs.pack_start(addtab, False, False, 0)

        action_box_wmgm = Gtk.HBox()
        action_box_wmgm.pack_start(Gtk.Separator.new(Gtk.Orientation.VERTICAL), False, False, 0)
        action_box_wmgm.pack_start(minimize, False, False, 0)
        action_box_wmgm.pack_start(maximize, False, False, 0)
        action_box_wmgm.pack_start(close, False, False, 0)

        action_box_tabs.pack_end(action_box_wmgm, False, False, 0)

        notebook.set_action_widget(action_box_logo, 0)
        notebook.set_action_widget(action_box_tabs, 1)

        action_box_logo.show_all()
        action_box_tabs.show_all()
        action_box_wmgm.show_all()

        self.add(notebook)

        self.connect("destroy", lambda x: quit(self))
        self.connect("key-press-event", self.on_key_pressed)
        self.connect("button-press-event", self.on_key_pressed)
        self.connect("window-state-event", self.on_window_state)
        notebook.connect("switch-page", self.on_tab_changed)

        self.focus_tab()

        notebook.show()

        '''
        ######################
        # Set Cookies Policy #
        ######################
        '''

        if not self.is_defcon:

            manager = web_context.get_cookie_manager()
            manager.set_accept_policy(cookies_policy)
            manager.set_persistent_storage("{}/{}".format(cookies_path, cookies_db), WebKit2.CookiePersistentStorage.SQLITE)

            self.cache_path = self.tabs[self.current_page][0].cache_path

        '''
        ##################
        # Bookmarks Menu #
        ##################
        '''

        bookmarks_menu = Gtk.Popover()
        bookmarks_menu.set_position(Gtk.PositionType.BOTTOM)
        bookmarks_menu.connect("closed", lambda x: self.on_menu_closed(3))

        bkscroll = Gtk.ScrolledWindow()
        bkscroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        bkview = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        bkaddbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        bkadd = Gtk.ModelButton()
        bkadd.set_alignment(0.5, 0.5)
        bkadd.set_label(_("Add this page to bookmarks"))
        bkadd.connect("clicked", lambda x: self.view_bookmarks(None, None))

        bkaddbox.add(bkadd)
        bkscroll.add(bkview)

        bkgrid = Gtk.Grid()
        bkgrid.attach(bkaddbox, 0, 1, 1, 1)

        bookmarks_menu.add(bkgrid)
        
        '''
        #################
        # Download Menu #
        #################
        '''

        downloads_menu = Gtk.Popover()
        downloads_menu.set_position(Gtk.PositionType.BOTTOM)
        downloads_menu.connect("closed", lambda x: self.on_menu_closed(2))

        dlscroll = Gtk.ScrolledWindow()
        dlview = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        dlscroll.add(dlview)
        downloads_menu.add(dlscroll)

        web_context.connect("download-started", self.on_download_started)

        '''
        ##############
        # Tools Menu #
        ##############
        '''

        tools_menu = Gtk.PopoverMenu()
        tools_menu.set_position(Gtk.PositionType.BOTTOM)
        tools_menu.connect("closed", lambda x: self.on_menu_closed(1))

        menu = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        utilities_menu = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        tools_menu.add(menu)
        tools_menu.get_child().add(utilities_menu)
        tools_menu.child_set_property(utilities_menu, "submenu", "utilities-menu")

        new_window_button = make_modelbutton(_("New Window"), 0.0, 0.5)
        new_window_button.connect("clicked", lambda x: self.open_new_window())
        new_window_label = make_modelbutton_label("[ Ctrl+N ]", 0.95, 0.5)

        defcon_button = make_modelbutton(_("Defcon Mode"), 0.0, 0.5)
        defcon_button.connect("clicked", lambda x: self.defcon())
        defcon_label = make_modelbutton_label("[ Ctrl+I ]", 0.95, 0.5)

        settings_button = make_modelbutton(_("Settings"), 0.0, 0.5)
        settings_button.connect("clicked", lambda x: self.view_settings())
        settings_label = make_modelbutton_label("[ Ctrl+S ]", 0.95, 0.5)

        finder_button = make_modelbutton(_("Finder"), 0.0, 0.5)
        finder_button.connect("clicked", lambda x: self.finder())
        finder_label = make_modelbutton_label("[ Ctrl+F ]", 0.95, 0.5)

        zoom_in_button = make_modelbutton(_("Zoom In"), 0.0, 0.5)
        zoom_in_button.connect("clicked", lambda x: self.zoom_in())
        zoom_in_label = make_modelbutton_label("[ Ctrl+ ]", 0.95, 0.5)

        zoom_out_button = make_modelbutton(_("Zoom Out"), 0.0, 0.5)
        zoom_out_button.connect("clicked", lambda x: self.zoom_out())
        zoom_out_label = make_modelbutton_label("[ Ctrl- ]", 0.95, 0.5)

        zoom_restore_button = make_modelbutton(_("Zoom Restore"), 0.0, 0.5)
        zoom_restore_button.connect("clicked", lambda x: self.zoom_restore())
        zoom_restore_label = make_modelbutton_label("[ Ctrl+M ]", 0.95, 0.5)

        print_button = make_modelbutton(_("Print"), 0.0, 0.5)
        print_button.connect("clicked", lambda x: self.page_print())
        print_label = make_modelbutton_label("[ Ctrl+P ]", 0.95, 0.5)

        adke_label_text = "\r<span size='small'>{}</span>\r<span size='x-small'>{}</span>\r"\
        .format("AdKiller", _("AdKiller is enabled"))

        adkd_label_text = "\r<span size='small'>{}</span>\r<span size='x-small'>{}</span>\r"\
        .format("AdKiller", _("AdKiller is disabled"))

        adk_label = make_label(0.0, 0.5)
        adk_label.set_markup(adke_label_text)

        adk_switch = Gtk.Switch()
        adk_switch.props.halign = Gtk.Align.CENTER
        adk_switch.set_active(True)
        adk_switch.connect("notify::active", self.on_adk_switch)

        if not adkiller:

            adk_label.set_markup(adkd_label_text)
            adk_label.set_sensitive(False)
            adk_switch.set_sensitive(False)
            adk_switch.set_active(False)

        sec_label_text = "\r<span size='small'>{}</span>\r<span size='x-small'>{}</span>\r"\
        .format(_("SSL Navigation Secure"), _("SNS is enabled"))

        isec_label_text = "\r<span size='small'>{}</span>\r<span size='x-small'>{}</span>\r"\
        .format(_("SSL Navigation Secure"), _("SNS is disabled"))

        sec_label = make_label(0.0, 0.5)
        sec_label.set_markup(sec_label_text)

        sec_switch = Gtk.Switch()
        sec_switch.props.halign = Gtk.Align.CENTER
        sec_switch.set_active(True)
        sec_switch.connect("notify::active", self.on_sec_switch)

        if not verify_req:

            sec_label.set_markup(isec_label_text)
            sec_label.set_sensitive(False)
            sec_switch.set_sensitive(False)
            sec_switch.set_active(False)
            self.tlsbool = False

        else: self.tlsbool = True

        jse_label_text = "\r<span size='small'>{}</span>\r<span size='x-small'>{}</span>\r"\
        .format("No-Script", _("Javascript is enabled"))

        jsd_label_text = "\r<span size='small'>{}</span>\r<span size='x-small'>{}</span>\r"\
        .format("No-Script", _("Javascript is disabled"))

        js_label = make_label(0.0, 0.5)
        js_label.set_markup(jse_label_text)

        js_switch = Gtk.Switch()
        js_switch.props.halign = Gtk.Align.CENTER
        js_switch.set_active(True)
        js_switch.connect("notify::active", self.on_js_switch)

        if not set_enable_javascript:

            js_label.set_markup(jsd_label_text)
            js_label.set_sensitive(False)
            js_switch.set_sensitive(False)
            js_switch.set_active(False)

        pge_label_text = "\r<span size='small'>{}</span>\r<span size='x-small'>{}</span>\r"\
        .format("No-Plugins", _("Plugins are enabled"))

        pgd_label_text = "\r<span size='small'>{}</span>\r<span size='x-small'>{}</span>\r"\
        .format("No-Plugins", _("Plugins are disabled"))

        pg_label = make_label(0.0, 0.5)
        pg_label.set_markup(pge_label_text)

        pg_switch = Gtk.Switch()
        pg_switch.props.halign = Gtk.Align.CENTER
        pg_switch.set_active(True)
        pg_switch.connect("notify::active", self.on_pg_switch)

        if not set_enable_plugins:

            pg_label.set_markup(pgd_label_text)
            pg_label.set_sensitive(False)
            pg_switch.set_sensitive(False)
            pg_switch.set_active(False)

        utilities_button = make_modelbutton(_("Utilities"), 0.0, 0.5)
        utilities_button.set_property("menu-name", "utilities-menu")

        back_main_button = make_modelbutton(_("Back to main menu"), 1.0, 0.5)
        back_main_button.set_property("menu-name", "main")
        back_main_button.set_property("inverted", True)

        quit_button = make_modelbutton("{} {}".format(_("Quit"), browser_name), 0.0, 0.5)
        quit_button.connect("clicked", lambda x: quit(self))
        quit_label = make_modelbutton_label("[ Ctrl+Q ]", 0.95, 0.5)

        fullscreen_button = make_modelbutton(_("Go Fullscreen"), 0.0, 0.5)
        fullscreen_button.connect("clicked", lambda x: self.go_fullscreen())
        fullscreen_label = make_modelbutton_label("[ F11 ]", 0.95, 0.5)

        del_theme_button = make_modelbutton(_("Delete Theme"), 0.0, 0.5)
        del_theme_button.connect("clicked", lambda x: self.delete_theme())
        del_theme_label = make_modelbutton_label("[ Ctrl+K ]", 0.95, 0.5)

        pass_gen_button = make_modelbutton(_("Password Generator"), 0.0, 0.5)
        pass_gen_button.connect("clicked", lambda x: pass_generator(self))
        pass_gen_label = make_modelbutton_label("[ Ctrl+J ]", 0.95, 0.5)

        usagent_button = make_modelbutton("User Agent Switcher", 0.0, 0.5)
        usagent_button.connect("clicked", lambda x: user_agent(self))
        usagent_label = make_modelbutton_label("[ Ctrl+G ]", 0.95, 0.5)

        if webkit_ver > wk16:

            proxy_button = make_modelbutton(_("Proxy Manager"), 0.0, 0.5)
            proxy_button.connect("clicked", lambda x: proxy(self))
            proxy_label = make_modelbutton_label("[ Ctrl+X ]", 0.95, 0.5)

        vte_button = make_modelbutton(_("VTE Terminal"), 0.0, 0.5)
        vte_button.connect("clicked", lambda x: self.vte())
        vte_label = make_modelbutton_label("[ F4 ]", 0.95, 0.5)

        plugins_button = make_modelbutton(_("View Plugins"), 0.0, 0.5)
        plugins_button.connect("clicked", lambda x: self.view_plugins())
        plugins_label = make_modelbutton_label("[ Ctrl+B ]", 0.95, 0.5)

        source_button = make_modelbutton(_("View Source"), 0.0, 0.5)
        source_button.connect("clicked", lambda x: self.view_source())
        source_label = make_modelbutton_label("[ Ctrl+U ]", 0.95, 0.5)

        history_button = make_modelbutton(_("View History"), 0.0, 0.5)
        history_button.connect("clicked", lambda x: self.view_history())
        history_label = make_modelbutton_label("[ Ctrl+H ]", 0.95, 0.5)

        bookmarks_button = make_modelbutton(_("View Bookmarks"), 0.0, 0.5)
        bookmarks_button.connect("clicked", lambda x: self.view_bookmarks(None, None))
        bookmarks_label = make_modelbutton_label("[ Ctrl+D ]", 0.95, 0.5)

        manager_cookies_button = make_modelbutton(_("Cookies Manager"), 0.0, 0.5)
        manager_cookies_button.connect("clicked", lambda x: self.cookies_manager())
        manager_cookies_label = make_modelbutton_label("[ Ctrl+O ]", 0.95, 0.5)

        delete_cache_button = make_modelbutton(_("Empty Cache"), 0.0, 0.5)
        delete_cache_button.connect("clicked", lambda x: web_context.clear_cache())
        delete_cache_label = make_label(0.95, 0.5)

        grid_buttons = Gtk.Grid()
        grid_buttons.set_column_spacing(10)
        grid_buttons.attach(new_window_button, 0, 0, 1, 1)
        grid_buttons.attach(new_window_label, 0, 0, 1, 1)
        grid_buttons.attach(defcon_button, 0, 1, 1, 1)
        grid_buttons.attach(defcon_label, 0, 1, 1, 1)
        grid_buttons.attach(settings_button, 0, 2, 1, 1)
        grid_buttons.attach(settings_label, 0, 2, 1, 1)
        grid_buttons.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 3, 1, 1)
        grid_buttons.attach(print_button, 0, 4, 1, 1)
        grid_buttons.attach(print_label, 0, 4, 1, 1)
        grid_buttons.attach(finder_button, 0, 5, 1, 1)
        grid_buttons.attach(finder_label, 0, 5, 1, 1)
        grid_buttons.attach(zoom_in_button, 0, 6, 1, 1)
        grid_buttons.attach(zoom_in_label, 0, 6, 1, 1)
        grid_buttons.attach(zoom_out_button, 0, 7, 1, 1)
        grid_buttons.attach(zoom_out_label, 0, 7, 1, 1)
        grid_buttons.attach(zoom_restore_button, 0, 8, 1, 1)
        grid_buttons.attach(zoom_restore_label, 0, 8, 1, 1)
        grid_buttons.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 9, 1, 1)
        grid_buttons.attach(utilities_button, 0, 10, 1, 1)
        grid_buttons.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 11, 1, 1)
        grid_buttons.set_column_homogeneous(True)

        grid_switches = Gtk.Grid()
        grid_switches.set_column_spacing(10)
        grid_switches.attach(adk_label, 0, 0, 1, 1)
        grid_switches.attach(adk_switch, 0, 1, 1, 1)
        grid_switches.attach(sec_label, 1, 0, 1, 1)
        grid_switches.attach(sec_switch, 1, 1, 1, 1)
        grid_switches.attach(js_label, 0, 2, 1, 1)
        grid_switches.attach(js_switch, 0, 3, 1, 1)
        grid_switches.attach(pg_label, 1, 2, 1, 1)
        grid_switches.attach(pg_switch, 1, 3, 1, 1)
        grid_switches.set_column_homogeneous(True)

        grid_utilities = Gtk.Grid()
        grid_utilities.set_column_spacing(10)
        grid_utilities.attach(fullscreen_button, 0, 0, 1, 1)
        grid_utilities.attach(fullscreen_label, 0, 0, 1, 1)
        grid_utilities.attach(quit_button, 0, 1, 1, 1)
        grid_utilities.attach(quit_label, 0, 1, 1, 1)
        grid_utilities.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 2, 1, 1)
        grid_utilities.attach(del_theme_button, 0, 3, 1, 1)
        grid_utilities.attach(del_theme_label, 0, 3, 1, 1)
        grid_utilities.attach(pass_gen_button, 0, 4, 1, 1)
        grid_utilities.attach(pass_gen_label, 0, 4, 1, 1)
        grid_utilities.attach(usagent_button, 0, 5, 1, 1)
        grid_utilities.attach(usagent_label, 0, 5, 1, 1)

        if webkit_ver > wk16:

            grid_utilities.attach(proxy_button, 0, 6, 1, 1)
            grid_utilities.attach(proxy_label, 0, 6, 1, 1)

        grid_utilities.attach(vte_button, 0, 7, 1, 1)
        grid_utilities.attach(vte_label, 0, 7, 1, 1)
        grid_utilities.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 8, 1, 1)
        grid_utilities.attach(plugins_button, 0, 9, 1, 1)
        grid_utilities.attach(plugins_label, 0, 9, 1, 1)
        grid_utilities.attach(source_button, 0, 10, 1, 1)
        grid_utilities.attach(source_label, 0, 10, 1, 1)
        grid_utilities.attach(history_button, 0, 11, 1, 1)
        grid_utilities.attach(history_label, 0, 11, 1, 1)
        grid_utilities.attach(bookmarks_button, 0, 12, 1, 1)
        grid_utilities.attach(bookmarks_label, 0, 12, 1, 1)
        grid_utilities.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 13, 1, 1)
        grid_utilities.attach(manager_cookies_button, 0, 14, 1, 1)
        grid_utilities.attach(manager_cookies_label, 0, 14, 1, 1)
        grid_utilities.attach(delete_cache_button, 0, 15, 1, 1)
        grid_utilities.attach(delete_cache_label, 0, 15, 1, 1)
        grid_utilities.attach(Gtk.Separator.new(Gtk.Orientation.HORIZONTAL), 0, 16, 1, 1)
        grid_utilities.attach(back_main_button, 0, 17, 1, 1)
        grid_utilities.set_column_homogeneous(True)

        menu.pack_start(grid_buttons, False, False, 0)
        menu.pack_start(grid_switches, False, False, 10)
        utilities_menu.pack_start(grid_utilities, False, False, 0)

        '''
        #####################
        # Fullscreen Window #
        #####################
        '''

        fs_win = Gtk.Window()
        fs_win.set_title(browser_name)
        fs_win.set_skip_taskbar_hint(True)
        fs_win.set_decorated(False)
        fs_win.set_keep_above(True)
        fs_win.set_modal(True)
        fs_win.set_transient_for(self)
        fs_win.fullscreen()

        '''
        #########
        # Props #
        #########
        '''

        bkscroll.set_property('margin', 15)
        bkaddbox.set_property('margin', 5)
        dlscroll.set_property('margin', 15)
        dlview.set_property('margin-right', 5)
        menu.set_property('margin', 15)
        utilities_menu.set_property('margin', 15)

        '''
        ###########
        # Selfize #
        ###########
        '''

        self.is_fullscreen = False
        self.is_human_choice = bool()

        self.remtab = remtab
        self.headerbar = headerbar
        self.notebook = notebook
        self.bkview = bkview
        self.bkscroll = bkscroll
        self.bkgrid = bkgrid
        self.bookmarks_menu = bookmarks_menu
        self.dlview = dlview
        self.dlscroll = dlscroll
        self.downloads_menu = downloads_menu
        self.adke_label_text = adke_label_text
        self.adkd_label_text = adkd_label_text
        self.adk_label = adk_label
        self.adk_switch = adk_switch
        self.sec_label = sec_label
        self.sec_label_text = sec_label_text
        self.isec_label_text = isec_label_text
        self.sec_switch = sec_switch
        self.jse_label_text = jse_label_text
        self.jsd_label_text = jsd_label_text
        self.js_label = js_label
        self.js_switch = js_switch
        self.pge_label_text = pge_label_text
        self.pgd_label_text = pgd_label_text
        self.pg_label = pg_label
        self.pg_switch = pg_switch
        self.zoom_restore_button = zoom_restore_button
        self.source_button = source_button
        self.tools_menu = tools_menu
        self.open_button = open_button
        self.save_button = save_button
        self.del_theme_button = del_theme_button
        self.fs_win = fs_win
        self.delete_cache_label = delete_cache_label
        self.finder_button = finder_button
        self.print_button = print_button
        self.zoom_in_button = zoom_in_button
        self.zoom_out_button = zoom_out_button
        self.vte_button = vte_button
        self.logo_menu = logo_menu
        self.action_box_logo = action_box_logo
        self.action_box_wmgm = action_box_wmgm

        self.update_status()
        self.show()

        try:
            if sys.argv[1] and not sys.argv[1] == "-i": self.on_load_url(sys.argv[1])
        except: pass

        '''
        ###############
        # Check Proxy #
        ###############
        '''

        if webkit_ver > wk16:

            db = self.get_proxy()

            if db:
                if db[1] != "socks": tp = 1
                else: tp = 0
                if db[0] != str(1): self.set_proxy(db[0], db[2], db[3], tp)

    '''
    ###########
    # Signals #
    ###########
    '''

    def create_tab(self):

        if self.is_defcon: tab = BrowserTab(name="defcon")
        else: tab = BrowserTab()

        tab.webview.connect("load-changed", self.on_load_changed)
        tab.webview.connect("context-menu", self.on_context_menu)
        tab.webview.connect("context-menu-dismissed", self.on_context_menu_dismissed)  
        tab.webview.connect("notify::title", self.on_title_changed)
        tab.webview.connect("decide-policy", self.on_decide_policy)
        tab.webview.connect("enter-fullscreen", self.on_enter_fullscreen)
        tab.webview.connect("leave-fullscreen", self.on_leave_fullscreen)
        tab.webview.connect("load-failed", self.on_load_failed)
        tab.webview.connect("load-failed-with-tls-errors", self.on_load_failed_with_tls_errors) 
        tab.webview.connect("create", self.on_create)
        tab.webview.connect("button-press-event", self.on_button_press)
        if tab_cb: tab.webview.connect("notify::is-playing-audio", self.on_playing_audio)
        tab.download_button.connect("clicked", lambda x: self.on_download_menu())
        tab.bookmarks_button.connect("clicked", lambda x: self.on_bookmarks_menu())
        tab.tools.connect("clicked", lambda x: self.on_tools_menu())
        tab.go_button.connect("clicked", self.on_load_url)
        tab.main_url_entry.connect("activate", self.on_load_url)
        tab.iconified_vte.connect("button-press-event", lambda x, y: [self.vte(), tab.iconified_vte.hide()])
        tab.main_url_entry.connect("icon-press", self.on_icon_pressed)
        tab.allow_cert_button.connect("clicked", lambda x: self.cert())

        global init_home_page

        if home_page and init_home_page != 0:

            if init_home_page == 1:
                tab.webview.load_uri(home_page)
                init_home_page = 0

            if init_home_page == 2: tab.webview.load_uri(home_page)

        return tab

    def on_window_state(self, widget, event):

        state = event.window.get_state()
        opts = Gdk.WindowState.FULLSCREEN | Gdk.WindowState.MAXIMIZED
        if (state & opts):
            self.headerbar.hide()
            self.action_box_wmgm.show_all()
            self.action_box_logo.show_all()
        else:
            self.headerbar.show_all()
            self.action_box_wmgm.hide()
            self.action_box_logo.hide()

    def on_playing_audio(self, view, boolean):

        for tab, widget in self.tabs:

            widget = self.check_tab(widget, 1)

            if tab.webview is view:
                if widget:
                    if view.is_playing_audio(): widget.show()
                    else: widget.hide()

    def on_button_press(self, view, event):

        if event.get_state() & Gdk.ModifierType.CONTROL_MASK\
        and event.button == Gdk.BUTTON_PRIMARY:
            if mem_url[0]:
                self.open_blank(mem_url[0])
                return True

        if event.type == Gdk.EventType.BUTTON_PRESS:

            if links_policy and event.button == Gdk.BUTTON_PRIMARY\
            and mem_url[0]:
                self.open_blank(mem_url[0])
                return True

            if event.button == 8: view.go_back()
            if event.button == 9: view.go_forward()

    def on_restore_settings(self):

        decision = dialog().decision(_("Are you sure?"), "<span size='small'>{}.</span>"\
        .format(_("Clicking on OK, all settings will be restored to default and browser will restart")))

        if decision:
            restore_db()
            self.restart()

    def on_save_settings(self, opts):

        with settings_con:    
            cur = settings_con.cursor()
            for i in opts:
                if type(i) == Gtk.Entry: value = i.get_text()
                if type(i) == Gtk.ComboBoxText: value = i.get_active()

                cur.execute("UPDATE settings SET value=? WHERE option=?;",(value, i.get_name(),))

        decision = dialog().decision(_("Are you sure?"), "<span size='small'>{}.</span>"\
        .format(_("Clicking on OK, all edited settings will be saved and browser will restart")))

        if decision: self.restart()

    def on_vte_button_press(self, widget, event):

        if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 3: vte_menu(widget)

    def on_menu_closed(self, int):
        
        page = self.tabs[self.current_page][0]
        if int == 1: button = page.tools
        if int == 2: button = page.download_button
        if int == 3: button = page.bookmarks_button
        button.set_active(False)

    def on_logo(self, widget):

        self.logo_menu.set_relative_to(widget)
        self.logo_menu.show_all()

        return True

    def on_about(self):

        ver = WebKit2.get_major_version(), WebKit2.get_minor_version(), WebKit2.get_micro_version()
        ver = str(ver).replace("(", "").replace(")", "").replace(", ", ".")

        dialog().about(self, self.pixbuf, ver)

        return True

    def on_leave_fullscreen(self, view):

        view.reparent(self.tabs[self.current_page][0].scrolled_window)
        self.fs_win.hide()

    def on_enter_fullscreen(self, view):

        view.reparent(self.fs_win)
        self.fs_win.show_all()

        scrolled_window = self.tabs[self.current_page][0].scrolled_window
        scrolled_window.remove(scrolled_window.get_children()[0])

    def on_timeout(self, view, event, url):
        
        view.stop_loading()
        stop_timeout(self)

        error = catch_error(url, self.tlsbool, self.p_req())

        if type(error) == requests.exceptions.SSLError: self.on_load_failed_with_tls_errors(view, url, None, None)
        else: self.on_load_failed(view, event, url, None)
 
        return True

    def on_load_changed(self, view, event):

        page = self.tabs[self.current_page][0]
        url = view.get_uri()
        title = view.get_title()
        self.dynamic_title(view, title)

        if event == WebKit2.LoadEvent.STARTED:

            if int(load_timeout) != 0:
                stop_timeout(self)
                self.timeout_id = GObject.timeout_add(int(load_timeout), lambda x: self.on_timeout(view, event, url), None)

            if not verify_req: web_context.set_tls_errors_policy(WebKit2.TLSErrorsPolicy.IGNORE)

            page.refresh.hide()
            page.cancel.show()

        if event == WebKit2.LoadEvent.COMMITTED:

            if view.get_tls_info()[0]: page.is_secure()
            else: page.is_nosecure()

        if event == WebKit2.LoadEvent.FINISHED:

            if int(load_timeout) != 0: stop_timeout(self)

            page.refresh.show()
            page.cancel.hide()

            if os.path.exists("{}{}".format(history_path, history_db)) and validators.url(url):

                view.grab_focus()

                if self.is_defcon == False:

                    with history_con:
                        cur = history_con.cursor()

                        if not title: title = get_domain(url)

                        today = datetime.date.today()
                        cur.execute("INSERT INTO history VALUES(?, ?, ?);", (title, url, time.strftime("%Y-%m-%d %H:%M")))
                        cur.execute("DELETE FROM history WHERE date < datetime(?, '-7 days');", (today,))
                        history_con.commit()

        self.update_status()

        return True

    def on_load_failed(self, view, event, failing_uri, error):

        if type(error) == GLib.GError:
            if not error.code == 2: return True

        elif type(error) == int: return True

        dialog().error(_("Connection Failed"), "<span size='small'>\"<b>{}</b>\" {}.\n\n{}.\n{}.</span>"\
        .format(minify(failing_uri, 50), _("seems to be not available"),\
        _("It may be temporarily unavailable or moved to a new address"),\
        _("You may also wish to verify that your internet connection is working correctly")))

        return True

    def on_load_failed_with_tls_errors(self, view, failing_uri, certificate, errors):

        if web_context.get_tls_errors_policy() == WebKit2.TLSErrorsPolicy.FAIL:

            decision = dialog().decision(_("Invalid Certificate"), "<span size='small'>\"<b>{}</b>\" {}.\n\n{}.\n\n{}.</span>"\
            .format(minify(failing_uri, 50), _("seems to be an insecure website"),\
            _("If you think this website do NOT represent a menace for you then click on OK"),\
            _("Note: Clicking on OK, 'SSL Secure Navigation' will be disabled but you can re-enable it back from browser menu")))

            if decision:
                self.sec_switch.set_active(False)
                self.tabs[self.current_page][0].webview.load_uri(failing_uri)

            return True

    def on_load_url(self, widget):

        page = self.tabs[self.current_page][0]
        pt = "http://"
        pts = "https://"

        if type(widget) == str: url = widget
        else: url = page.main_url_entry.get_text()

        if url == "about:settings":
            self.view_settings()
            return True

        if url == "about:plugins":
            self.view_plugins()
            return True

        if url == "about:bookmarks":
            self.view_bookmarks(None, None)
            return True

        if url == "about:history":
            self.view_history()
            return True

        if url == "about:cookies":
            self.cookies_manager()
            return True

        if url == "localhost" or "://localhost" in url:
            if https_redirect: pt = pts
            page.webview.load_uri("{}{}".format(pt, local_ip))
            return True

        format = "{}{}".format(pt, parse(url))
        sec_format = "{}{}".format(pts, parse(url))

        if not url: return True

        if url.startswith("file://"):
            page.webview.load_uri(url)
            return True

        if url.startswith("ftp.") or url.startswith("www."):
            if https_redirect: pt = pts
            page.webview.load_uri("{}{}".format(pt, url))
            return True

        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", url):
            page.webview.load_uri(format)
            return True

        if validators.url(url):
            if https_redirect:
                if url.startswith(pt): url = url.replace(pt, pts)
            page.webview.load_uri(url)
            return True

        else:
            if validators.url(format):
                if is_url_valid(format, self.tlsbool, self.p_req()):
                    if https_redirect: page.webview.load_uri(sec_format)
                    else: page.webview.load_uri(format)
                else: self.try_search(parse(url))
            else: self.try_search(parse(url))

    def on_click_bookmark(self, button, event):

        self.bookmarks_menu.hide()
        self.tabs[self.current_page][0].webview.load_uri(button.get_name())

        return True

    def on_iter_clicked(self, view, iter, column):

        url = view.get_model()[iter][3]
        if url: self.open_blank(url)

        return True

    def on_add_bookmarks(self, title_entry, url_entry):

        url = url_entry.get_text()
        title = title_entry.get_text()
        if not title or not url: return True
        self.on_insert_bookmarks(title, url)

    def on_insert_bookmarks(self, title, url):

        with bookmarks_con:    
            cur = bookmarks_con.cursor()
            cur.execute("SELECT * FROM bookmarks;")
            urls = cur.fetchall()

            if len(urls) != 0:
                for i in urls:
                    if url == i[1]:
                        return True

            cur.execute("INSERT INTO bookmarks VALUES(?, ?, ?);",\
            (title.replace("\n","").strip(), url, time.strftime("%Y-%m-%d %H:%M")))

            self.refresh_liststore(1)

            return True

    def on_rem_bookmarks(self, selection):

        (model, iter) = selection.get_selected()
        if iter is not None: self.on_erase_bookmarks(model[iter][3])

    def on_erase_bookmarks(self, url):

        with bookmarks_con:
            cur = bookmarks_con.cursor()
            cur.execute("SELECT * FROM bookmarks;")
            urls = cur.fetchall()

            if len(urls) != 0:
                for i in urls:
                    if url == i[1]:
                        cur.execute("DELETE FROM bookmarks WHERE url=?;", (url,))
                        bookmarks_con.commit()

                        self.refresh_liststore(1)

                        return True

    def on_bookmarks_selected(self, selection):

        (model, iter) = selection.get_selected()

        if iter is not None:

            self.entry_title_bookmarks.set_text(model[iter][1])
            self.entry_url_bookmarks.set_text(model[iter][3])

        self.rem_bookmarks_button.set_sensitive(True)

        return True

    def on_clear_bookmarks(self):

        with bookmarks_con:
            cur = bookmarks_con.cursor()   
            cur.execute("DROP TABLE IF EXISTS bookmarks;")
            cur.execute("CREATE TABLE bookmarks(title TEXT, url TEXT, date TEXT);")

        self.refresh_liststore(1)

        return True

    def on_bookmarks_history(self, selection):

        (model, iter) = selection.get_selected()

        if iter is not None:

            try:
                title = model[iter][1]
                url = model[iter][3]
            except: title, url = (None, None)

            self.view_bookmarks(title, url)

            return True

    def on_bookmarks_menu(self):

        for i in self.bkview:
            if i: self.bkview.remove(i)

        bookmarks = bookmarksview()

        for i in bookmarks:

            icon = Gtk.Image()
            icon.set_from_file("{}text-x-generic.svg".format(icns))

            if not self.is_defcon and icons_pop:
                favicon = get_favicon(self.tabs[self.current_page][0].webview, i[3], (16, 16))
                if favicon: icon.set_from_pixbuf(favicon)

            item = Gtk.ModelButton(name=i[3])
            item.set_alignment(0.0, 0.5)
            item.set_label("<span size='small'>{}</span>\r<span size='x-small'>{}</span>".\
            format(html.escape(minify(i[1], 50)), html.escape(i[2])))
            item.get_child().set_use_markup(True)
            item.get_child().set_padding(5, 5)
            item.set_hexpand(True)
            item.connect("button-press-event", self.on_click_bookmark)

            grid_bookmarks = Gtk.Grid()
            grid_bookmarks.set_column_spacing(10)
            grid_bookmarks.attach(icon, 0, 1, 1, 1)
            grid_bookmarks.attach(item, 1, 1, 1, 1)
            grid_bookmarks.set_column_homogeneous(False)

            self.bkview.add(grid_bookmarks)

        if len(self.bkview) != 0:

            if len(self.bkgrid) == 1: self.bkgrid.attach(self.bkscroll, 0, 0, 1, 1)

            if len(self.bkview) < 7:
                self.bkscroll.set_size_request(200, 0)
                self.bkscroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
            if len(self.bkview) >= 7:
                self.bkscroll.set_size_request(200, 300)
                self.bkscroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        else: self.bkgrid.remove(self.bkscroll)

        self.bookmarks_menu.set_relative_to(self.tabs[self.current_page][0].bookmarks_button)
        self.bookmarks_menu.show_all()

    def on_download_menu(self):

        page = self.tabs[self.current_page][0]
        button = page.download_button
        button.set_image(page.download_icon)

        for i, item in enumerate(self.tabs):
            self.tabs[i][0].download_button.\
            set_image(self.tabs[i][0].download_icon)

        if self.dlview.get_children():

            if len(self.dlview) < 7:
                self.dlscroll.set_size_request(200, 0)
                self.dlscroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
            if len(self.dlview) >= 7:
                self.dlscroll.set_size_request(200, 300)
                self.dlscroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

            self.downloads_menu.set_relative_to(button)
            self.downloads_menu.show_all()

        else: button.set_active(False)

    def on_cookies_selected(self, selection):

        (model, iter) = selection.get_selected()

        if iter is not None:

            self.name_obj.get_children()[0].set_text(model[iter][1])
            self.value_obj.get_children()[0].set_text(model[iter][9])
            self.host_obj.get_children()[0].set_text(model[iter][3])
            self.path_obj.get_children()[0].set_text(model[iter][4])
            self.expiry_obj.get_children()[0].set_text(str(model[iter][5]))
            self.lastacc_obj.get_children()[0].set_text(str(model[iter][6]))
            self.issec_obj.get_children()[0].set_text(str(model[iter][7]))
            self.ishttp_obj.get_children()[0].set_text(str(model[iter][8]))

        self.rem_cookies_button.set_sensitive(True)
        self.edit_cookies_button.set_sensitive(True)
        self.add_cookies_button.set_sensitive(True)

        return True

    def on_clear_cookies(self):

        with cookies_con:
            cur = cookies_con.cursor()   
            cur.execute("DROP TABLE IF EXISTS moz_cookies;")
            cur.execute("CREATE TABLE moz_cookies (id INTEGER PRIMARY KEY, name TEXT, value TEXT, host TEXT, path TEXT,\
            expiry INTEGER, lastAccessed INTEGER, isSecure INTEGER, isHttpOnly INTEGER);")

        self.refresh_liststore(2)

        return True

    def on_rem_cookies(self, selection):

        (model, iter) = selection.get_selected()

        if iter is not None:

            with cookies_con:
                cur = cookies_con.cursor()
                cur.execute("DELETE FROM moz_cookies WHERE id=?;", (model[iter][0],))
                cookies_con.commit()

                self.refresh_liststore(2)

                return True

    def on_edit_cookies(self, selection, action):

        (model, iter) = selection.get_selected()

        if iter is not None:

            if not action: id = model[iter][0]
            else: id = None

            name = self.name_obj.get_children()[0].get_text()
            value = self.value_obj.get_children()[0].get_text()
            host = self.host_obj.get_children()[0].get_text()
            path = self.path_obj.get_children()[0].get_text()
            expiry = self.expiry_obj.get_children()[0].get_text()
            lastacc = self.lastacc_obj.get_children()[0].get_text()
            issec = self.issec_obj.get_children()[0].get_text()
            ishttp = self.ishttp_obj.get_children()[0].get_text()

            if expiry and lastacc and issec and ishttp:
                with cookies_con:
                    cur = cookies_con.cursor()

                    if action: cur.execute("INSERT INTO moz_cookies VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);",\
                    (id,name,value,host,path,expiry,lastacc,issec,ishttp,))
                    else: cur.execute("UPDATE moz_cookies SET name=?,value=?,host=?,path=?,expiry=?,lastAccessed=?,isSecure=?,isHttpOnly=? WHERE id=?;",\
                    (name,value,host,path,expiry,lastacc,issec,ishttp,id,))

                    cookies_con.commit()
                    self.refresh_liststore(2)

        return True

    def on_history_selected(self, selection):

        self.bookmarks_history_button.set_sensitive(True)

        return True

    def on_clear_history(self):

        with history_con:
            cur = history_con.cursor()   
            cur.execute("DROP TABLE IF EXISTS history;")
            cur.execute("CREATE TABLE history(title TEXT, url TEXT, date TEXT);")

        self.refresh_liststore(3)

        return True

    def on_adk_switch(self, button, active):

        if not adkiller: return True

        page = self.tabs[self.current_page][0]

        if button.get_active():
            write_file(adk_file, "1")
            self.adk_label.set_markup(self.adke_label_text)
        else:
            write_file(adk_file, "0")
            self.adk_label.set_markup(self.adkd_label_text)

        url = page.webview.get_uri()
        if url and validators.url(url): page.webview.reload()

    def on_sec_switch(self, button, active):

        if not verify_req: return True

        if button.get_active():
            web_context.set_tls_errors_policy(WebKit2.TLSErrorsPolicy.FAIL)
            self.sec_label.set_markup(self.sec_label_text)
            self.tlsbool = True
        else:
            web_context.set_tls_errors_policy(WebKit2.TLSErrorsPolicy.IGNORE)
            self.sec_label.set_markup(self.isec_label_text)
            self.tlsbool = False

    def on_js_switch(self, button, active):

        if not set_enable_javascript: return True

        page = self.tabs[self.current_page][0]
        settings = page.webview.get_settings()

        if button.get_active():
            settings.set_property("enable-javascript", True)
            self.js_label.set_markup(self.jse_label_text)
        else:
            settings.set_property("enable-javascript", False)
            self.js_label.set_markup(self.jsd_label_text)

        page.webview.set_settings(settings)
        url = page.webview.get_uri()
        if url and validators.url(url): page.webview.reload()

    def on_pg_switch(self, button, active):

        if not set_enable_plugins: return True

        page = self.tabs[self.current_page][0]
        settings = page.webview.get_settings()

        if button.get_active():
            settings.set_property("enable-plugins", True)
            self.pg_label.set_markup(self.pge_label_text)
        else:
            settings.set_property("enable-plugins", False)
            self.pg_label.set_markup(self.pgd_label_text)

        page.webview.set_settings(settings)
        url = page.webview.get_uri()
        if url and validators.url(url): page.webview.reload()

    def on_tools_menu(self):

        page = self.tabs[self.current_page][0]
        self.tools_menu.set_relative_to(page.tools)
        
        if page.webview.get_property("visible"):
            self.finder_button.set_sensitive(True)
            self.print_button.set_sensitive(True)
            self.zoom_in_button.set_sensitive(True)
            self.zoom_out_button.set_sensitive(True)
            self.vte_button.set_sensitive(True)
        else:
            self.finder_button.set_sensitive(False)
            self.print_button.set_sensitive(False)
            self.zoom_in_button.set_sensitive(False)
            self.zoom_out_button.set_sensitive(False)
            self.vte_button.set_sensitive(False)

        if not self.is_defcon:
            self.delete_cache_label.set_markup("<span size='x-small'>{}: {}</span>".\
            format(_("In use"), get_cache_size(self.cache_path)))

        self.tools_menu.show_all()
        self.update_status()

    def on_download_started(self, context, download):

        download.connect("decide-destination", self.on_decide_destination)
        download.connect("created-destination", self.on_created_destination)
        download.connect("received-data", self.on_received_data)
        download.connect("finished", self.on_finished)
        download.connect("failed", self.on_failed)

    def on_failed(self, download, error):

        if type(error) == GLib.GError:
            
            if error.code == 400: return True

            msg = error.message.encode("ascii", "replace").\
            decode("utf8", "replace").replace("?", "")
            if msg:
                dialog().error(_("GLib Notification"),\
                "<span size='small'>{}.</span>".format(msg))
                return True
            else: return True
        else: return True

    def on_decide_destination(self, download, name):

        url = download.get_request().get_uri()

        if not name: name = get_domain(url).replace(".", "_")
        if not "." in name:

            mime = download.get_response().get_mime_type()
            suf = mime.split("/")
            name = "{}.{}".format(name, suf[1])

        for i in self.dlview:
            for a in i:
                if type(a) == Gtk.ModelButton:
                    if a.get_name().split("/")[-1] == name:
                        self.downloads_menu.show()
                        return True

        if url: pathchooser().save(name, download, url)

    def on_cancel_download(self):

        if len(self.dlview) == 0: self.downloads_menu.hide()

    def on_restart_download(self, download):

        url = download.get_request().get_uri()
        if url: download.get_web_view().download_uri(url)

    def on_created_destination(self, download, destination):

        name = get_filename(destination)
        unname = unparse(destination)

        item = Gtk.ModelButton(name=unname)
        item.set_alignment(0.0, 0.5)

        item.set_label("<span size='small'>{}: {}</span>\r<span size='x-small'>{}: {}</span>"\
        .format(_("Downloading"), minify(html.escape(name), 50),\
        _("In"), minify(html.escape(destination.replace("file://", "")), 50)))

        item.get_child().set_use_markup(True)
        item.get_child().set_padding(5, 5)

        item.connect("clicked", lambda x: subprocess.Popen\
        ([app_launcher, os.path.dirname(destination)]))

        canc = make_button(make_icon("edit-delete.svg"), None, False)
        canc.connect("clicked", lambda x: [download.cancel(),\
        self.dlview.remove(grid), self.on_cancel_download()])

        rest = make_button(make_icon("refresh.svg"), None, False)
        rest.connect("clicked", lambda x: [download.cancel(),\
        self.dlview.remove(grid), self.on_cancel_download(),\
        self.on_restart_download(download)])

        pbar = Gtk.ProgressBar(name=unname)

        grid = Gtk.Grid()
        grid.set_column_spacing(0)
        grid.attach(canc, 0, 0, 1, 1)
        grid.attach(rest, 1, 0, 1, 1)
        grid.attach(item, 2, 0, 1, 1)
        grid.attach(pbar, 2, 1, 1, 1)
        grid.set_column_homogeneous(False)

        self.dlview.add(grid)
        self.dlview.reorder_child(grid, 0)
        self.on_download_menu()

    def on_received_data(self, download, data_length):

        bar = self.get_progress_bar(download)

        if bar:
            if download.props.estimated_progress <= 0: bar.pulse()
            else: bar.set_fraction(download.props.estimated_progress)

    def on_finished(self, download):

        for i in self.dlview:
            for a in i:
                if a.get_name() == download.get_destination():

                    if type(a) == Gtk.ModelButton:

                        name = get_filename(download.get_destination())
                        a.get_child().set_markup("<span size='small'>{}: {}</span>".\
                        format(_("Download complete for"), minify(html.escape(name), 25)))

                        if not self.downloads_menu.get_visible():

                            for i, item in enumerate(self.tabs):
                                self.tabs[i][0].download_button.\
                                set_image(make_icon("notification.svg"))

                    if type(a) == Gtk.ProgressBar: a.set_fraction(1.0)

                    a.set_name("")

    def on_context_menu(self, view, menu, event, htr): on_context_menu(self, view, menu, event, htr)

    def on_context_menu_dismissed(self, view): self.is_human_choice = True

    def on_title_changed(self, view, event):

        if event.name == "title":
            title = view.get_title()
            self.dynamic_title(view, title)

        self.update_status()

    def on_decide_policy(self, view, decision, decision_type):

        url = decision.get_request().get_uri()

        if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION:

            for i in uri_schemes:
                if i in url:
                    decision.ignore()
                    subprocess.Popen([app_launcher, url])
                    return True

        if decision_type == WebKit2.PolicyDecisionType.NEW_WINDOW_ACTION:

            self.is_human_choice = False
            self.open_blank(url)
            return True

        if decision_type == WebKit2.PolicyDecisionType.RESPONSE:

            mime_request = decision.get_response().props.mime_type

            if mime_request in evince_mime:

                try: gi.require_version("EvinceView", "3.0")
                except: pass
                else: return True

            if mime_request in mime_view: return True
            if "application/" in mime_request: decision.download()

    def on_create(self, view, action):

        t = action.get_navigation_type()
        g = action.is_user_gesture()
        m = action.get_mouse_button()

        if self.adk_switch.get_active() and adk_popups == 1:
            if not self.is_human_choice:
                if t == WebKit2.NavigationType.OTHER and not g: return

        if self.adk_switch.get_active() and adk_popups == 2:
            if not self.is_human_choice: return

        self.is_human_choice = False
        if t == WebKit2.NavigationType.LINK_CLICKED and g and m: return
        self.open_blank(action.get_request().get_uri())

    def on_tab_changed(self, notebook, page, index):

        self.current_page = index
        self.remtab.set_sensitive(True)
        if tab_cb: self.sensitive_tab(True)
        self.update_status()

    def on_maximize(self):

        if self.is_maximized(): self.unmaximize()
        else: self.maximize()

        return True

    def on_icon_pressed(self, entry, pos, event):

        page = self.tabs[self.current_page][0]

        if pos == pos.SECONDARY:
            if page.security == 0: self.cert()
            else: secure(page.security, page.webview.get_uri(),\
                  page.cert_message, page.cert_revealer, page.allow_cert_button)

        return True

    '''
    ###################
    # Browser Methods #
    ###################
    '''

    def update_status(self):

        page = self.tabs[self.current_page][0]
        view = page.webview
        url = view.get_uri()
        scrolled_window = page.scrolled_window
        name = scrolled_window.get_name()

        if os.path.exists(theme_file): self.del_theme_button.set_sensitive(True)
        else: self.del_theme_button.set_sensitive(False)

        if url:
            page.refresh.set_sensitive(True)
            self.save_button.set_sensitive(True)
        else:
            page.refresh.set_sensitive(False)
            self.save_button.set_sensitive(False)

        if name == "source" or name == "bookmarks": self.save_button.set_sensitive(True)

        if name == "webview" or name == "bookmarks": self.open_button.set_sensitive(True)
        else: self.open_button.set_sensitive(False)

        if url and validators.url(url): self.source_button.set_sensitive(True)
        else:
            page.main_url_entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.SECONDARY, None)
            self.source_button.set_sensitive(False)

        if view.get_zoom_level() != 1.0: self.zoom_restore_button.set_sensitive(True)
        else: self.zoom_restore_button.set_sensitive(False)

        if view.can_go_forward(): page.go_forward.set_sensitive(True)
        else: page.go_forward.set_sensitive(False)

        if view.can_go_back(): page.go_back.set_sensitive(True)
        else: page.go_back.set_sensitive(False)

    def refresh_liststore(self, tp):

        for i in self.tabs[self.current_page][0]:
            if type(i) == Gtk.ScrolledWindow:
                for t in i:
                    if type(t) == Gtk.TreeView:

                        ls = t.get_model()
                        ls.clear()

                        if tp == 1: l = bookmarksview()
                        if tp == 2: l = cookiesview()
                        if tp == 3: l = historyview()

                        for a in l: ls.append(list(a))
                        t.set_model(ls)

    def get_progress_bar(self, download):

        for i in self.dlview:
            for a in i:
                if a.get_name() == download.get_destination():
                    if type(a) == Gtk.ProgressBar: return a

    def close_current_tab(self):

        if self.notebook.get_n_pages() != 1:
            page = self.current_page
            self.tabs[page][0].webview.destroy()
            self.tabs[page][0].destroy()
            current_tab = self.tabs.pop(page)
            self.notebook.remove(current_tab[0])

            if self.notebook.get_n_pages() == 1:
                self.remtab.set_sensitive(False)
                if tab_cb: self.sensitive_tab(False)

    def close_clicked_tab(self, sender, widget):

        self.notebook.set_current_page(self.notebook.page_num(widget))
        self.close_current_tab()
        self.update_status()

    def sensitive_tab(self, boolean):

        for tab, widget in self.tabs:
            if type(widget) == gi.repository.Gtk.HBox:
                for i in widget:
                    if type(i) == gi.overrides.Gtk.Button: i.set_sensitive(boolean)

    def tab_data(self):

        page = self.current_page

        if not tab_cb: page_tuple = (self.create_tab(), Gtk.Label(tab_name))

        if tab_cb:
            tab_box = make_tab_box(tab_name)
            page_tuple = (self.create_tab(), tab_box)

        self.tabs.insert(page + 1, page_tuple)
        self.notebook.insert_page(page_tuple[0], page_tuple[1], page + 1)
        self.notebook.set_current_page(page + 1)

        if tab_cb:
            for i in tab_box:
                if type(i) == gi.overrides.Gtk.Button:
                    i.connect("clicked", self.close_clicked_tab, page_tuple[0])

    def open_new_tab(self):

        self.tab_data()
        self.focus_tab()

    def open_blank(self, url):

        if url:
            self.open_new_tab()
            self.tabs[self.current_page][0].webview.load_uri(url)

    '''
    ###########
    # Methods #
    ###########
    '''

    def check_tab(self, widget, img):

        if type(widget) == gi.repository.Gtk.HBox:
            for i in widget:
                if type(i) == gi.overrides.Gtk.Label and not img: return i
                if type(i) == gi.repository.Gtk.Image and img: return i
        else: return widget

    def try_search(self, query):

        if not search_engine: return True

        query = "{}{}".format(search_engine, query)
        self.tabs[self.current_page][0].webview.load_uri(query)

        return True

    def apply_theme(self, url):

        d = dialog().info(_("Setting a new theme"),\
        "<span size='small'>{}...\n\n{}.</span>".format(_("This operation may take a while"),\
       _("It all depends on your internet speed and requested image size")))

        data = request(url, self.tlsbool, self.p_req())
        content = data[0][0]

        if content:
            with open(theme_file, "wb") as f:
                f.write(content)
                f.close()
                apply_css()
                d.destroy()

        return True

    def p_req(self):

        if webkit_ver > wk16:

            db = self.get_proxy()

            if db:
                if db[0] == str(2): return db
            else: return None

        else: return None

    def get_proxy(self):

        with proxy_con:
            cur = proxy_con.cursor()
            cur.execute("SELECT * FROM proxy;")
            opts = cur.fetchall()

        if opts: return opts[0]

    def set_proxy(self, mode, url, port, type):

        mode = int(mode)

        if mode == 1: web_context.set_network_proxy_settings(\
                      WebKit2.NetworkProxyMode.DEFAULT)

        if mode == 2:

            if type == 0: type = "socks"
            else: type = "http"
            if not url: url = local_ip
            if not port: port = 0

            proxy = "{}://{}:{}".format(type, url, port)

            web_context.set_network_proxy_settings(\
            WebKit2.NetworkProxyMode.CUSTOM, WebKit2.NetworkProxySettings.new(proxy))

        if mode == 3: web_context.set_network_proxy_settings(\
                      WebKit2.NetworkProxyMode.NO_PROXY)

        with proxy_con:
            cur = proxy_con.cursor()
            cur.execute("DELETE FROM proxy;")
            cur.execute("INSERT INTO proxy VALUES(?, ?, ?, ?);", (mode, type, url, port))

        self.tabs[self.current_page][0].webview.reload()

        return True

    def new_user_agent(self, view, iter, column):

        page = self.tabs[self.current_page][0]
        settings = page.webview.get_settings()
        settings.set_property("user-agent", view.get_model()[iter][1])
        page.webview.set_settings(settings)
        page.webview.reload()

        return True

    def video_popout(self, url):

        win = Gtk.Window()
        view = WebKit2.WebView()
        win.set_keep_above(True)
        win.add(view)
        view.load_uri(url)
        win.set_default_size(500, 250)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.set_title(url)
        win.show_all()

        return True

    def delete_theme(self):

        if os.path.exists(theme_file):

            decision = dialog().decision(_("Delete Theme"), "<span size='small'>{}?</span>"\
            .format(_("Do you really want to delete this theme")))

            if decision:
                os.remove(theme_file)
                apply_css()
                self.present()

        return True

    def dynamic_title(self, view, title):

        url = view.get_uri()

        if not url and not title: title = tab_name
        if not title: title = url

        counter = 0

        for tab, widget in self.tabs:

            widget = self.check_tab(widget, 0)

            if tab.webview is view:
                if widget:
                    widget.set_text(minify(title, 50))
                    widget.set_tooltip_text("")
                    if len(title) > 50: widget.set_tooltip_text(title)

            counter += 1

    def get_clean_page(self, page, name, status):

        page = self.tabs[page][0]

        for child in page.url_box.get_children(): child.destroy()

        list = ["frame_main"]

        if not status:
            list.append("frame_status")
            page.iconified_vte.destroy()

        for i in page:
            if not i.get_name() in list and\
            not type(i) == gi.overrides.Gtk.ScrolledWindow:
                page.remove(i)

        scrolled_window = page.scrolled_window
        for i in scrolled_window: scrolled_window.remove(i)
        scrolled_window.set_name(name)
        return scrolled_window

    def view_settings(self):

        self.open_new_tab()
        page = self.current_page
        scrolled_window = self.get_clean_page(page, "settings", False)
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        scrolled_window.set_shadow_type(Gtk.ShadowType.NONE)

        save_settings_button = make_button(make_icon("object-select.svg"), _("Save Settings"), False)
        restore_settings_button = make_button(make_icon("edit-clear-all.svg"), _("Restore Settings"), False)
        plugins_button = make_button(make_icon("plugin.svg"), _("View Plugins"), False)
        bookmarks_button = make_button(make_icon("bookmarks.svg"), _("View Bookmarks"), False)
        history_button = make_button(make_icon("history.svg"), _("View History"), False)
        cookies_button = make_button(make_icon("cookies.svg"), _("Cookies Manager"), False)

        with settings_con:
            cur = settings_con.cursor()
            cur.execute("SELECT * FROM settings;")
            opts = cur.fetchall()

            general_grid = Gtk.Grid()
            general_sw = Gtk.ScrolledWindow()
            advanced_grid = Gtk.Grid()
            advanced_sw = Gtk.ScrolledWindow()
            obrien_grid = Gtk.Grid()
            obrien_sw = Gtk.ScrolledWindow()

            for c, i in enumerate(opts):

                if i[4] == "1": grid = general_grid
                if i[4] == "2": grid = advanced_grid
                if i[4] == "3": grid = obrien_grid
                if i[2] == "1": grid.attach(setting_element(i[6], i[0], i[1], i[2], i[3], None), 0, c, 1, 1)
                if i[2] == "2": grid.attach(setting_element(i[6], i[0], i[1], i[2], i[3], globals()[i[5]]), 0, c, 1, 1)

        opts = []
        grids = [general_grid, advanced_grid, obrien_grid]

        for i in grids:
            for a in i:
                for e in a:
                    if type(e) != Gtk.Label: opts.append(e)

        self.tabs[page][0].url_box.pack_start(save_settings_button, False, False, 5)
        self.tabs[page][0].url_box.pack_start(restore_settings_button, False, False, 5)
        self.tabs[page][0].url_box.pack_start(plugins_button, False, False, 5)
        self.tabs[page][0].url_box.pack_start(bookmarks_button, False, False, 5)
        self.tabs[page][0].url_box.pack_start(history_button, False, False, 5)
        self.tabs[page][0].url_box.pack_start(cookies_button, False, False, 5)
        self.tabs[page][0].url_box.show_all()

        save_settings_button.connect("clicked", lambda x: self.on_save_settings(opts))
        restore_settings_button.connect("clicked", lambda x: self.on_restore_settings())
        plugins_button.connect("clicked", lambda x: self.view_plugins())
        bookmarks_button.connect("clicked", lambda x: self.view_bookmarks(None, None))
        history_button.connect("clicked", lambda x: self.view_history())
        cookies_button.connect("clicked", lambda x: self.cookies_manager())

        tab = self.check_tab(self.tabs[page][1], 0)
        tab.set_text(_("Settings"))

        general_sw.add(general_grid)
        advanced_sw.add(advanced_grid)
        obrien_sw.add(obrien_grid)

        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.LEFT)
        notebook.append_page(general_sw, make_label_text(_("General")))
        notebook.append_page(advanced_sw, make_label_text(_("Advanced")))
        notebook.append_page(obrien_sw, make_label_text("Miles O'Brien"))

        scrolled_window.add(notebook)
        scrolled_window.show_all()

        self.update_status()

        return True

    def find_source(self, entry, view):

        buf = view.get_buffer()
        i = buf.get_iter_at_mark(buf.get_insert())

        settings = SearchSettings()
        settings.set_case_sensitive(False)
        settings.set_at_word_boundaries(False)
        settings.set_regex_enabled(True)
        settings.set_property('search-text', entry.get_text())
        settings.set_wrap_around(True)

        context = SearchContext.new(buf, settings)
        context.set_highlight(True)

        i.forward_chars(1)
        match, start_iter, end_iter = context.forward(i)

        if match:
            buf.place_cursor(start_iter)
            buf.move_mark(buf.get_selection_bound(), end_iter)
            view.scroll_to_mark(buf.get_insert(), 0.25, True, 0.5, 0.5)
            return True

    def view_source(self):

        if not self.tabs[self.current_page][0]\
        .webview.get_property("visible"): return True

        url = self.tabs[self.current_page][0].webview.get_uri()

        if url and validators.url(url):
            
            data = request(url, self.tlsbool, self.p_req())
            source = data[0][0]
            content_type = data[0][1].split(";")[0]

            self.open_new_tab()
            page = self.current_page

            source = ''.join([s.decode("utf8", "replace") + "\n" for s in source.splitlines()])            
            scrolled_window = self.get_clean_page(page, "source", False)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file("{}system-search.svg".format(icns))
            entry = Gtk.Entry()
            entry.set_width_chars(30)
            entry.set_icon_from_pixbuf(Gtk.EntryIconPosition.PRIMARY, pixbuf)

            button = make_button(make_icon("go-down.svg"), None, False)

            self.tabs[page][0].url_box.pack_end(button, False, False, 0)
            self.tabs[page][0].url_box.pack_end(entry, False, False, 5)
            self.tabs[page][0].show_all()

            view = View(name=get_domain(url))
            view.set_auto_indent(True)
            view.set_show_line_numbers(True)
            view.set_wrap_mode(Gtk.WrapMode.WORD)
            view.set_monospace(True)
            view.get_buffer().set_text(source)
            scrolled_window.add(view)
            lang = LanguageManager.get_default().guess_language(None, content_type)
            view.get_buffer().set_language(lang)
            view.get_buffer().set_highlight_syntax(True)
            scrolled_window.show_all()

            button.connect("clicked", lambda x: self.find_source(entry, view))
            entry.connect("activate", lambda x: self.find_source(entry, view))
            entry.connect("changed", lambda x: self.find_source(entry, view))
            entry.grab_focus()

            tab = self.check_tab(self.tabs[page][1], 0)
            tab.set_text("{}: {}".format(_("Source"), minify(url, 50)))

            self.update_status()

            return True

    def cookies_manager(self):

        self.open_new_tab()
        page = self.current_page
        scrolled_window = self.get_clean_page(page, "cookies", True)
        
        clear_cookies_button = make_button(make_icon("edit-clear-all.svg"), _("Clear cookies"), False)
        clear_cookies_button.connect("clicked", lambda x: self.on_clear_cookies())
        rem_cookies_button = make_button(make_icon("edit-delete.svg"), _("Remove the selected cookie"), False)

        name_obj = make_box(_("Name"), None, None)
        value_obj = make_box(_("Value"), None, None)
        host_obj = make_box(_("Host"), None, None)
        path_obj = make_box(_("Path"), None, None)
        expiry_obj = make_box(_("Expiry"), 10, 1)
        lastacc_obj = make_box(_("LastAccessed"), 1, 2)
        issec_obj = make_box(_("IsSecure"), 1, 2)
        ishttp_obj = make_box(_("IsHttpOnly"), 1, 2)

        edit_cookies_grid = Gtk.Grid()
        edit_cookies_grid.set_column_spacing(10)
        edit_cookies_button = make_button(make_icon("document-edit.svg"), _("Edit the selected cookie"), False)
        add_cookies_button = make_button(make_icon("list-add.svg"), _("Add a new cookie with set data"), False)

        edit_cookies_grid.attach(Gtk.Label(), 0, 0, 1, 1)
        edit_cookies_grid.attach(Gtk.Label(), 0, 1, 1, 1)
        edit_cookies_grid.attach(edit_cookies_button, 0, 2, 1, 1)
        edit_cookies_grid.attach(add_cookies_button, 1, 2, 1, 1)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)

        grid.attach(name_obj, 0, 0, 1, 1)
        grid.attach(value_obj, 1, 0, 1, 1)
        grid.attach(host_obj, 2, 0, 1, 1)
        grid.attach(path_obj, 3, 0, 1, 1)
        grid.attach(expiry_obj, 0, 1, 1, 1)
        grid.attach(lastacc_obj, 1, 1, 1, 1)
        grid.attach(issec_obj, 2, 1, 1, 1)
        grid.attach(ishttp_obj, 3, 1, 1, 1)
        grid.attach(edit_cookies_grid, 4, 1, 1, 1)

        frame = Gtk.Frame(name="frame_cookies")
        frame.add(grid)

        self.tabs[page][0].url_box.pack_start(clear_cookies_button, False, False, 5)
        self.tabs[page][0].url_box.pack_start(rem_cookies_button, False, False, 5)
        self.tabs[page][0].pack_start(frame, False, False, 0)
        self.tabs[page][0].show_all()

        rem_cookies_button.set_sensitive(False)
        edit_cookies_button.set_sensitive(False)
        add_cookies_button.set_sensitive(False)

        cookies = cookiesview()

        liststore = Gtk.ListStore(int, str, str, str, str, int, int, int, int, str)

        for i in cookies: liststore.append(list(i))

        view = Gtk.TreeView(model=liststore)

        for i, column_title in enumerate(\
        [_("Id"), _("Name"), _("Value"), _("Host"), _("Path"),\
        _("Expiry"), _("LastAccessed"), _("IsSecure"), _("IsHttpOnly")]):

            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            view.append_column(column)

        selection = view.get_selection()
        selection.connect("changed", self.on_cookies_selected)

        rem_cookies_button.connect("clicked", lambda x:\
        self.on_rem_cookies(selection))
        edit_cookies_button.connect("clicked", lambda x:\
        self.on_edit_cookies(selection, None))
        add_cookies_button.connect("clicked", lambda x:\
        self.on_edit_cookies(selection, 1))

        scrolled_window.add(view)
        scrolled_window.show_all()

        tab = self.check_tab(self.tabs[page][1], 0)
        tab.set_text(_("Cookies"))

        grid.set_property("margin-left", 10)
        grid.set_property("margin-bottom", 10)

        self.name_obj = name_obj
        self.value_obj = value_obj
        self.host_obj = host_obj
        self.path_obj = path_obj
        self.expiry_obj = expiry_obj
        self.lastacc_obj = lastacc_obj
        self.issec_obj = issec_obj
        self.ishttp_obj = ishttp_obj
        self.rem_cookies_button = rem_cookies_button
        self.edit_cookies_button = edit_cookies_button
        self.add_cookies_button = add_cookies_button

        self.update_status()

        return True

    def view_history(self):

        self.open_new_tab()
        page = self.current_page
        scrolled_window = self.get_clean_page(page, "history", False)

        clear_history_button = make_button(make_icon("edit-clear-all.svg"), _("Clear history"), False)
        clear_history_button.connect("clicked", lambda x: self.on_clear_history())
        bookmarks_history_button = make_button(make_icon("bookmarks.svg"), _("Add to bookmarks"), False)

        self.tabs[page][0].url_box.pack_start(clear_history_button, False, False, 5)
        self.tabs[page][0].url_box.pack_start(bookmarks_history_button, False, False, 5)
        self.tabs[page][0].url_box.show_all()

        bookmarks_history_button.set_sensitive(False)

        history = historyview()

        treestore = Gtk.TreeStore(str, str, str, str)

        today = datetime.date.today()
        minusone = datetime.date.fromordinal(datetime.date.today().toordinal()-1)
        minustwo = datetime.date.fromordinal(datetime.date.today().toordinal()-2)

        iter_today = treestore.append(None, [_("Today"), None, None, None])
        iter_one = treestore.append(None, [_("Yesterday"), None, None, None])
        iter_two = treestore.append(None, [_("Two days ago"), None, None, None])
        iter_old = treestore.append(None, [_("This week"), None, None, None])

        for i in history:

            if str(today) in i[0]: treestore.append(iter_today, [i[0], i[1], i[2], i[3]])
            if str(minusone) in i[0]: treestore.append(iter_one, [i[0], i[1], i[2], i[3]])
            if str(minustwo) in i[0]: treestore.append(iter_two, [i[0], i[1], i[2], i[3]])
            if not str(today) in i[0] and not str(minusone) in i[0] and not str(minustwo)\
            in i[0]: treestore.append(iter_old, [i[0], i[1], i[2], i[3]])

        view = Gtk.TreeView(model=treestore)

        for i, column_title in enumerate([_("Date"), _("Title"), _("URL")]):

            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            view.append_column(column)

        view.connect('row-activated', self.on_iter_clicked)

        selection = view.get_selection()
        selection.connect("changed", self.on_history_selected)

        bookmarks_history_button.connect("clicked", lambda x:\
        self.on_bookmarks_history(selection))

        scrolled_window.add(view)
        scrolled_window.show_all()

        tab = self.check_tab(self.tabs[page][1], 0)
        tab.set_text(_("History"))

        self.bookmarks_history_button = bookmarks_history_button

        self.update_status()

        return True

    def view_bookmarks(self, title, url):

        page = self.tabs[self.current_page][0]

        if not url:
            url = page.webview.get_uri()
            title = page.webview.get_title()

        self.open_new_tab()
        page = self.current_page
        scrolled_window = self.get_clean_page(page, "bookmarks", False)

        clear_bookmarks_button = make_button(make_icon("edit-clear-all.svg"), _("Erase all bookmarks"), False)
        clear_bookmarks_button.connect("clicked", lambda x: self.on_clear_bookmarks())
        rem_bookmarks_button = make_button(make_icon("edit-delete.svg"), _("Remove the selected bookmark"), False)
        add_bookmarks_button = make_button(make_icon("bookmark-new.svg"), _("Add to bookmarks"), False)

        entry_title_bookmarks = Gtk.Entry()
        entry_title_bookmarks.set_width_chars(30)
        entry_url_bookmarks = Gtk.Entry()
        entry_url_bookmarks.set_width_chars(50)

        self.tabs[page][0].url_box.pack_start(clear_bookmarks_button, False, False, 5)
        self.tabs[page][0].url_box.pack_start(rem_bookmarks_button, False, False, 5)
        self.tabs[page][0].url_box.pack_end(add_bookmarks_button, False, False, 5)
        self.tabs[page][0].url_box.pack_end(entry_url_bookmarks, False, False, 5)
        self.tabs[page][0].url_box.pack_end(entry_title_bookmarks, False, False, 0)
        self.tabs[page][0].url_box.show_all()

        entry_title_bookmarks.set_tooltip_text(_("Type here your description"))
        entry_url_bookmarks.set_tooltip_text(_("Type here your URL address"))

        if title: entry_title_bookmarks.set_text(title)
        if url and validators.url(url): entry_url_bookmarks.set_text(url)

        rem_bookmarks_button.set_sensitive(False)

        bookmarks = bookmarksview()

        liststore = Gtk.ListStore(str, str, str, str)

        for i in bookmarks: liststore.append(list(i))

        view = Gtk.TreeView(model=liststore, name="bookmarks")

        for i, column_title in enumerate([_("Date"), _("Title"), _("URL")]):

            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            view.append_column(column)

        view.connect('row-activated', self.on_iter_clicked)

        selection = view.get_selection()
        selection.connect("changed", self.on_bookmarks_selected)

        rem_bookmarks_button.connect("clicked", lambda x: self.on_rem_bookmarks(selection))

        scrolled_window.add(view)
        scrolled_window.show_all()

        tab = self.check_tab(self.tabs[page][1], 0)
        tab.set_text(_("Bookmarks"))

        add_bookmarks_button.connect("clicked", lambda x:\
        self.on_add_bookmarks(entry_title_bookmarks, entry_url_bookmarks))
        entry_url_bookmarks.connect("activate", lambda x:\
        self.on_add_bookmarks(entry_title_bookmarks, entry_url_bookmarks))
        entry_title_bookmarks.connect("activate", lambda x:\
        self.on_add_bookmarks(entry_title_bookmarks, entry_url_bookmarks))

        self.rem_bookmarks_button = rem_bookmarks_button
        self.entry_title_bookmarks = entry_title_bookmarks
        self.entry_url_bookmarks = entry_url_bookmarks

        self.update_status()

        return True

    def get_plugins(self, src, res, data):

        page = self.tabs[self.current_page][0]
        plugins = WebKit2.WebContext.get_plugins_finish(src, res)
        scrolled_window = page.scrolled_window

        if scrolled_window:

            l = ["flash", "evince", "icedtea", "java", "openjdk", "vlc", "windows", "quicktime"]
            plgs = []

            for i in plugins:

                mime_desc_list = []
                mime_exts_list = []
                mime_type_list = []

                label = make_label_selectable(0.0, 0.5)
                label.set_markup("<b>{}</b>\n<span size='small'>{}</span>\n<span size='small'>{}</span>\n"\
                .format(clean_html(i.get_name()), clean_html(i.get_description()), clean_html(i.get_path())))

                for m in i.get_mime_info_list():
                    mime_desc_list.append(m.get_description())
                    mime_exts_list.append(m.get_extensions())
                    mime_type_list.append(m.get_mime_type())

                p = ["plugin", "{}{}.svg"]
                name = p[0]

                for o in l:
                    if o in i.get_name().lower(): name = o

                icon_path = p[1].format(icns, name)
                if not os.path.exists(icon_path): icon_path = p[1].format(icns, p[0]) 

                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icon_path, 32, 32)
                icon = Gtk.Image().new_from_pixbuf(pixbuf)
                icon.set_alignment(0, 0.2)

                plgs.append(make_plugin_grid(icon, label, mime_desc_list, mime_exts_list, mime_type_list))

            grid = Gtk.Grid()
            grid.set_column_homogeneous(False)
            for c, i in enumerate(plgs): grid.attach(i, 0, c, 1, 1)

            scrolled_window.add(grid)
            scrolled_window.show_all()

    def view_plugins(self):

        web_context.get_plugins(None, self.get_plugins, None)

        self.open_new_tab()
        page = self.current_page
        scrolled_window = self.get_clean_page(page, "plugins", False)

        self.tabs[page][0].url_box.pack_start(Gtk.Label(), False, False, 0)
        self.tabs[page][0].show_all()

        tab = self.check_tab(self.tabs[page][1], 0)
        tab.set_text(_("Plugins"))

        self.update_status()

        return True

    def cert(self):

        page = self.tabs[self.current_page][0]
        reveal(page.cert_revealer, False)
        data = page.webview.get_tls_info()

        popover = build_scrollable_popover(Gtk.PositionType.BOTTOM, -1, 500)

        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)

        for x in range(0, 14): grid.attach(cert_declarations(data, x+1), 0, x, 1, 1)

        for i in popover:
            if type(i) == Gtk.ScrolledWindow: i.add(grid)

        entry = page.main_url_entry

        popover.set_relative_to(entry)
        popover.set_pointing_to(entry.get_icon_area(Gtk.EntryIconPosition.SECONDARY))
        popover.show_all()

        self.update_status()

        return True

    def zoom_in(self):

        page = self.tabs[self.current_page][0]
        if not page.webview.get_property("visible"): return True
        level = page.webview.props.zoom_level
        level += 0.05
        page.webview.set_zoom_level(level)
        self.update_status()

        return True

    def zoom_out(self):

        page = self.tabs[self.current_page][0]
        if not page.webview.get_property("visible"): return True
        level = page.webview.props.zoom_level
        level -= 0.05
        page.webview.set_zoom_level(level)
        self.update_status()

        return True

    def zoom_restore(self):

        page = self.tabs[self.current_page][0]
        if not page.webview.get_property("visible"): return True
        page.webview.set_zoom_level(1.0)
        self.update_status()

        return True

    def page_print(self):

        page = self.tabs[self.current_page][0]
        if not page.webview.get_property("visible"): return True

        p = WebKit2.PrintOperation.new(page.webview)
        p.run_dialog()

        return True

    def finder(self):

        page = self.tabs[self.current_page][0]
        if not page.webview.get_property("visible"): return True
        page.find_revealer.show_all()
        reveal(page.find_revealer, True)
        page.find_entry.grab_focus()
        page.on_finder()

        return True

    def vte(self):

        page = self.tabs[self.current_page][0]
        if not page.webview.get_property("visible"): return True

        try: gi.require_version('Vte', '2.91')
        except:
            dialog().error(_("VTE missing"), "<span size='small'>{} {}.</span>"\
            .format(browser_name, _("requires at least Vte 2.91 or higher")))
            return True
        else: from gi.repository import Vte

        terminal = Vte.Terminal()
        terminal.spawn_sync(Vte.PtyFlags.DEFAULT,\
        os.environ['HOME'], [shell_list[shell]], [], GLib.SpawnFlags\
        .DO_NOT_REAP_CHILD, None, None,)

        terminal.connect("button-press-event", self.on_vte_button_press)

        page.iconified_vte.hide()

        if not page.vte_sw.get_children(): page.vte_sw.add(terminal)
        page.vte_revealer.show_all()
        reveal(page.vte_revealer, True)
        if page.vte_sw.get_children(): page.vte_sw.get_children()[0].grab_focus()

        return True

    def go_fullscreen(self):

        if not self.is_fullscreen:
            self.is_fullscreen = True
            self.fullscreen()
        else:
            self.is_fullscreen = False
            self.unfullscreen()

        return True

    def reload_tab(self):

        page = self.tabs[self.current_page][0]
        if page.refresh.get_sensitive(): page.webview.reload()

        return True

    def focus_tab(self):

        self.tabs[self.current_page][0].main_url_entry.grab_focus()

        return True

    def save(self):

        page = self.tabs[self.current_page][0]
        scrolled_window = page.scrolled_window
        url = page.webview.get_uri()
        name = scrolled_window.get_name()
        child = scrolled_window.get_children()[0]

        if url and name == "webview": page.webview.download_uri(url)

        if name == "source":

            buf = child.get_buffer()
            content = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
            if content: pathchooser().force_save(content,\
            "{}.src.txt".format(child.get_name().replace(".","_")))

        if name == "bookmarks":

            bookmarks_list = []

            for i in child.get_model(): bookmarks_list.append([i[0]] + [i[1]] + [i[3]])

            if bookmarks_list:
                content = do_export_bookmarks(bookmarks_list)
                if content: pathchooser().force_save(content, "{}.html".format(_("Bookmarks").lower()))

        return True

    def open(self):

        page = self.tabs[self.current_page][0]
        scrolled_window = page.scrolled_window
        name = scrolled_window.get_name()

        if name == "bookmarks":

            s = _("new bookmark will be imported")
            p = _("new bookmarks will be imported")

            filename = pathchooser().import_bookmarks()
            if filename: content = do_import_bookmarks(filename)
            if filename and content:

                if len(content) == 1: m = s
                else: m = p

                decision = dialog().decision(_("Are you sure?"),\
                "<span size='small'>{}, {} {}.\n{}.</span>"\
                .format(_("Clicking on OK"), len(content), m,\
                _("Bookmarks with identical urls will be automatically ignored")))

                if decision:
                    for i in content: self.on_insert_bookmarks(i[0], i[1])

            return True

        pathchooser().open(page.webview)

        return True

    def open_new_window(self):

        subprocess.Popen([browser])

        return True

    def defcon(self):

        subprocess.Popen([browser, "-i"])

        return True

    def restart(self): os.execl(sys.executable, sys.executable, *sys.argv)

    '''
    ############
    # Gdk.KEYS #
    ############
    '''

    def on_key_pressed(self, widget, event):

        modifiers = Gtk.accelerator_get_default_mod_mask()
        vte_revealed = self.tabs[self.current_page][0].vte_revealer.get_child_revealed()

        mapping = {Gdk.KEY_r: self.reload_tab,
                   Gdk.KEY_w: self.close_current_tab,
                   Gdk.KEY_t: self.open_new_tab,
                   Gdk.KEY_f: self.finder,
                   Gdk.KEY_s: self.view_settings,
                   Gdk.KEY_u: self.view_source,
                   Gdk.KEY_h: self.view_history,
                   Gdk.KEY_p: self.page_print,
                   Gdk.KEY_plus: self.zoom_in,
                   Gdk.KEY_minus: self.zoom_out,
                   Gdk.KEY_m: self.zoom_restore,
                   Gdk.KEY_k: self.delete_theme,
                   Gdk.KEY_n: self.open_new_window,
                   Gdk.KEY_i: self.defcon,
                   Gdk.KEY_b: self.view_plugins,
                   Gdk.KEY_o: self.cookies_manager,
                   Gdk.KEY_l: self.focus_tab,
                   Gdk.KEY_j: lambda: pass_generator(self),
                   Gdk.KEY_g: lambda: user_agent(self),
                   Gdk.KEY_d: lambda: self.view_bookmarks(None, None),
                   Gdk.KEY_q: lambda: quit(self)}

        if webkit_ver > wk16:

            mapping.update({Gdk.KEY_x: lambda: proxy(self)})

        if event.state & modifiers == Gdk.ModifierType.CONTROL_MASK\
        and event.keyval in mapping and not vte_revealed:
            mapping[event.keyval]()
            return True

        nomod = {Gdk.KEY_F4: self.vte,
                 Gdk.KEY_F5: self.reload_tab,
                 Gdk.KEY_F11: self.go_fullscreen}

        try:
            if type(event.state) == Gdk.ModifierType\
            and event.keyval in nomod and not vte_revealed:
                nomod[event.keyval]()
                return True
        except: pass

    '''
    ########
    # Init #
    ########
    '''

def init():

    if not webkit_ver:

        dialog().error(_("WebKit Error"), "<span size='small'>{} {}.\n{}.</span>"\
        .format(browser_name, _("requires at least WebKit 2.12.3 or higher"),\
        _("In some distros you probably need to add a third-party repository")))

        return

    try:

        if sys.argv[1]:

            if sys.argv[1] == "-h":
                print("\033[1;91m\n{} {}\n\n-h: {}\n-i: {}\n-v: {}\n\n{}: {} ddg.co (or http://ddg.co)\n\n\033[0m"\
                .format(_("Welcome to"), browser_name, _("shows this menu"), _("opens the browser in defcon mode"),\
                _("shows the version"), _("Usage"), browser))
                return

            if sys.argv[1] == "-v":
                print("\n", version, "\n")
                return

    except: pass

    Browser()
    Gtk.main()

def quit(obj):

    obj.destroy()
    Gtk.main_quit()

if __name__ == "__main__": init()

