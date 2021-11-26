#!/bin/bash

# desc:
#	add a string at any position in files with a extension
# usage:
#	run in the directory with files to rename
#	addstring.sh index string fileext
#	for example, to add a dot after position 2 to all files with extension flac:
#	addstring.sh 2 . .flac

if [ $# -ne 3 ]; then
  exit 1
fi

for file in *"$3"
do
  a=$(echo "$file" | cut -c1-"$1")
  (( n=$1+1 ))
  b=$(echo "$file" | cut -c$n-)
  c="$a$2$b"
  mv "$file" "$c"
done
