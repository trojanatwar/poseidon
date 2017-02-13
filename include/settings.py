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

import os, platform, gettext, pickle, sqlite3 as lite, subprocess, shutil

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

base_path = "{}/.poseidon/"\
.format(os.path.expanduser('~'))                           # Base path
icns = "icons/"                                            # Icons path
adk_filters_path = "filters"                               # AdKiller filters path
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
####################
# Deprecated Stuff #
####################
'''

cache_path = "{}cache".format(base_path)                   # Cache path (Deprecated since 0.4.1 since WebKit2.WebsiteDataManager() is now used)
if os.path.exists(cache_path): shutil.rmtree(cache_path)

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

"aim:", "apt:", "bitcoin:", "callto:", "ed2k:", "fax:", "gtalk:", "irc:", "irc6:", "ircs:", "lastfm:", "magnet:?xt=urn:",\
"mailto:", "secondlife:", "skype:", "smb:", "sms:", "steam:", "tel:", "unreal:", "ut2004:"

]

'''
################
# Charset List #
################
'''

charset_list = [

"ANSI_X3.110-1983", "ANSI_X3.4-1968", "ARMSCII-8", "ASMO_449", "BIG5", "BIG5-HKSCS", "BRF", "BS_4730",\
"BS_VIEWDATA", "CP10007", "CP1125", "CP1250", "CP1251", "CP1252", "CP1253", "CP1254", "CP1255", "CP1256", "CP1257",\
"CP1258", "CP737", "CP770", "CP771", "CP772", "CP773", "CP774", "CP775", "CP949", "CSA_Z243.4-1985-1", "CSA_Z243.4-1985-2",\
"CSA_Z243.4-1985-GR", "CSN_369103", "CWI", "DEC-MCS", "DIN_66003", "DS_2089", "EBCDIC-AT-DE", "EBCDIC-AT-DE-A", "EBCDIC-CA-FR",\
"EBCDIC-DK-NO", "EBCDIC-DK-NO-A", "EBCDIC-ES", "EBCDIC-ES-A", "EBCDIC-ES-S", "EBCDIC-FI-SE", "EBCDIC-FI-SE-A", "EBCDIC-FR",\
"EBCDIC-IS-FRISS", "EBCDIC-IT", "EBCDIC-PT", "EBCDIC-UK", "EBCDIC-US", "ECMA-CYRILLIC", "ES", "ES2", "EUC-JISX0213",\
"EUC-JP", "EUC-JP-MS", "EUC-KR", "EUC-TW", "GB18030", "GB2312", "GBK", "GB_1988-80", "GEORGIAN-ACADEMY", "GEORGIAN-PS",\
"GOST_19768-74", "GREEK-CCITT", "GREEK7", "GREEK7-OLD", "HP-GREEK8", "HP-ROMAN8", "HP-ROMAN9", "HP-THAI8", "HP-TURKISH8",\
"IBM037", "IBM038", "IBM1004", "IBM1026", "IBM1047", "IBM1124", "IBM1129", "IBM1132", "IBM1133", "IBM1160", "IBM1161",\
"IBM1162", "IBM1163", "IBM1164", "IBM256", "IBM273", "IBM274", "IBM275", "IBM277", "IBM278", "IBM280", "IBM281",\
"IBM284", "IBM285", "IBM290", "IBM297", "IBM420", "IBM423", "IBM424", "IBM437", "IBM500", "IBM850", "IBM851",\
"IBM852", "IBM855", "IBM856", "IBM857", "IBM860", "IBM861", "IBM862", "IBM863", "IBM864", "IBM865", "IBM866",\
"IBM866NAV", "IBM868", "IBM869", "IBM870", "IBM871", "IBM874", "IBM875", "IBM880", "IBM891", "IBM903", "IBM904",\
"IBM905", "IBM918", "IBM922", "IEC_P27-1", "INIS", "INIS-8", "INIS-CYRILLIC", "INVARIANT", "ISIRI-3342", "ISO-8859-1",\
"ISO-8859-10", "ISO-8859-11", "ISO-8859-13", "ISO-8859-14", "ISO-8859-15", "ISO-8859-16", "ISO-8859-2", "ISO-8859-3",\
"ISO-8859-4", "ISO-8859-5", "ISO-8859-6", "ISO-8859-7", "ISO-8859-8", "ISO-8859-9", "ISO-8859-9E", "ISO-IR-197",\
"ISO-IR-209", "ISO-IR-90", "ISO_10367-BOX", "ISO_10646", "ISO_11548-1", "ISO_2033-1983", "ISO_5427", "ISO_5427-EXT",\
"ISO_5428", "ISO_646.BASIC", "ISO_646.IRV", "ISO_6937", "ISO_6937-2-25", "ISO_6937-2-ADD", "ISO_8859-1,GL",\
"ISO_8859-SUPP", "IT", "JIS_C6220-1969-JP", "JIS_C6220-1969-RO", "JIS_C6229-1984-A", "JIS_C6229-1984-B",\
"JIS_C6229-1984-B-ADD", "JIS_C6229-1984-HAND", "JIS_C6229-1984-HAND-ADD", "JIS_C6229-1984-KANA", "JIS_X0201",\
"JOHAB", "JUS_I.B1.002", "JUS_I.B1.003-MAC", "JUS_I.B1.003-SERB", "KOI-8", "KOI8-R", "KOI8-RU", "KOI8-T",\
"KOI8-U", "KSC5636", "LATIN-GREEK", "LATIN-GREEK-1", "MAC-CENTRALEUROPE", "MAC-CYRILLIC", "MAC-IS", "MAC-SAMI",\
"MAC-UK", "MACINTOSH", "MAC_CENTRALEUROPE", "MIK", "MSZ_7795.3", "NATS-DANO", "NATS-DANO-ADD", "NATS-SEFI",\
"NATS-SEFI-ADD", "NC_NC00-10", "NEXTSTEP", "NF_Z_62-010", "NF_Z_62-010_(1973)", "NF_Z_62-010_1973",\
"NS_4551-1", "NS_4551-2", "PT", "PT154", "PT2", "RK1048", "SAMI", "SAMI-WS2", "SEN_850200_B",\
"SEN_850200_C", "SHIFT_JIS", "SHIFT_JISX0213", "T.101-G2", "T.61-7BIT", "T.61-8BIT", "TCVN5712-1", "TIS-620",\
"TSCII", "UTF-8", "VIDEOTEX-SUPPL", "VISCII", "WIN-SAMI-2", "WINDOWS-31J"

]

'''
###################
# User Agent List #
###################
'''

ua_moz = "Mozilla/5.0"
ua_sys = "({} {})".format(platform.system(), platform.machine())
ua_mos = "{} {}".format(ua_moz, ua_sys)

ua_browsers_dsc = [

"Google Chrome", "Google Chrome (Windows)", "Google Chrome (Mac)", "Mozilla Firefox", "Mozilla Firefox (Windows)", "Mozilla Firefox (Mac)",\
"Opera 9.80", "Opera 9.80 (Windows)", "Opera 9.80 (Mac)", "Internet Explorer 11.0", "Internet Explorer 10.6", "Internet Explorer 10.0", "Internet Explorer 9.0",\
"Internet Explorer 8.0", "Microsoft Edge"

]

ua_browsers_val = [

"{} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36".format(ua_mos),\
"{} (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36".format(ua_moz),\
"{} (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36".format(ua_moz),\
"{} Gecko/20100101 Firefox/40.1".format(ua_mos),\
"{} (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1".format(ua_moz),\
"{} (Macintosh; Intel Mac OS X 10_10; rv:40.0) Gecko/20100101 Firefox/40.1".format(ua_moz),\
"Opera/9.80 {} Presto/2.12.388 Version/12.16".format(ua_sys),\
"Opera/9.80 (Windows NT 6.1) Presto/2.12.388 Version/12.16",\
"Opera/9.80 (Macintosh; Intel Mac OS X 10_10_1) Presto/2.12.388 Version/12.16",\
"{} (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko".format(ua_moz),\
"{} (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:10.6) like Gecko".format(ua_moz),\
"{} (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:10.0) like Gecko".format(ua_moz),\
"{} (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:9.0) like Gecko".format(ua_moz),\
"{} (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:8.0) like Gecko".format(ua_moz),\
"{} (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246".format(ua_moz)

]

ua_mobile_dsc = [

"Android Webkit Browser", "IE Mobile 9.0", "Opera Mini 9.80", "Opera Mobile 12.02", "BlackBerry", "S60 OSS 3.0",\
"Apple iPhone", "Apple iPad"

]

ua_mobile_val = [

"{} (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30".format(ua_moz),\
"{} (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)".format(ua_moz),\
"Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.348; U; en) Presto/2.5.25 Version/10.54",\
"Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02",\
"{} (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+".format(ua_moz),\
"SamsungI8910/SymbianOS/9.1 Series60/3.0",\
"{} (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53".format(ua_moz),\
"{} (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53".format(ua_moz)

]

ua_crawlers_dsc = [

"Baiduspider 2.0", "Bingbot 2.0", "Googlebot 2.1", "Msnbot 2.1", "YahooSeeker 1.2", "YandexBot 3.0"

]

ua_crawlers_val = [

"{} (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)".format(ua_moz),\
"{} (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)".format(ua_moz),\
"{} (compatible; Googlebot/2.1; +http://www.google.com/bot.html)".format(ua_moz),\
"msnbot/2.1",\
"YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com; http://help.yahoo.com/help/us/shop/merchant/)",\
"{} (compatible; YandexBot/3.0; +http://yandex.com/bots)".format(ua_moz)

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
###########
# Methods #
###########
'''

def get_available_shells():

     list = []

     for i in subprocess.check_output(["cat", "/etc/shells"])\
     .decode("utf8", "replace").split("\n"):
         if not i.startswith("#") and i != "": list.append(i)

     return list

def get_font_families():

    list = []

    from tkinter import Tk, font
    root = Tk()
    default = ("serif", "sans-serif", "monospace")
    for i in default: list.append(i)
    for i in font.families():
        if i not in list: list.append(i)

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
autocomplete_limit = -1
shell = 0
find = 1
cache_model = 1
cookies_policy = 2
geolocation_policy = 2
adkiller = 1
adk_policy = 1
adk_popups = 1
load_timeout = 0
width = 800
height = 600
verify_req = 1
tab_cb = 0

'''
############################
# WebKit2 Default Settings #
############################

More info at: https://lazka.github.io/pgi-docs/WebKit2-4.0/classes/Settings.html#property-details

'''

set_allow_file_access_from_file_urls = 0
set_allow_modal_dialogs = 0
set_auto_load_images = 1
set_cursive_font_family = 0
set_default_charset = 139
set_default_font_family = 1
set_default_font_size = 16
set_default_monospace_font_size = 13
set_draw_compositing_indicators = 0
set_enable_accelerated_2d_canvas = 0
set_enable_caret_browsing = 0
set_enable_developer_extras = 1
set_enable_dns_prefetching = 0
set_enable_frame_flattening = 0
set_enable_fullscreen = 1
set_enable_html5_database = 1
set_enable_html5_local_storage = 1
set_enable_hyperlink_auditing = 0
set_enable_java = 1
set_enable_javascript = 1
set_enable_media_stream = 1
set_enable_mediasource = 1
set_enable_offline_web_application_cache = 1
set_enable_page_cache = 1
set_enable_plugins = 1
set_enable_resizable_text_areas = 1
set_enable_site_specific_quirks = 1
set_enable_smooth_scrolling = 0
set_enable_spatial_navigation = 0
set_enable_tabs_to_links = 1
set_enable_webaudio = 1
set_enable_webgl = 1
set_enable_write_console_messages_to_stdout = 0
set_enable_xss_auditor = 1
set_fantasy_font_family = 0
set_javascript_can_access_clipboard = 0
set_javascript_can_open_windows_automatically = 1
set_load_icons_ignoring_image_load_setting = 0
set_media_playback_allows_inline = 1
set_media_playback_requires_user_gesture = 0
set_minimum_font_size = 0
set_monospace_font_family = 2
set_pictograph_font_family = 0
set_print_backgrounds = 1
set_sans_serif_font_family = 1
set_serif_font_family = 0
set_user_agent = ""
set_zoom_text_only = 0

'''
#########
# Lists #
#########
'''

language_list = ["en_US", "it_IT", "de_DE"]
boolean_list = ["False", "True"]
adkiller_list = ["Disabled", "Enabled"]
adk_policy_list = ["Fastest", "Precise"]
adk_popups_list = ["Don't Block Pop-Ups", "Block Pop-Ups"]
verify_req_list = ["Insecure", "Secure"]
autocomplete_policy_list = ["Disable Autocomplete",\
"Secure: History", "Secure: DuckDuckGo",\
"Secure: Wikipedia", "Spyware: Google",\
"Spyware: Youtube", "Spyware: Amazon"]
find_list = ["Case Insensitive",\
"Wrap Around" ,"At Words Starts",\
"Treat Medial Capital As Word Start", "Backwards"]
cache_model_list = ["Disable Cache",\
"Improved for Speed",\
"Optimized for Local Files"]
cookies_policy_list = ["Always Enabled",\
"Never Enabled", "No Third Party"]
geolocation_policy_list = ["Always Enabled",\
"Never Enabled", "Ask Everytime"]
shell_list = get_available_shells()
font_list = get_font_families()


'''
#########
# Texts #
#########
'''

lang = gettext.translation(language_list[0],\
localedir=lc_path, languages=language_list).install()

text_blank_desc = _("Leave it empty to disable it")
text_home_page = _("Home Page")
text_search_engine = _("Search Engine")
text_app_launcher = _("Application Launcher")
text_app_launcher_desc = _("Set a application launcher")
text_language = _("Language")
text_language_desc = _("Set a language")
text_adkiller_desc = _("Enable or disable AdKiller")
text_adk_policy = _("AdKiller Policy")
text_adk_policy_desc = _("Set AdKiller behaviour")
text_adk_popups = _("AdKiller Pop-Ups Policy")
text_adk_popups_desc = _("Should AdKiller block pop-ups?")
text_tab_cb = _("Tab Close Button")
text_tab_cb_desc = _("Show a close button in the tabs?")
text_verify_req = _("Requests Module SSL Verification")
text_verify_req_desc = _("Set Requests Module SSL Verification behaviour")
text_autocomplete = _("Autocomplete")
text_autocomplete_desc = _("Set word completion for the main input field")
text_autocomplete_limit = _("Autocomplete Limit")
text_autocomplete_limit_desc = _("Set a limit for autocomplete results (eg. 500 = 500 results, -1 = disabled)")
text_find = _("Find Behaviour")
text_find_desc = _("Set finder behaviour")
text_cache_model = _("Cache Model")
text_cache_model_desc = _("Set the cache model")
text_geolocation = _("Geolocation")
text_geolocation_desc = _("Set geolocation behaviour")
text_shell_desc = _("Type of shell to use with VTE Terminal")
text_load_timeout = _("Load Timeout")
text_load_timeout_desc = _("Set load timeout in milliseconds (eg. 10000 = 10 seconds, 0 = disabled)")
text_width = _("Restored Window Width Size")
text_width_desc = _("Default width size for normal window")
text_height = _("Restored Window Height Size")
text_height_desc = _("Default height size for normal window")

'''
##################################
# Initializing Settings Database #
##################################
'''

settings_db_path = "{}{}".format(settings_path, settings_db)
settings_db_code = "2"

def create_settings_db():

    con = lite.connect("{}/{}".format(settings_path, settings_db))

    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE settings(title TEXT, value TEXT, type TEXT, desc TEXT, cat TEXT, other TEXT, option TEXT);")
        insert_string = "INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?, ?);"
        cur.execute(insert_string, ("code", settings_db_code, "0", "", "", "", ""))

        '''
        #####################################
        # Listing Settings Database Options #
        #####################################
        # . | Types           | Category    #
        #===|=================|=============#
        # 0 | None            | None        #
        # 1 | Text            | General     #
        # 2 | List            | Advanced    #
        # 3 |                 | O'Brien     #
        #####################################

        '''

        cur.execute(insert_string, (text_home_page, home_page, "1", text_blank_desc, "1", "", "home_page"))
        cur.execute(insert_string, (text_search_engine, search_engine, "1", text_blank_desc, "1", "", "search_engine"))
        cur.execute(insert_string, (text_app_launcher, app_launcher, "1", text_app_launcher_desc, "1", "", "app_launcher"))
        cur.execute(insert_string, (text_language, language, "2", text_language_desc, "1", "language_list", "language"))
        cur.execute(insert_string, ("AdKiller", adkiller, "2", text_adkiller_desc, "1", "adkiller_list", "adkiller"))
        cur.execute(insert_string, (text_tab_cb, tab_cb, "2", text_tab_cb_desc, "1", "boolean_list", "tab_cb"))
        cur.execute(insert_string, (text_autocomplete, autocomplete_policy, "2", text_autocomplete_desc, "2", "autocomplete_policy_list", "autocomplete_policy"))
        cur.execute(insert_string, (text_autocomplete_limit, autocomplete_limit, "1", text_autocomplete_limit_desc, "2", "", "autocomplete_limit"))
        cur.execute(insert_string, (text_find, find, "2", text_find_desc, "2", "find_list", "find"))
        cur.execute(insert_string, (text_adk_policy, adk_policy, "2", text_adk_policy_desc, "2", "adk_policy_list", "adk_policy"))
        cur.execute(insert_string, (text_adk_popups, adk_popups, "2", text_adk_popups_desc, "2", "adk_popups_list", "adk_popups"))
        cur.execute(insert_string, (text_verify_req, verify_req, "2", text_verify_req_desc, "2", "verify_req_list", "verify_req"))
        cur.execute(insert_string, (text_cache_model, cache_model, "2", text_cache_model_desc, "2", "cache_model_list", "cache_model"))
        cur.execute(insert_string, (text_geolocation, geolocation_policy, "2", text_geolocation_desc, "2", "geolocation_policy_list", "geolocation_policy"))
        cur.execute(insert_string, ("Shells", shell, "2", text_shell_desc, "2", "shell_list", "shell"))
        cur.execute(insert_string, (text_load_timeout, load_timeout, "1", text_load_timeout_desc, "2", "", "load_timeout"))
        cur.execute(insert_string, (text_width, width, "1", text_width_desc, "2", "", "width"))
        cur.execute(insert_string, (text_height, height, "1", text_height_desc, "2", "", "height"))

        '''
        ####################
        # WebKit2 Settings #
        ####################
        '''

        cur.execute(insert_string, ("set-allow-file-access-from-file-urls", set_allow_file_access_from_file_urls, "2", "Default: False", "3", "boolean_list", "set_allow_file_access_from_file_urls"))
        cur.execute(insert_string, ("set-allow-modal-dialogs", set_allow_modal_dialogs, "2", "Default: False", "3", "boolean_list", "set_allow_modal_dialogs"))
        cur.execute(insert_string, ("set-auto-load-images", set_auto_load_images, "2", "Default: True", "3", "boolean_list", "set_auto_load_images"))
        cur.execute(insert_string, ("set-cursive-font-family", set_cursive_font_family, "2", "Default: serif", "3", "font_list", "set_cursive_font_family"))
        cur.execute(insert_string, ("set-default-charset", set_default_charset, "2", "Default: ISO-8859-1", "3", "charset_list", "set_default_charset"))
        cur.execute(insert_string, ("set-default-font-family", set_default_font_family, "2", "Default: sans-serif", "3", "font_list", "set_default_font_family"))
        cur.execute(insert_string, ("set-default-font-size", set_default_font_size, "1", "Default: 16", "3", "", "set_default_font_size"))
        cur.execute(insert_string, ("set-default-monospace-font-size", set_default_monospace_font_size, "1", "Default: 13", "3", "", "set_default_monospace_font_size"))
        cur.execute(insert_string, ("set-draw-compositing-indicators", set_draw_compositing_indicators, "2", "Default: False", "3", "boolean_list", "set_draw_compositing_indicators"))
        cur.execute(insert_string, ("set-enable-accelerated-2d_canvas", set_enable_accelerated_2d_canvas, "2", "Default: False", "3", "boolean_list", "set_enable_accelerated_2d_canvas"))
        cur.execute(insert_string, ("set-enable-caret-browsing", set_enable_caret_browsing, "2", "Default: False", "3", "boolean_list", "set_enable_caret_browsing"))
        cur.execute(insert_string, ("set-enable-developer-extras", set_enable_developer_extras, "2", "Default: True", "3", "boolean_list", "set_enable_developer_extras"))
        cur.execute(insert_string, ("set-enable-dns-prefetching", set_enable_dns_prefetching, "2", "Default: False", "3", "boolean_list", "set_enable_dns_prefetching"))
        cur.execute(insert_string, ("set-enable-frame-flattening", set_enable_frame_flattening, "2", "Default: False", "3", "boolean_list", "set_enable_frame_flattening"))
        cur.execute(insert_string, ("set-enable-fullscreen", set_enable_fullscreen, "2", "Default: True", "3", "boolean_list", "set_enable_fullscreen"))
        cur.execute(insert_string, ("set-enable-html5-database", set_enable_html5_database, "2", "Default: True", "3", "boolean_list", "set_enable_html5_database"))
        cur.execute(insert_string, ("set-enable-html5-local-storage", set_enable_html5_local_storage, "2", "Default: True", "3", "boolean_list", "set_enable_html5_local_storage"))
        cur.execute(insert_string, ("set-enable-hyperlink-auditing", set_enable_hyperlink_auditing, "2", "Default: False", "3", "boolean_list", "set_enable_hyperlink_auditing"))
        cur.execute(insert_string, ("set-enable-java", set_enable_java, "2", "Default: True", "3", "boolean_list", "set_enable_java"))
        cur.execute(insert_string, ("set-enable-javascript", set_enable_javascript, "2", "Default: True", "3", "boolean_list", "set_enable_javascript"))
        cur.execute(insert_string, ("set-enable-media-stream", set_enable_media_stream, "2", "Default: False", "3", "boolean_list", "set_enable_media_stream"))
        cur.execute(insert_string, ("set-enable-mediasource", set_enable_mediasource, "2", "Default: False", "3", "boolean_list", "set_enable_mediasource"))
        cur.execute(insert_string, ("set-enable-offline-web-application-cache", set_enable_offline_web_application_cache, "2", "Default: True", "3", "boolean_list", "set_enable_offline_web_application_cache"))
        cur.execute(insert_string, ("set-enable-page-cache", set_enable_page_cache, "2", "Default: True", "3", "boolean_list", "set_enable_page_cache"))
        cur.execute(insert_string, ("set-enable-plugins", set_enable_plugins, "2", "Default: True", "3", "boolean_list", "set_enable_plugins"))
        cur.execute(insert_string, ("set-enable-resizable-text-areas", set_enable_resizable_text_areas, "2", "Default: True", "3", "boolean_list", "set_enable_resizable_text_areas"))
        cur.execute(insert_string, ("set-enable-site-specific-quirks", set_enable_site_specific_quirks, "2", "Default: True", "3", "boolean_list", "set_enable_site_specific_quirks"))
        cur.execute(insert_string, ("set-enable-smooth-scrolling", set_enable_smooth_scrolling, "2", "Default: False", "3", "boolean_list", "set_enable_smooth_scrolling"))
        cur.execute(insert_string, ("set-enable-spatial-navigation", set_enable_spatial_navigation, "2", "Default: False", "3", "boolean_list", "set_enable_spatial_navigation"))
        cur.execute(insert_string, ("set-enable-tabs-to-links", set_enable_tabs_to_links, "2", "Default: True", "3", "boolean_list", "set_enable_tabs_to_links"))
        cur.execute(insert_string, ("set-enable-webaudio", set_enable_webaudio, "2", "Default: False", "3", "boolean_list", "set_enable_webaudio"))
        cur.execute(insert_string, ("set-enable-webgl", set_enable_webgl, "2", "Default: False", "3", "boolean_list", "set_enable_webgl"))
        cur.execute(insert_string, ("set-enable-write-console-messages-to-stdout", set_enable_write_console_messages_to_stdout, "2", "Default: False", "3", "boolean_list", "set_enable_write_console_messages_to_stdout"))
        cur.execute(insert_string, ("set-enable-xss-auditor", set_enable_xss_auditor, "2", "Default: True", "3", "boolean_list", "set_enable_xss_auditor"))
        cur.execute(insert_string, ("set-fantasy-font-family", set_fantasy_font_family, "2", "Default: serif", "3", "font_list", "set_fantasy_font_family"))
        cur.execute(insert_string, ("set-javascript-can-access-clipboard", set_javascript_can_access_clipboard, "2", "Default: False", "3", "boolean_list", "set_javascript_can_access_clipboard"))
        cur.execute(insert_string, ("set-javascript-can-open-windows-automatically", set_javascript_can_open_windows_automatically, "2", "Default: False", "3", "boolean_list", "set_javascript_can_open_windows_automatically"))
        cur.execute(insert_string, ("set-load-icons-ignoring-image-load-setting", set_load_icons_ignoring_image_load_setting, "2", "Default: False", "3", "boolean_list", "set_load_icons_ignoring_image_load_setting"))
        cur.execute(insert_string, ("set-media-playback-allows-inline", set_media_playback_allows_inline, "2", "Default: True", "3", "boolean_list", "set_media_playback_allows_inline"))
        cur.execute(insert_string, ("set-media-playback-requires-user-gesture", set_media_playback_requires_user_gesture, "2", "Default: False", "3", "boolean_list", "set_media_playback_requires_user_gesture"))
        cur.execute(insert_string, ("set-monospace-font-family", set_monospace_font_family, "2", "Default: monospace", "3", "font_list", "set_monospace_font_family"))
        cur.execute(insert_string, ("set-pictograph-font-family", set_pictograph_font_family, "2", "Default: serif", "3", "font_list", "set_pictograph_font_family"))
        cur.execute(insert_string, ("set-print-backgrounds", set_print_backgrounds, "2", "Default: True", "3", "boolean_list", "set_print_backgrounds"))
        cur.execute(insert_string, ("set-sans-serif-font-family", set_sans_serif_font_family, "2", "Default: sans-serif", "3", "font_list", "set_sans_serif_font_family"))
        cur.execute(insert_string, ("set-serif-font-family", set_serif_font_family, "2", "Default: serif", "3", "font_list", "set_serif_font_family"))
        cur.execute(insert_string, ("set-user-agent", set_user_agent, "1", "Default: (N/A)", "3", "", "set_user_agent"))
        cur.execute(insert_string, ("set-zoom-text-only", set_zoom_text_only, "2", "Default: False", "3", "boolean_list", "set_zoom_text_only"))

def reinitialize_db():

    os.remove(settings_db_path)
    create_settings_db()

def restore_db(): os.remove(settings_db_path)

if os.path.exists(settings_db_path):

    con = lite.connect("{}/{}".format(settings_path, settings_db))

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM settings;")
        opts = cur.fetchall()
        
        if not "code" in opts[0][0]: reinitialize_db()
        else:
            if opts[0][1] != settings_db_code: reinitialize_db()
            else:
                for i in opts:
                    if i[2] != "0":
                        if i[2] == "1": value = i[1]
                        if i[2] == "2": value = int(i[1])
                        globals()[i[6]] = value

else: create_settings_db()

'''
#################################
# Settings Database Declaration #
#################################
'''

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

lang = gettext.translation(language_list[language],\
localedir=lc_path, languages=language_list).install()

'''
################
# Dev Settings #
################
'''

version = "0.4.6"
browser_name = "Poseidon"
website = "https://github.com/sidus-dev/poseidon"
authors = "Andrea Pasciuta  <sidus@arbornet.org>"
translators = "de - Marius Messerschmidt <marius.messerschmidt@googlemail.com>\n\
               it - Andrea Pasciuta  <sidus@arbornet.org>"
comments = _("A fast, minimal and lightweight browser")
tab_name = _("Empty")

