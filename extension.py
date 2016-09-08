#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, pickle
from os import path
sys.path.append("include")
from settings import adk_filters_path, pickle_path, adk_name, adb_name
from dialog import *

adk_rules = []
adk_data = []
adk_blocks = []

def initialize(extension):
    
    adk_data.append(pickle_path)
    adk_data.append(adk_name)
    adk_data.append(adb_name)

    adk_combo = adk_init(adk_filters_path)
    replacement(adk_combo)
    extension.connect("page-created", on_page_created)

def on_page_created(extension, webpage):

    webpage.connect("send-request", on_send_request)

def on_send_request(webpage, request, redirect):

    url = request.get_uri()

    if url.startswith("ftp://"): url = request.set_uri(url.replace("ftp://", "http://"))

    if pickle.load(open("{}{}".format(adk_data[0], adk_data[1]), "rb")):

        url = request.get_uri()

        if "://" in url and not "file://" in url:
            if adk(url, adk_rules):

                adk_blocks.append(" ")
                pickle.dump(len(adk_blocks), open("{}{}".format(adk_data[0], adk_data[2]), "wb"))

                return True

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

def adk(arg, rules):
    for i in rules:
        if i in arg: return True

def combined(filenames):
    for filename in filenames:
        with open(filename) as file:
            for line in file:
                yield line

