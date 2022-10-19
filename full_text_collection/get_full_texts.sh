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

# For collecting from the topic_list directly
TAG=1016
python -m full_text_collection.get_full_texts --source all --tag ${TAG}

# # For collecting single topic (e.g., the topic of gun-violence and mass-shooting)
# export TAG=1016 
# python -m full_text_collection.get_full_texts --source mass-shooting --tag ${TAG}
# python -m full_text_collection.get_full_texts --source gun-violence --tag ${TAG}
