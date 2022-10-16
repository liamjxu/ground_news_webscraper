#!/bin/bash
# usage: main.sh <starting rank> <ending rank>
# using 0-8 because my CPU has 8 cores

# START=0
# END=8
# for (( i=$START; i<$END; i++ ))
# do
#    python -m full_text_collection.get_full_texts --source all --rank $i &
# done
# wait

TAG=1016
python -m full_text_collection.get_full_texts --source all --tag ${TAG}
