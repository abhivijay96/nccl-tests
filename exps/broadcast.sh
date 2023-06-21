#!/bin/bash

n=$1 

for i in $(seq 2 2 $n); do # Loop from 1 to n
  echo $i # Print i
  ../build/sendrecv_perf -b 96 -e 4096M -f 2 -g $i > sendrecv_$i.log
done