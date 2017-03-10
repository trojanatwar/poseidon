#!/bin/bash

rm *.txt

url(){

    file="$RANDOM.txt"

	if [ ! -z "$1" ]; then
		wget -q --no-check-certificate "$1" -O "$file"
		[ "$?" -eq 0 ] && echo "$1 downloading..." || echo "$1 doesn't exists."
	else
		echo "No args, exiting" & exit
	fi
        ./recode.sh utf-8 "$file"
        echo "Done."

}

#####################################
# Add your AdAway filters URLS here #
#####################################

url "https://adaway.org/hosts.txt"
url "http://winhelp2002.mvps.org/hosts.txt"
url "http://hosts-file.net/ad_servers.txt"
url "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext"

