#!/bin/bash
for cat in topic person place source
do
python -m topic_collection.get_topic_list --category ${cat} &
done
wait