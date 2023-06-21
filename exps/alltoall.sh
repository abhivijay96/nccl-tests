#!/bin/bash

export NCCL_DEBUG=TRACE
export NCCL_DEBUG_SUBSYS=ALL

n=$1 

for i in $(seq 2 $n); do # Loop from 1 to n
  echo $i # Print i
  ../build/alltoall_perf -b 96 -e 4096M -f 2 -g 1 -t $i > alltoall_$i.log
done