#!/bin/bash

# usage: main.sh <the desired number of processes>
START=$1
END=$2
for (( i=$START; i<$END; i++ ))
do
   python main.py --rank $i --num_proc 1
done