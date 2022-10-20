#!/bin/bash
while :; do
    clear
    date
    python -m full_text_collection.full_text_stats --tag ${TAG}
    sleep 600
done