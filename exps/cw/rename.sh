#!/bin/bash

for file in *.log; do
  mv -- "$file" "${file%.log}.txt"
done
