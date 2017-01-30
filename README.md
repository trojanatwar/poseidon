# [Poseidon](https://sidus-dev.github.io/projects/poseidon/index.html)
A fast, minimal and lightweight browser

### Screenshot

![Alt text](http://m-net.arbornet.org/~sidus/images/gscreenshot_2016-09-09-150033.png "Poseidon on Arch Linux")

### Requirements

* Requires [WebKit](https://webkitgtk.org/) 2.12.3 or higher

### Dependencies

* Arch Linux

`# pacman -S python3 python-gobject python-decorator python-six python-requests python-pillow python-cairo pyopenssl gtk3 gtksourceview3 webkit2gtk`

Optionally:

```
gst-libav: HTML5 H264 videos support
gst-plugins-base: HTML5 OGG videos support
gst-plugins-good: HTML5 H264 and WebM videos support
evince: Embed PDFs support
vte3: Embed terminal support
flashplugin: Adobe Flash Player
icedtea-web: Free web browser plugin to run applets written in Java and an implementation of Java Web Start
```

Full command:

`# pacman -S gst-libav gst-plugins-base gst-plugins-good evince vte3 flashplugin icedtea-web`

* Ubuntu/Mint

`# apt-get install gir1.2-evince-3.0 gir1.2-webkit2-4.0 python3-decorator python3-openssl python3-tk libgtksourceview-3.0-dev`

Optional: [evince-browser-plugin](http://packages.ubuntu.com/en/yakkety/browser-plugin-evince)

If your WebKit version is too old, upgrade it from [here](https://launchpad.net/~webkit-team/+archive/ubuntu/ppa):

`# add-apt-repository ppa:webkit-team/ppa && apt-get update && apt-get upgrade`

* Fedora

`# dnf install python3-pyOpenSSL.noarch`

* FreeBSD (10.3*)

`# pkg install python3 py34-gobject3 py34-sqlite3 py34-pillow gtksourceview3`

then (ignore the first two lines if you already have pip3 installed):

```
python3.4 -m ensurepip
pip3.4 install --upgrade pip
pip3 install six decorator pyopenssl
rehash
```

[Compile](https://trac.webkit.org/wiki/BuildingGtk) [WebKitGTK](https://webkit.org/getting-the-code/) manually if the one provided by the ports is obsolete, viceversa:

`# pkg install webkit2-gtk3`

### Other

For more info, click [here](https://sidus-dev.github.io/projects/poseidon/index.html)

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
