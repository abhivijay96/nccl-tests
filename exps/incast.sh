#!/bin/bash

n=$1 

for i in $(seq 2 $n); do # Loop from 1 to n
  echo $i # Print i
  ../build/gather_perf -b 96 -e 400M -f 2 -g $i > incast_$i.log
done