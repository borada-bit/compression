#!/bin/bash

files=("text.txt") # "bigfile.txt" "alice29.txt" "beer.jpg" "pineapple.jpg") 

for file in "${files[@]}"
do
  for i in {2..16}
  do
    python huffman.py -c "$file" $i >/dev/null
    python huffman.py -d "$file" >/dev/null
    if ! cmp -s "$file" output; then
        echo "Compression and decompression with bit length $i failed on $file"
    fi
  done
done
