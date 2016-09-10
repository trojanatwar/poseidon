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

import os, gettext, pickle, sqlite3 as lite

'''
############
# Language #
############
'''

language = "en_US"                                         # Language (Default: "en_US")
                                                           # Check "po/locale" folder to know how many languages are currently available.

'''
##################
# Languages List #
##########################################################################################
# Set here your languages. eg. ['it_IT', 'jp_JA', 'fr_FR'] etc..                         #
# You can use Poedit to create new translations, it's cool and free: https://poedit.net/ #
##########################################################################################
'''

translations = ['en_US', 'ru_RU', 'de_DE', 'nl_NL', 'fr_FR', 'es_ES', 'it_IT', 'ja_JP',\
                'tr_TR', 'pl_PL', 'zh_CN', 'da_DK', 'zh_TW']

lc_path = "po/locale"
lang = gettext.translation(language, localedir=lc_path, languages=translations)
lang.install()

'''
##################
# About Settings #
##################
'''

version = "0.1.1"
browser_name = "Poseidon"
website = "https://github.com/sidus-dev/poseidon"
authors = "Andrea Pasciuta  <sidus@arbornet.org>"
comments = _("A fast, minimal and lightweight browser")

'''
####################
# Browser Settings #
####################
'''

width = 800                                                # Window width size (Default: 800)
height = 600                                               # Window height size (Default: 600)
tab_name = _("Empty")                                      # Empty tab label name (Default: _("Empty"))
search_engine = "https://duckduckgo.com/?q="               # Default search engine (Default: "https://duckduckgo.com/?q=")
home_page = "https://www.duckduckgo.com/"                  # Home page (Default: "https://www.duckduckgo.com/") set None to disable it

'''
#########
# Paths #
#########
'''

base_path = ".poseidon/"                                   # Base path
icns = "icons/"                                            # Icons path
adk_filters_path = "filters"                               # AdKiller filters path
cache_path = "{}cache".format(base_path)                   # Cache path
cookies_path = "{}cookies".format(base_path)               # Cookies path
history_path = "{}history/".format(base_path)              # History path
bookmarks_path = "{}bookmarks/".format(base_path)          # Bookmarks path
pickle_path = "{}pickle/".format(base_path)                # Pickle path
theme_path = "{}theme/".format(base_path)                  # Theme path
pages_path = "pages"                                       # Pages path
lib_path = "lib"                                           # Library path

'''
#####################
# Autistic Settings #                                      One String to rule them all, One String to find them, One String to bring them all and in the Memory store them.
#####################
'''

                                                           # Floats

zoom_level_float = 0.05                                    # Zoom level speed (Default: 0.05)
xalign = 0.0                                               # Gtk.Popover xalign (Default: 0.0)
yalign = 0.5                                               # Gtk.Popover yalign (Default: 0.5)

                                                           # Integers

autocomplete_policy = 0                                    # Autocomplete policy (Default: 0) (Disabled = None, History = 0, DuckDuckGo = 1)
favicon_size = 16                                          # Favicon size (Default: 16)
bf_timeout = 1000                                          # Back/Forward buttons holding time (Default: 1000) (1000 = 1 second)
                                                           # Visited links will show in a popover when you hold back/forward buttons for these seconds.
load_timeout = 0                                           # Load timeout (Default: 0) (30000 = 30 seconds) (set 0 to disable it)
                                                           # If loading a website takes longer than set seconds browser will return a popup dialog with the issue.
                                                           # Increase the value in case your connection is very slow, 25000 is a good deal.
find = 1                                                   # Finding type (Default: 1) (eg. set 0 for case sensitive) (None = 0, Case Insensitive = 1, Wrap Around = 16
                                                           # At Words Starts = 2, Treat Medial Capial As Word Start = 4, Backwards = 8)
                                                           # Info: https://lazka.github.io/pgi-docs/WebKit2-4.0/flags.html#WebKit2.FindOptions
cache_model = 1                                            # Cache model (Default: 1) (eg. set 0 to disable cache) (Document Viewer = 0, Web Browser = 1, Document Browser = 2)

                                                           # Booleans

verify_req = True                                          # If 'False', 'requests' module will ignore verifying the SSL certificate (Default: True)
                                                           # False = insecure (but faster), True = secure (but slower)

                                                           # Misc

app_launcher = "xdg-open"                                  # Apps Launcher (Default: "xdg-open") alternatives to xdg-utils:
                                                           # https://wiki.archlinux.org/index.php/default_applications#mimeopen
cookies_db = "cookies.sqlite"                              # Cookies database (Default: "cookies.sqlite")
history_db = "history.sqlite"                              # History database (Default: "history.sqlite")
bookmarks_db = "bookmarks.sqlite"                          # Bookmarks database (Default: "bookmarks.sqlite")
theme_file = "{}theme".format(theme_path)                  # Theme file

'''
####################
# WebKit2 Settings #                                       [https://lazka.github.io/pgi-docs/WebKit2-4.0/classes/Settings.html#property-details]
####################
'''

set_allow_file_access_from_file_urls = False               # (Default: False)
set_allow_modal_dialogs = False                            # (Default: False)
set_auto_load_images = True                                # (Default: True)
set_cursive_font_family = "serif"                          # (Default: "serif")
set_default_charset = "iso-8859-1"                         # (Default: "iso-8859-1")
set_default_font_family = "sans-serif"                     # (Default: "sans-serif")
set_default_font_size = 16                                 # (Default: 16)
set_default_monospace_font_size = 13                       # (Default: 13)
set_draw_compositing_indicators = False                    # (Default: False)
set_enable_accelerated_2d_canvas = False                   # (Default: False)
set_enable_caret_browsing = False                          # (Default: False)
set_enable_developer_extras = True                         # (Default: False)
set_enable_dns_prefetching = False                         # (Default: False)
set_enable_frame_flattening = False                        # (Default: False)
set_enable_fullscreen = True                               # (Default: True)
set_enable_html5_database = True                           # (Default: True)
set_enable_html5_local_storage = True                      # (Default: True)
set_enable_hyperlink_auditing = False                      # (Default: False)
set_enable_java = True                                     # (Default: True)
set_enable_javascript = True                               # (Default: True)
set_enable_media_stream = False                            # (Default: False)
set_enable_mediasource = False                             # (Default: False)
set_enable_offline_web_application_cache = True            # (Default: True)
set_enable_page_cache = True                               # (Default: True)
set_enable_plugins = True                                  # (Default: True)
#set_enable_private_browsing                               # Look for "defcon" in "Paranoid Settings"
set_enable_resizable_text_areas = True                     # (Default: True)
set_enable_site_specific_quirks = True                     # (Default: True)
set_enable_smooth_scrolling = False                        # (Default: False)
set_enable_spatial_navigation = False                      # (Default: False)
set_enable_tabs_to_links = True                            # (Default: True)
set_enable_webaudio = True                                 # (Default: False)
set_enable_webgl = True                                    # (Default: False)
set_enable_write_console_messages_to_stdout = False        # (Default: False)
set_enable_xss_auditor = True                              # (Default: True)
set_fantasy_font_family = "serif"                          # (Default: "serif")
set_javascript_can_access_clipboard = False                # (Default: False)
set_javascript_can_open_windows_automatically = False      # (Default: False)
set_load_icons_ignoring_image_load_setting = False         # (Default: False)
set_media_playback_allows_inline = True                    # (Default: True)
set_media_playback_requires_user_gesture = False           # (Default: False)
set_minimum_font_size = 0                                  # (Default: 0)
set_monospace_font_family = "monospace"                    # (Default: "monospace")
set_pictograph_font_family = "serif"                       # (Default: "serif")
set_print_backgrounds = True                               # (Default: True)
set_sans_serif_font_family = "sans-serif"                  # (Default: "sans-serif")
set_serif_font_family = "serif"                            # (Default: "serif")
set_user_agent = None                                      # (Default: None)
set_zoom_text_only = False                                 # (Default: False)

'''
#####################
# Paranoid Settings #                                      HINT: Enable/Disable Javascript, Java, Flash and other security compromising stuff directly from WebKit2 settings
#####################
'''

cookies_policy = 2                                         # Cookies policy (Default: 2) (eg. set 1 to disable cookies) (Always = 0, Never = 1, No Third Party = 2)
geolocation_policy = 2                                     # Geolocation policy (Default: 2) (eg. set 1 to disable geolocation) (Always = 0, Never = 1, Ask Everytime = 2)
adkiller = True                                            # AdKiller (a pseudo-alternative to AdBlock Plus) (Default: True) (Experimental)
                                                           # It's actually experimental and at the moment it won't manipulate the DOM to remove ads.
defcon = False                                             # Defcon mode (Default: False) If 'True', browser will disable cache, ignore history and cookies
                                                           # independently from their policies.

'''
########
# MIME # 
########
'''

mime_view = [

"application/xml", "application/rss+xml", "application/atom+xml", "application/json"

]

evince_mime = [

"application/pdf", "application/x-bzpdf", "application/x-gzpdf", "application/x-xzpdf", "application/x-ext-pdf", "application/x-dvi",\
"application/x-bzdvi", "application/x-gzdvi", "application/x-ext-dvi","image/tiff", "application/postscript", "application/x-bzpostscript", \
"application/x-gzpostscript", "image/x-eps", "image/x-bzeps", "image/x-gzeps", "application/x-ext-ps", "application/x-ext-eps", "image/vnd.djvu",\
"image/vnd.djvu+multipage", "application/x-ext-djv", "application/x-ext-djvu", "application/x-cbr application/x-cbz", "application/x-cb7",\
"application/x-cbt", "application/x-ext-cbr", "application/x-ext-cbz", "application/x-ext-cb7", "application/x-ext-cbt", "application/oxps",\
"application/vnd.ms-xpsdocument"

]

'''
###############
# URI Schemes #
###############
'''

uri_schemes = [

"magnet:?xt=urn:", "mailto:", "apt:", "ed2k:"

]

'''
###############
# Paths Check #
###############
'''

if not os.path.exists(base_path): os.makedirs(base_path)
if not os.path.exists(cookies_path): os.makedirs(cookies_path)
if not os.path.exists(pickle_path): os.makedirs(pickle_path)
if not os.path.exists(theme_path): os.makedirs(theme_path)

'''
##########
# Pickle #
##########
'''

adk_name = "adkiller.p"
adb_name = "adblocks.p"

if adkiller: pickle.dump(True, open("{}{}".format(pickle_path, adk_name), "wb"))
else: pickle.dump(False, open("{}{}".format(pickle_path, adk_name), "wb"))

pickle.dump(0, open("{}{}".format(pickle_path, adb_name), "wb"))

'''
#############
# Databases #
#############
'''

cookies_con = lite.connect("{}/{}".format(cookies_path, cookies_db))

if not os.path.exists("{}{}".format(history_path,history_db)):

    os.makedirs(history_path)

    history_con = lite.connect("{}/{}".format(history_path, history_db))

    with history_con:
        history_cur = history_con.cursor()    
        history_cur.execute("CREATE TABLE history(title TEXT, url TEXT, date TEXT);")

if not os.path.exists("{}{}".format(bookmarks_path, bookmarks_db)):

    os.makedirs(bookmarks_path)

    bookmarks_con = lite.connect("{}/{}".format(bookmarks_path, bookmarks_db))

    with bookmarks_con:
        bookmarks_cur = bookmarks_con.cursor()    
        bookmarks_cur.execute("CREATE TABLE bookmarks(title TEXT, url TEXT, date TEXT);")

history_con = lite.connect("{}/{}".format(history_path, history_db))
bookmarks_con = lite.connect("{}/{}".format(bookmarks_path, bookmarks_db))

