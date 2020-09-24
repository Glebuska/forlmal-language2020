#!/bin/bash

LOC="/home/gleb/Documents/formal-language2020/tests/data/refinedDataForRPQ/"

DATA=(LUBM1M LUBM1.5M)

for set in ${DATA[*]}
do
graph="$LOC/$set/$set.txt"
folder="$LOC/$set/regexes/*"
output="benchmark_${set}_result.txt"
export PYTHONPATH="${PYTHONPATH}:./"
for regex in $folder
do
python3 main.py --graph_path $graph --regex_path $regex >> $output
done
done
