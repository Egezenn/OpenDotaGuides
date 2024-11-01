#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <directory1> <directory2>"
    exit 1
fi

DIR1="$1"
DIR2="$2"
OUTPUT_FILE="comparison.diff"

> "$OUTPUT_FILE"

if [ ! -d "$DIR1" ]; then
    echo "Directory $DIR1 does not exist." >> "$OUTPUT_FILE"
    exit 1
fi

if [ ! -d "$DIR2" ]; then
    echo "Directory $DIR2 does not exist." >> "$OUTPUT_FILE"
    exit 1
fi

for file in "$DIR1"/*; do
    filename=$(basename "$file")
    echo $file
    echo $filename

    if [ -f "$DIR2/$filename" ]; then
        echo "Comparing $file with $DIR2/$filename..."
        diff_output=$(git diff "$file" "$DIR2/$filename")
        
        if [ -n "$diff_output" ]; then
            echo "$diff_output" >> "$OUTPUT_FILE"
        else
            echo "No differences found for $filename." >> "$OUTPUT_FILE"
        fi
    else
        echo "File $filename does not exist in $DIR2" >> "$OUTPUT_FILE"
    fi
done
