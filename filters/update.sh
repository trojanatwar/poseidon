#!/bin/bash

rm *.txt

url(){
	if [ ! -z "$1" ]; then
		wget -q --no-check-certificate "$1" -O "$RANDOM.txt"
		[ "$?" -eq 0 ] && echo "$1 downloading..." || echo "$1 doesn't exists."
	else
		echo "No args, exiting" & exit
	fi
       for file in *.txt; do
           iconv -t UTF-8 $file -o $file
        done
        echo "Done."
}

################################
# Add your AdAway filters here #
################################

url "https://adaway.org/hosts.txt"
url "http://winhelp2002.mvps.org/hosts.txt"
url "http://hosts-file.net/ad_servers.txt"
url "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext"

