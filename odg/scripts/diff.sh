#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory1> <directory2>"
    exit 1
fi

DIR1="$1"
DIR2="$2"
OUTPUT_FILE="comparison.diff"

> "$OUTPUT_FILE"

if [ ! -d "$DIR1" ]; then
    echo -e "Directory $DIR1 does not exist.\n" >> "$OUTPUT_FILE"
    exit 1
fi

if [ ! -d "$DIR2" ]; then
    echo -e "Directory $DIR2 does not exist.\n" >> "$OUTPUT_FILE"
    exit 1
fi

for file in "$DIR1"/*; do
    filename=$(basename "$file")

    if [ -f "$DIR2/$filename" ]; then
        hero_name="${filename:8:${#filename}-12}"
        # ignore title changes with grep
        diff_output=$(diff -C 10 <(grep -v "Title" "$file") <(grep -v "Title" "$DIR2/$filename"))
        
        if [ -n "$diff_output" ]; then
            echo -e "Differences found for ===$hero_name===\n$diff_output\n" >> "$OUTPUT_FILE"
        else
            echo -e "No differences found for ==="$hero_name"===\n" >> "$OUTPUT_FILE"
        fi
    else
        echo -e "File $filename does not exist in $DIR2\n" >> "$OUTPUT_FILE"
    fi
done
