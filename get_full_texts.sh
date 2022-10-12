#!/bin/bash
# usage: main.sh <starting rank> <ending rank>
# using 0-8 because my CPU has 8 cores

START=0
END=8
for (( i=$START; i<$END; i++ ))
do
   python get_full_texts.py --source all --rank $i &
done
wait