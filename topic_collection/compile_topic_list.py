import os
import json
import argparse
from functools import reduce
from collections import OrderedDict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', type=str, default='latest',
                        help='the tag to use for data version labeling')
    args = parser.parse_args()

    file_list = [file for file in os.listdir('topic_collection/')
                 if file.endswith('.json') and file.startswith(f'{args.tag}_topic_list_')]
    print(file_list)
    d = []
    for file in file_list:
        with open(f'topic_collection/{file}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        d.append(data)

    all_d = reduce(lambda a, b: a | b, d)
    if os.path.exists(f'topic_collection/{args.tag}_topic_list.json'):
        with open(f'topic_collection/{args.tag}_topic_list.json', 'r', encoding='utf-8') as f:
            topic_list = json.load(f)
    else:
        topic_list = {}

    pre_len = len(topic_list)
    topic_list |= all_d
    post_len = len(topic_list)

    with open(f'topic_collection/{args.tag}_topic_list.json', 'w', encoding='utf-8') as f:
        json.dump(OrderedDict(sorted(topic_list.items())), f, indent=4, ensure_ascii=False)

    print(f'One compilation finished, {post_len - pre_len} more topics are found, currently have {post_len} in total.')
    print(f'Saved to topic_collection/{args.tag}_topic_list.json')
