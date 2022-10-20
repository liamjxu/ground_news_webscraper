#!/bin/bash
while :; 
    do 
    clear
    date

    # get topic_list
    for cat in topic person place source
    do
    python -m topic_collection.get_topic_list --category ${cat} --tag ${TAG} &
    done
    wait
    
    # compile
    python -m topic_collection.compile_topic_list --tag ${TAG}
    
    sleep 600
done