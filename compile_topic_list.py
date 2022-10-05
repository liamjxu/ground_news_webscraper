import os
import json
from functools import reduce

file_list = [file for file in os.listdir('.') if file.endswith('.json') and file.startswith('topic_list_')]
print(file_list)
d = []
for file in file_list:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    d.append(data)

all_d = reduce(lambda a, b: a | b, d)
print(len(all_d))
with open('topic_list.json', 'w', encoding='utf-8') as f:
    json.dump(all_d, f, indent=4, ensure_ascii=False)