# [Poseidon](https://sidus-dev.github.io/projects/poseidon/index.html)
A fast, minimal and lightweight browser

### Screenshot

![Alt text](https://sidus-dev.github.io/projects/poseidon/images/gscreenshot_2017-01-30-114314.png "Poseidon on Arch Linux")

### Requirements

Requires [WebKit](https://webkitgtk.org/) 2.12.3 or higher.

### Installation

**Arch Linux**

`$ yaourt -Sy poseidon-browser-git`

**Debian (tested on Stretch)**

* Required dependencies

`# apt install gir1.2-webkit2-4.0 gir1.2-gtksource-3.0 python3-decorator python3-requests python3-pil python3-openssl python3-gi-cairo`

* Development dependencies

`# apt install libwebkit2gtk-4.0-dev python-gi-dev`

* Optional dependencies

`# apt install gir1.2-evince-3.0 browser-plugin-evince gir1.2-vte-2.91`

**Mint (tested on Serena)**

[Deb Package (0.4.9 - amd64)](https://sidus-dev.github.io/projects/poseidon/downloads/poseidon_0.4.9-1_amd64.deb)

For evince support install `evince-browser-plugin` package from [Ubuntu Packages](http://packages.ubuntu.com/zesty/browser-plugin-evince)

**Ubuntu (tested on Yakkety Yak 16.10)**

* Required dependencies

`# apt install python3-decorator`

* Development dependencies

`# apt install libwebkit2gtk-4.0-dev python3-dev python-gi-dev`

* Optional dependencies

`# apt install gir1.2-evince-3.0 browser-plugin-evince gir1.2-vte-2.91`

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

### Other

For more informations, click [here](https://sidus-dev.github.io/projects/poseidon/index.html).

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

