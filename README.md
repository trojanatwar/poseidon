# Poseidon
A fast, minimal and lightweight browser

### Screenshot

![Alt text](http://arbornet.org/~sidus/images/gscreenshot_2017-03-27-154512.png "Poseidon on Arch Linux")

### Requirements

Requires [WebKit](https://webkitgtk.org/) 2.12.3 or higher.

### Installation

**Arch Linux**

`$ yaourt -Sy poseidon-browser-git`

**Debian, Mint, Ubuntu**

[Download & install .deb packages](https://github.com/sidus-dev/poseidon/releases)

* Optional dependencies

`# apt install gir1.2-evince-3.0 browser-plugin-evince`

**Fedora (tested on 25 Workstation)**

* Required dependencies

`# dnf install python3 webkitgtk4 webkitgtk4-jsc gtksourceview3 python3-pillow python3-pyOpenSSL pygobject3`

* Development dependencies

`# dnf install python3-devel webkitgtk4-devel pygobject3-devel`

* Optional dependencies

`# dnf install evince-browser-plugin vte3`

### Compile [WebKit2GTK+ Python WebExtension loader](https://github.com/aperezdc/webkit2gtk-python-webextension-example) and run Poseidon

`$ cd < POSEIDON ROOT DIR >/lib/src && make && mv pythonloader.so ../ && cd ../../`

`$ ./poseidon`

### Features

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

### Shortcuts

In the main entry, type:

* about:plugins : to get a list of loaded plugins
* about:bookmarks : to open bookmarks tab
* about:history : to open history tab
* about:cookies : to open cookies manager tab
* about:settings : to open settings tab

### Available Languages

Actually, supported languages are 4:

* English (en_US)
* German (de_DE)
* Italian (it_IT)
* Spanish (es_ES)

### Themes

Any image can become a theme. Right click on any image and click "Apply as theme".

### Anonymity

* Tor

In order to use Poseidon with Tor, you need torsocks or alternatively proxychains. Once Tor is started through arm or the discontinued vidalia, you can launch Poseidon in these ways:

`$ torsocks(or proxychains) ./poseidon` (default mode)

`$ torsocks(or proxychains) ./poseidon -i` (defcon mode)

To increase security even more, go to "Settings" > "Miles O'Brien", set "set-enable-java", "set-enable-javascript", "set-enable-plugins", "set-enable-webgl" to "False", save the new settings and re-launch Poseidon in Defcon Mode. It's also a good practice keeping your browser un-maximized during the navigation and set a custom user-agent ("set-user-agent").

### Code snippets, examples, icons, inspirations, peace to:

* https://gist.github.com/kklimonda/890640 (pybrowser.py)
* https://github.com/kvesteri/validators (validators)
* https://github.com/aperezdc/webkit2gtk-python-webextension-example (WebKit2GTK+ Python WebExtension loader)
* https://www.gnome-look.org/p/1012545/ (Faenza)
* http://www.gnome.org (Adwaita)

### Contribution

You can help:

* Improving the source code
* Committing new translation files
* Reporting bugs
* Buying me a beer! `BTC: 1Ki95pCN6drymSUY7sS45MLVDkfiKTC8t9`

