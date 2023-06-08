#!/bin/bash

n=$1
list=()
for ((i=0;i<=n;i++))
do
  list+=($i)
done

for i in "${list[@]}"
do
  for j in "${list[@]}"
  do
    if [ "$i" -ne "$j" ]
    then
      echo "[PAIR]: $i $j"
      ../build/latency_perf -b 4 -e 4 -i 1 -g 2 -L $i -R $j -a 1
    fi
  done
done
