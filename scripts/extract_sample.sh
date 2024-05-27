#!/bin/bash

directory="../data/tsx/"
new_file="../data/example_tsx.csv"

echo "hash;to_address;input;block_timestamp;receipt_gas_used" > "$new_file"

for file in "$directory"/*.csv; do 
    tail -n +2 "$file" | shuf -n 1000 >> "$new_file"
done