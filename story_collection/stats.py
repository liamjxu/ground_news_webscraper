import os
import json
from collections import Counter

threshold = 4
def qualify(articles, threshold=4):
    sufficient_quantity = len(articles) >= threshold
    bias = Counter([_['bias'] for _ in articles])
    sufficient_left = (bias['Lean Left'] + bias['Left'] >= threshold // 2)
    sufficient_right = (bias['Lean Right'] + bias['Right'] >= threshold // 2)
    sufficient_bias = sufficient_left and sufficient_right
    return sufficient_bias and sufficient_quantity


if __name__ == '__main__':
    topic_name = 'all'
    if topic_name == 'all':
        file_list = os.listdir('story_collection/interest/')
        data = {}
        for file in file_list:
            with open('story_collection/interest/' + file, 'r', encoding='utf-8') as f:
                data = data | json.load(f)

    else:
        with open('story_collection/interest/' + topic_name + '.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        file_list = [data]

    print('the number of topics:')
    print(len(file_list))

    print('the number of stories:')
    print(len(data))

    print('the number of article info:')
    print(sum([len(data[story]) for story in data]))

    print(f'the number of stories that have {threshold} or more articles '
          f'and have {threshold//2} or more on both sides: ', end='\n')
    print(sum([qualify(data[story]) for story in data]))

    print('the number of articles in these stories: ', end='\n')
    print(sum([len(data[story]) for story in data if qualify(data[story])]))

    print('the number of words (split by space) in the current article abstract: ', end='\n')
    print(sum([len(article['abstract'].split(' '))
               for story in data if qualify(data[story])
               for article in data[story]]))
