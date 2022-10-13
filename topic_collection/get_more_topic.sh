#!/bin/bash
while :; 
  do 
  clear
  date
  sh topic_collection/get_topic_list.sh && python -m topic_collection.compile_topic_list
  sleep 600
done