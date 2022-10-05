#!/bin/bash

# usage: main.sh <the desired number of processes>
START=0
END=$1-1
for (( i=$START; i<=$END; i++ ))
do
   python main.py --rank $i --num_proc $1 &
done