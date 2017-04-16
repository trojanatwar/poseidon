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

import sys, gi, datetime
from OpenSSL import crypto
from gi.repository import Gtk
from gi.repository.GtkSource import Buffer, View

sys.path.append(".")
from functions import get_domain, reveal, val_sec_string

def time_parse(raw):
    raw = raw.decode("utf8", "replace").replace('Z', '')
    return datetime.datetime.strptime(raw, '%Y%m%d%H%M%S')

def buf_replace(buf):

    buf = buf.replace("C:", "C [{}]:".format(_("Country Name"))).\
    replace("ST:", "ST [{}]:".format(_("State Or Province Name"))).\
    replace("L:", "L [{}]:".format(_("Locality"))).\
    replace("O:", "O [{}]:".format(_("Organization"))).\
    replace("CN:", "CN [{}]:".format(_("Common Name"))).\
    replace("OU:", "OU [{}]:".format(_("Organizational Unit"))).\
    replace("SN:", "SN [{}]:".format(_("Surname"))).\
    replace("GN:", "GN [{}]:".format(_("Given Name")))

    return buf

def secure(sec, url, message, box, button):

    url = get_domain(url)

    if sec == 1:
        message.set_markup("<span size='small'>{} {}.\r{}.</span>".format(url, _("has no security"),\
        _("An attacker could see any information you send, or control the content that you see")))
        box.show_all()
        reveal(box, True)
        button.hide()
        return

    if sec == 0: message.set_markup("<span size='small'>{} {}\r{}</span>".format(_("Connected to"),\
    url, _("Your connection seems to be secure. Want to know more about?")))

    if sec == 2: message.set_markup("<span size='small'>{} {}\r{}</span>".format(_("Connected to"),\
    url, _("This web site did not properly secure your connection. Want to know more about?")))

    box.show_all()
    reveal(box, True)

def certificate(data, arg):

    https, certificate, flags = data

    if https and certificate is not None: pem_certificate = certificate.props.certificate_pem
    else: pem_certificate = None

    if pem_certificate:

        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, pem_certificate)
        extensions = [x509.get_extension(i) for i in range(x509.get_extension_count())]
        keyed_extensions = {}
            
        for ext in extensions:
            
            name = ext.get_short_name().decode("utf8", "replace")
                
            try: value = str(ext)
            except Exception: value = 'Value unavailable'
            keyed_extensions[name] = value

        if arg == 1:

            buf = "<b>{}</b>\n\n".format(_("Subject"))
            buf += "\n".join(b": ".join(kv).decode("utf8", "replace") for kv in x509.get_subject().get_components())
            buf = buf_replace(buf)

            return buf

        if arg == 2:

            buf = "<b>{}</b>\n\n".format(_("Issuer"))
            buf += "\n".join(b": ".join(kv).decode("utf8", "replace") for kv in x509.get_issuer().get_components())
            buf = buf_replace(buf)

            return buf

        if arg == 3:

            start = time_parse(x509.get_notBefore())
            end = time_parse(x509.get_notAfter())
            buf = "<b>{}</b>\n\n{} - {}".format(_("Valid Time Range"), start, end)
            
            return buf

        if arg == 4:

            buf = "<b>{}</b>\n\n".format(_("Subject Alternative Names"))
            buf += val_sec_string(keyed_extensions.get("subjectAltName", "").replace(", ", "\n"))

            return buf

        if arg == 5:

            buf = "<b>{}</b>\n\n".format(_("Subject Key Identifier"))
            skeyid = val_sec_string(keyed_extensions.get("subjectKeyIdentifier", "").replace(", ", "\n"))

            if skeyid:
                buf += skeyid
            else:
                buf += "?"

            return buf

        if arg == 6:

            buf = "<b>{}</b>\n\n".format(_("Key Usage"))
            buf += val_sec_string(keyed_extensions.get("keyUsage", "").replace(", ", "\n"))

            return buf

        if arg == 7:

            buf = "<b>{}</b>\n\n".format(_("Extended Key Usage"))
            buf += val_sec_string(keyed_extensions.get("extendedKeyUsage", "").replace(", ", "\n"))

            return buf

        if arg == 8:

            buf = "<b>{}</b>\n".format(_("Distribution Points"))
            buf += val_sec_string(keyed_extensions.get("crlDistributionPoints", "").replace(", ", "\n"))

            return buf

        if arg == 9:

            buf = "<b>{}</b>\n\n".format(_("Certificate Policies"))
            buf += val_sec_string(keyed_extensions.get("certificatePolicies", "").replace(", ", "\n"))

            return buf

        if arg == 10:

            buf = "<b>{}</b>\n\n".format(_("Basic Constraints"))
            buf += val_sec_string(keyed_extensions.get("basicConstraints", "").replace(", ", "\n"))

            return buf

        if arg == 11:

            buf = "<b>{}</b>\n\n".format(_("Authority Key Identifier"))
            buf += val_sec_string(keyed_extensions.get("authorityKeyIdentifier", "").replace(", ", "\n").replace("keyid:", ""))

            return buf

        if arg == 12:

            buf = "<b>{}</b>\n\n".format(_("Authority Info Access"))
            buf += val_sec_string(keyed_extensions.get("authorityInfoAccess", "").replace(", ", "\n"))

            return buf

        if arg == 13:

            t = _("Signature Algorithm")

            try:

                buf = "<b>{}</b>\n\n{}".format(t,\
                x509.get_signature_algorithm().decode("utf8", "replace"))

            except BaseException as e:

                buf = "<b>{}</b>\n\n{}.\n{}: {}".format(t,\
                _("In order to show signature algorithm you need to install a newer version of pyOpenSSL"),\
                _("Error found"), e)

            return buf

        if arg == 14:

            buf = pem_certificate

            return buf

def cert_declarations(data, arg):

        action = certificate(data, arg)

        box = Gtk.Frame(name="frame_x509")

        if arg == 14:

            view = View()
            view.set_auto_indent(True)
            view.set_show_line_numbers(True)
            view.set_wrap_mode(Gtk.WrapMode.WORD)
            view.set_monospace(True)
            view.get_buffer().set_text(action)
            view.set_can_focus(False)

            box.add(view)
 
            return box

        label = Gtk.Label(name="label_x509")
        label.set_selectable(True)
        label.set_can_focus(False)
        label.set_alignment(0.0, 0.0)
        label.set_markup(action)

        box.add(label)

        return box

