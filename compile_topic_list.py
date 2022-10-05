import os
import json
from functools import reduce
from collections import OrderedDict

file_list = [file for file in os.listdir('.') if file.endswith('.json') and file.startswith('topic_list_')]
print(file_list)
d = []
for file in file_list:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    d.append(data)

all_d = reduce(lambda a, b: a | b, d)
with open('topic_list.json', 'r', encoding='utf-8') as f:
    topic_list = json.load(f)

pre_len = len(topic_list)
topic_list |= all_d
post_len = len(topic_list)

with open('topic_list_orig.json', 'w', encoding='utf-8') as f:
    json.dump(topic_list, f, indent=4, ensure_ascii=False)

with open('topic_list.json', 'w', encoding='utf-8') as f:
    json.dump(OrderedDict(sorted(topic_list.items())), f, indent=4, ensure_ascii=False)

print(f'One compilation finished, {post_len - pre_len} more topics are found, currently have {post_len} in total.')
