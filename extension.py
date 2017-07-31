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

import os, sys
from os import path
sys.path.append("include")
from settings import read_file, adk_file, adk_filters_path, adk_policy
from dialog import *

adk_rules = []

def initialize(extension, args):

    adk_combo = adk_init(adk_filters_path)
    replacement(adk_combo)
    extension.connect("page-created", on_page_created)

def on_page_created(extension, webpage):

    webpage.connect("send-request", on_send_request)

def on_send_request(webpage, request, redirect):

    url = request.get_uri()

    if read_file(adk_file) == "1":

        if "://" in url and not "file://" in url:
            if adk(url, adk_rules): return True

'''
############
# AdKiller #
############
'''

def replacement(combo):

    for i in combo:

        if i.startswith("!"):
            err = "{}...".format(_("Houston, we have a problem"))
            msg = "<span size='small'>{}. {}.\n\n{}:\n{}</span>".\
            format(_("An AdBlockPlus filter has been detected in your 'filters' folder but actually AdKiller only works with AdAway filters"),\
            _("In order to avoid any issues or incompatibilities, remove that filter and restart this program"),\
            _("Get your AdAway filter list here"),"https://github.com/AdAway/AdAway/wiki/HostsSources")
            dialog().error(err, msg)
            return True
 
        if i.startswith("#"): continue
        i = i.replace("\t","").replace(" ","").strip().replace("127.0.0.1","").replace("0.0.0.0","").split("#")[0]
        if i != '': adk_rules.append(i)

def adk_init(filters_path):

    filters = []
    filters_path = "{}/".format(filters_path)
    list = os.listdir(filters_path)

    for i in range(len(list)):
        if ".txt" in list[i]: filters.append("{}{}".format(filters_path, list[i]))

    return combined(filters)

def adk(url, rules):

    if adk_policy:
        domain = url.split("://",1)[1].split("/",1)[0]
        if any(c for c in rules if c == domain): return True
    else:
        if any(c for c in rules if c in url): return True

def combined(filenames):
    for filename in filenames:
        with open(filename) as file:
            for line in file: yield line

