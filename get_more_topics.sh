#!/bin/bash
# usage: watch.sh <your_command> <sleep_duration>

while :; 
  do 
  clear
  date
  sh get_topic_lists.sh && python compile_topic_list.py
  sleep 600
done