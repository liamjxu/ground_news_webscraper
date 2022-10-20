#!/bin/bash

# For collecting from the topic_list directly
python -m story_collection.main --source topic_list --tag ${TAG} --headless

# # For collecting known topics (e.g., gun-violence and mass-shooting)
# python -m story_collection.main --source href --href /interest/gun-violence --tag ${TAG} --headless
# python -m story_collection.main --source href --href /interest/mass-shooting --tag ${TAG} --headless
