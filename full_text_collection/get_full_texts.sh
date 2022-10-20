#!/bin/bash

# For collecting from the topic_list directly
python -m full_text_collection.get_full_texts --source all --tag ${TAG}

# # For collecting single topic (e.g., the topic of gun-violence and mass-shooting)
# export TAG=1016 
# python -m full_text_collection.get_full_texts --source mass-shooting --tag ${TAG}
# python -m full_text_collection.get_full_texts --source gun-violence --tag ${TAG}
