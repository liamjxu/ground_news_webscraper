#!/bin/bash
while :; do
    clear
    date
    python -m story_collection.stats --tag ${TAG}
    sleep 600
done