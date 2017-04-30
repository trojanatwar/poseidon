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

import sys, requests, sqlite3 as lite, json

sys.path.append(".")
from functions import minify
from settings import autocomplete_policy, autocomplete_limit,\
history_con, bookmarks_con, cookies_con, verify_req, language,\
language_list

def autocomplete(query, liststore):

    if query:

        liststore.clear()

        if autocomplete_policy == 1:

            tmp = []
            tmp_ap = tmp.append

            with history_con:    
                cur = history_con.cursor()
                cur.execute("SELECT DISTINCT title,url FROM history LIMIT {};".format(autocomplete_limit))
                urls = cur.fetchall()

                if len(urls) != 0:
                    for url in urls:
                        tmp_ap(["{} | {}".format(minify(url[0], 50), minify(url[1], 100))] + [url[1]])

                for i in tmp: liststore.append(tuple(i))

            return True

        else:

            if autocomplete_policy == 2: url = ("https://ac.duckduckgo.com/ac/?q={}&type=list".format(query))
            if autocomplete_policy == 3: url = ("https://{}.wikipedia.org/w/api.php?action=opensearch&search={}".format(language_list[language].split("_")[0], query))
            if autocomplete_policy == 4: url = ("https://suggestqueries.google.com/complete/search?json&client=firefox&q={}".format(query))
            if autocomplete_policy == 5: url = ("https://suggestqueries.google.com/complete/search?json&client=firefox&ds=yt&q={}".format(query))
            if autocomplete_policy == 6: url = ("https://completion.amazon.co.uk/search/complete?method=completion&q={}&search-alias=aps&mkt=4".format(query))

            request = requests.get(url, stream=True, verify=bool(verify_req))
            request = json.loads(request.content.decode('utf-8'))

            for i in request:
                if i and type(i) == list:
                    for a in i:
                        try: liststore.append([a])
                        except ValueError: pass

            return True

def cookiesview():

    tmp = []
    cookies = []
    tmp_ap = tmp.append
    cookies_ap = cookies.append
        
    with cookies_con:    
        cur = cookies_con.cursor()
        cur.execute("SELECT * FROM moz_cookies;")
        cks = cur.fetchall()

        for i in cks:
            tmp_ap([i[0]] + [i[1]] + [minify(i[2],50)] + [i[3]] + [i[4]] +\
                   [i[5]] + [i[6]] + [i[7]] + [i[8]] + [i[2]])
        
        for i in tmp: cookies_ap(tuple(i))

        return cookies

def bookmarksview():

    tmp = []
    bookmarks = []
    tmp_ap = tmp.append
    bookmarks_ap = bookmarks.append
        
    with bookmarks_con:    
        cur = bookmarks_con.cursor()
        cur.execute("SELECT * FROM bookmarks ORDER BY date DESC;")
        urls = cur.fetchall()

        for i in urls: tmp_ap([i[2]] + [minify(i[0],50)] + [minify(i[1],50)] + [i[1]])
        for i in tmp: bookmarks_ap(tuple(i))

        return bookmarks

def historyview():

    tmp = []
    history = []
    tmp_ap = tmp.append
    history_ap = history.append
        
    with history_con:    
        cur = history_con.cursor()
        cur.execute("SELECT * FROM history ORDER BY date DESC;")
        urls = cur.fetchall()

        for i in urls: tmp_ap([i[2]] + [minify(i[0],50)] + [minify(i[1],50)] + [i[1]])
        for i in tmp: history_ap(tuple(i))

        return history

