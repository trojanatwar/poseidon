# Poseidon
A fast, minimal and lightweight browser

## Screenshot

![Alt text](https://raw.githubusercontent.com/sidus-dev/screenshots/master/poseidon-0.7.1.png "Poseidon 0.7.1 on Arch Linux")

## Requirements

Requires [WebKit](https://webkitgtk.org/) 2.12.3 or higher.

## Installation

### Arch Linux

`$ yaourt -Sy poseidon-browser-git`

### Debian, Mint, Ubuntu

[Download & install .deb packages](https://github.com/sidus-dev/poseidon/releases)

* Optional dependencies

`# apt install gir1.2-evince-3.0 browser-plugin-evince`

### Fedora (tested on 25 Workstation)

* Required dependencies

`# dnf install python3 python3-requests python3-six python3-decorator python3-cairo python3-pillow python3-pyOpenSSL python-pysocks pygobject3 webkitgtk4 webkitgtk4-jsc gtksourceview3`

* Development dependencies

`# dnf install python3-devel webkitgtk4-devel pygobject3-devel`

* Optional dependencies

`# dnf install evince-browser-plugin vte291`

### Compile [WebKit2GTK+ Python WebExtension loader](https://github.com/aperezdc/webkit2gtk-python-webextension-example) and run Poseidon

`$ cd < POSEIDON ROOT DIR >/lib/src && make && mv pythonloader.so ../ && cd ../../`

`$ ./poseidon`

## Features

Actually, Poseidon have some features like:

* Media player (audio and video) (embedded in WebKit2).
* PDF reader (through Evince plugin).
* Import / Export bookmarks.
* Strong password generator.
* User agent switcher.
* VTE terminal.
* X509 decoder.
* Source viewer.
* Downloads manager.
* Custom themes.
* Video popout.
* Cookies manager (reader and editor).
* Protection from SSL insecure websites.
* AdKiller. Experimental Ads / Popups blocker.
* No-Script / No-Plugins. Useful to disable Javascript or Adobe Flash.
* Minimalist history and bookmarks tabs.
* Proxy manager (since Poseidon 0.5.5. Requires WebKit 2.16.x or higher)
* Incognito mode (aka. Defcon mode)
* HTTPS Redirect.

And much more...

## Shortcuts

In the main entry, type:

* about:plugins : to get a list of loaded plugins
* about:bookmarks : to open bookmarks tab
* about:history : to open history tab
* about:cookies : to open cookies manager tab
* about:settings : to open settings tab

## Available Languages

Actually, supported languages are 6:

* German (de_DE)
* English (en_US)
* Spanish (es_ES)
* French (fr_FR)
* Italian (it_IT)
* Polish (pl_PL)

## Themes

Any image can become a theme. Right click on any image and click "Apply as theme".

## Anonymity (Proxy)

In order to use Poseidon with a proxy, you can try:

### Torsocks or Proxychains

Once Tor is started through arm or the discontinued vidalia, you can launch Poseidon in these ways:

`$ torsocks(or proxychains) ./poseidon` (default mode)

`$ torsocks(or proxychains) ./poseidon -i` (defcon mode)

### Proxy Manager

If you installed WebKit 2.16.x and Poseidon 0.5.5 (or higher) then you might want to use `Proxy Manager`.
You can find it in the "Utilites" tab or just press its shortcut key "Ctrl+X".

### Other tips

To increase security even more, go to "Settings" > "Miles O'Brien", set "set-enable-java", "set-enable-javascript", "set-enable-plugins", "set-enable-webgl" to "False", save the new settings and re-launch Poseidon in Defcon Mode. It's also a good practice keeping your browser un-maximized during the navigation and set a custom user-agent ("set-user-agent").

## Make Poseidon as default browser

Install [xdg-utils](https://www.freedesktop.org/wiki/Software/xdg-utils/) then execute:

`$ xdg-settings set default-web-browser poseidon.desktop`

## Code snippets, examples, icons, inspirations, peace to:

* https://gist.github.com/kklimonda/890640 (pybrowser.py)
* https://github.com/kvesteri/validators (validators)
* https://github.com/aperezdc/webkit2gtk-python-webextension-example (WebKit2GTK+ Python WebExtension loader)
* https://www.gnome-look.org/p/1012545/ (Faenza)
* http://www.gnome.org (Adwaita)

## Contribution

You can help:

* Improving the source code
* Committing new translation files
* Reporting bugs

