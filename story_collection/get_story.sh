#!/bin/bash

# usage: main.sh <starting rank> <ending rank>
# START=$1
# END=$2
# for (( i=$START; i<$END; i++ ))
# do
#    python -m story_collection.main --rank $i &
# done
# wait
TAG=1016
python -m story_collection.main --source topic_list --tag ${TAG} --headless