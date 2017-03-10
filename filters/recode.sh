#!/bin/bash

encoding=$(file -i "$2" | sed "s/.*charset=\(.*\)$/\1/")

if [ ! "$1" == "${encoding}" ]
then
echo "Recoding from ${encoding} to $1 file : $2"
recode ${encoding}..$1 $2
fi
