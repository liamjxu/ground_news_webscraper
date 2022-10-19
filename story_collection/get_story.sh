#!/bin/bash

# usage: main.sh <starting rank> <ending rank>
# START=$1
# END=$2
# for (( i=$START; i<$END; i++ ))
# do
#    python -m story_collection.main --rank $i &
# done
# wait

# For collecting from the topic_list directly
TAG=1016
python -m story_collection.main --source topic_list --tag ${TAG} --headless

# # For collecting with known topic (e.g., gun-violence and mass-shooting)
# export TAG=1016
# python -m story_collection.main --source href --href /interest/gun-violence --tag ${TAG} --headless
# python -m story_collection.main --source href --href /interest/mass-shooting --tag ${TAG} --headless
