#!/bin/bash

# usage: main.sh <starting rank> <ending rank>
START=$1
END=$2
for (( i=$START; i<$END; i++ ))
do
   python main.py --rank $i
done