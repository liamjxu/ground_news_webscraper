#!/bin/bash

usage: main.sh <starting rank> <ending rank>
START=$1
END=$2
for (( i=$START; i<$END; i++ ))
do
   python get_full_texts.py --source all --rank $i &
done
wait