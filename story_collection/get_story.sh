#!/bin/bash

# usage: main.sh <starting rank> <ending rank>
# START=$1
# END=$2
# for (( i=$START; i<$END; i++ ))
# do
#    python -m story_collection.main --rank $i &
# done
# wait

python -m story_collection.main --source topic_list --tag 1016 --headless