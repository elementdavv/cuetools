#!/bin/bash

# desc:
#	delete last part of filename, keeping extension
# usage:
#	run in the directory with files to rename
#	dellast.sh string fileext
#	for example, to find blank character and delete it till end of all files with extension flac:
#	dellast.sh " " .flac

lastchr()
{
    return "$(echo "$1" | awk -F "$2" '{printf "%d", length($0)-length($NF)}')"
}

if [ $# -ne 2 ]; then
  exit 1
fi

for file in *"$2"
do
    lastchr "$file" "$1"
    a=$(echo "$file" | cut -c1-$(($?-1)))
    c="$a$2"
    mv "$file" "$c"
done
