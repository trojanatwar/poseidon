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

import os, gettext, pickle, sqlite3 as lite, subprocess

'''
#####################
# Advanced Settings #
#############################################
# The following variables can be manually   #
# edited as long you know what you're doing #
#############################################
'''

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
settings_path = "{}settings/".format(base_path)            # Settings path
pickle_path = "{}pickle/".format(base_path)                # Pickle path
theme_path = "{}theme/".format(base_path)                  # Theme path
theme_file = "{}theme".format(theme_path)                  # Theme file path
pages_path = "pages"                                       # Pages path
lib_path = "lib"                                           # Library path
lc_path = "po/locale"                                      # Languages path

cookies_db = "cookies.sqlite"                              # Cookies database (Default: "cookies.sqlite")
history_db = "history.sqlite"                              # History database (Default: "history.sqlite")
bookmarks_db = "bookmarks.sqlite"                          # Bookmarks database (Default: "bookmarks.sqlite")
settings_db = "settings.sqlite"                            # Settings database (Default: "settings.sqlite")

'''
#####################
# Autistic Settings #                                      One String to rule them all, One String to find them, One String to bring them all and in the Memory store them.
#####################
'''
                                                           # Integers

width = 800                                                # Window width size (Default: 800)
height = 600                                               # Window height size (Default: 600)
autocomplete_limit = -1                                    # Autocomplete limit (Default: -1) (Disabled = -1)
                                                           # For example, setting 500 will show 500 results if autocomplete policy is 0
favicon_size = 16                                          # Favicon size (Default: 16)
                                                           # Visited links will show in a popover when you hold back/forward buttons for these seconds.
load_timeout = 0                                           # Load timeout (Default: 0) (30000 = 30 seconds) (set 0 to disable it)
                                                           # If loading a website takes longer than set seconds browser will return a popup dialog with the issue.
                                                           # Increase the value in case your connection is very slow, 25000 is a good deal.
adk_policy = 1                                             # AdKiller policy (Default: 1) (Global = 0, Precise = 1)
                                                           # If "Global", AdKiller will check if the requested url is in list.
                                                           # This method is ultra simple and fast but can misunderstand a request like "downloads.domain.com" for "ads.domain.com".
                                                           # If "Precise", AdKiller will check if the requested url is identical to one of the listed urls.
                                                           # This method is a bit slower (anyway, not so considerably) but 100% precise.

                                                           # Booleans

verify_req = True                                          # Requests module SSL verification (Default: True)
                                                           # If 'False', 'requests' module will ignore verifying the SSL certificate
                                                           # False = insecure (but faster), True = secure (but slower)

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
set_enable_mediasource = True                              # (Default: False)
set_enable_offline_web_application_cache = True            # (Default: True)
set_enable_page_cache = True                               # (Default: True)
set_enable_plugins = True                                  # (Default: True)
#set_enable_private_browsing                               # (Managed by Defcon Mode)
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
##########################
# Settings for GUI usage #
###############################################
# Following settings doesn't requires editing #
###############################################
'''

'''
###############
# Paths Check #
###############
'''

if not os.path.exists(base_path): os.makedirs(base_path)
if not os.path.exists(settings_path): os.makedirs(settings_path)
if not os.path.exists(history_path): os.makedirs(history_path)
if not os.path.exists(bookmarks_path): os.makedirs(bookmarks_path)
if not os.path.exists(cookies_path): os.makedirs(cookies_path)
if not os.path.exists(pickle_path): os.makedirs(pickle_path)
if not os.path.exists(theme_path): os.makedirs(theme_path)

'''
#############
# Databases #
#############
'''

if not os.path.exists("{}{}".format(history_path, history_db)):

    con = lite.connect("{}/{}".format(history_path, history_db))

    with con:
        cur = con.cursor()    
        cur.execute("CREATE TABLE history(title TEXT, url TEXT, date TEXT);")

if not os.path.exists("{}{}".format(bookmarks_path, bookmarks_db)):

    con = lite.connect("{}/{}".format(bookmarks_path, bookmarks_db))

    with con:
        cur = con.cursor()    
        cur.execute("CREATE TABLE bookmarks(title TEXT, url TEXT, date TEXT);")

history_con = lite.connect("{}/{}".format(history_path, history_db))
bookmarks_con = lite.connect("{}/{}".format(bookmarks_path, bookmarks_db))
cookies_con = lite.connect("{}/{}".format(cookies_path, cookies_db))

'''
################################
# Initialize Settings Database #
################################
'''

slist = []

if os.path.exists("{}{}".format(settings_path, settings_db)):

    con = lite.connect("{}/{}".format(settings_path, settings_db))

    with con:    
        cur = con.cursor()
        cur.execute("SELECT * FROM settings;")
        opts = cur.fetchall()
        slist = opts

'''
###########
# Methods #
###########
'''

def std():
    if len(slist) == 0: return True

def rop(value, list, bool):
    for a in range(len(list)):
        if bool:
            if value == list[a]:
                return a
        else:
            if value == a:
                return list[a]

def ctt(s): return s.title().replace("_", " ")

def get_available_shells():

     list = []

     for i in subprocess.check_output(["cat", "/etc/shells"])\
     .decode("utf8", "replace").split("\n"):
         if not i.startswith("#") and i != "": list.append(i)

     return list

'''
####################
# Default Settings #
####################
'''

search_engine = "https://duckduckgo.com/?q="
home_page = "https://www.duckduckgo.com/"
app_launcher = "xdg-open"
language = 0
autocomplete_policy = 1
shell = 0
find = 1
cache_model = 1
cookies_policy = 2
geolocation_policy = 2
adkiller = 1

'''
#########
# Lists #
#########
'''

language_list = ["en_US", "it_IT"]                         # Languages list
adkiller_list = ["Disabled", "Enabled"]                    # Adkiller list
autocomplete_policy_list = ["Disable Autocomplete",\
"Secure: History", "Secure: DuckDuckGo",\
"Secure: Wikipedia", "Spyware: Google",\
"Spyware: Youtube", "Spyware: Amazon"]                     # Autocomplete list
find_list = ["Case Insensitive",\
"Wrap Around" ,"At Words Starts",\
"Treat Medial Capial As Word Start", "Backwards"]          # Find list
cache_model_list = ["Disable Cache",\
"Improved for Speed",\
"Optimized for Local Files"]                               # Cache list
cookies_policy_list = ["Always Enabled",\
"Never Enabled", "No Third Party"]                         # Cookies list
geolocation_policy_list = ["Always Enabled",\
"Never Enabled", "Ask Everytime"]                          # Geolocation list
shell_list = get_available_shells()                        # Shells list

'''
#######################################
# Save/Load Settings to/from Database #
#######################################
'''

sdlist = ["search_engine", "home_page", "app_launcher", "language",\
"adkiller", "shell", "cache_model", "find", "autocomplete_policy",\
"cookies_policy", "geolocation_policy"]

if not std():

    for c, i in enumerate(sdlist):

        value = slist[c][1]
        vlist = slist[c][2]

        if vlist:
            if i == sdlist[c]: value = rop(value, globals()[vlist], 1)

        if i == "find":
            if value == find_list[0]: value = 1
            if value == find_list[1]: value = 16
            if value == find_list[2]: value = 2
            if value == find_list[3]: value = 4
            if value == find_list[4]: value = 8

        globals()[i] = value

if not os.path.exists("{}{}".format(settings_path, settings_db)):

    con = lite.connect("{}/{}".format(settings_path, settings_db))

    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE settings(option TEXT, value TEXT, list TEXT);")

        for c, i in enumerate(sdlist):

            value = globals()[i]
            vlist = ""

            if type(value) == int:

                if i == sdlist[c]:
                    vlist = "{}_list".format(i)
                    value = rop(value, globals()[vlist], 0)

                if i == "find":
                    if value == 1: value = find_list[0]
                    if value == 16: value = find_list[1]
                    if value == 2: value = find_list[2]
                    if value == 4: value = find_list[3]
                    if value == 8: value = find_list[4]

            cur.execute("INSERT INTO settings VALUES(?, ?, ?);", (ctt(i), value, vlist))

settings_con = lite.connect("{}/{}".format(settings_path, settings_db))

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
####################
# Install Language #
####################
'''

lang = gettext.translation(language_list[language], localedir=lc_path, languages=language_list)
lang.install()

'''
################
# Dev Settings #
################
'''

version = "0.2.6"
browser_name = "Poseidon"
website = "https://github.com/sidus-dev/poseidon"
authors = "Andrea Pasciuta  <sidus@arbornet.org>"
comments = _("A fast, minimal and lightweight browser")
tab_name = _("Empty")

