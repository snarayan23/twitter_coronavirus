#!/bin/sh

for file in /data/Twitter\ dataset/geoTwitter20-*; do
    nohup ./src/map.py "--input_path=$file" > outputcheck/$(basename "$file"| cut -f 1 -d '.') &
    #echo $file
done 
