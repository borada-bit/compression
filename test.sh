#!/bin/bash

files=("text.txt") 

for file in "${files[@]}"
do
  for i in {2..16}
  do
    python huffman.py -c "$file" $i >/dev/null
    python huffman.py -d "$file".huf >/dev/null
    if ! cmp -s "$file" output; then
        echo "Compression and decompression with bit length $i failed on $file"
    fi
  done
done
