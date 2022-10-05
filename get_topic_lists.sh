#!/bin/bash
for cat in topic person place source
do
python get_topic_list.py --category ${cat} &
done
wait