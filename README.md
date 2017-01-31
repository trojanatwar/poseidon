# [Poseidon](https://sidus-dev.github.io/projects/poseidon/index.html)
A fast, minimal and lightweight browser

### Screenshot

![Alt text](http://m-net.arbornet.org/~sidus/images/gscreenshot_2016-09-09-150033.png "Poseidon on Arch Linux")

### Requirements

* Requires [WebKit](https://webkitgtk.org/) 2.12.3 or higher.

### Installation

* Arch Linux

`$ yaourt -S poseidon-browser-git`

* Ubuntu (tested on Yakkety Yak 16.10)

`# apt install python3-decorator python3-tk libwebkit2gtk-4.0-dev python3-dev python-gi-dev gir1.2-evince-3.0 browser-plugin-evince`
`$ cd < POSEIDON ROOT DIR >/lib/src && make && mv pythonloader.so ../ && cd ../../`
`$ ./poseidon`

* Fedora (tested on 25 Workstation)

`# dnf install python3 python3-devel webkitgtk4 webkitgtk4-devel webkitgtk4-jsc gtksourceview3 python3-tkinter python3-pillow python3-pyOpenSSL pygobject3 pygobject3-devel evince-browser-plugin`
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

### Donations

If you enjoy [Poseidon](https://github.com/sidus-dev/poseidon)
consider to buy me a beer!

`BTC: 1Ki95pCN6drymSUY7sS45MLVDkfiKTC8t9`
