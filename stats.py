import os
import json
from collections import Counter

threshold = 2
def qualify(articles):
    sufficient_quantity = len(articles) >= threshold
    bias = Counter([_['bias'] for _ in articles])
    sufficient_bias = (bias['Lean Left'] + bias['Left'] >= threshold//2) and (bias['Lean Right'] + bias['Right'] >= threshold//2)
    return sufficient_bias and sufficient_quantity


file_list = os.listdir('interest/')
data = {}
for file in file_list:
    with open('interest/' + file, 'r', encoding='utf-8') as f:
        data = data | json.load(f)

print(f'the number of stories that have {threshold} or more articles and have {threshold//2} or more on both sides: ', end='')
print(sum([qualify(data[story]) for story in data]))

print('the number of articles in these stories: ', end='')
print(sum([len(data[story]) for story in data if qualify(data[story])]))

print('the number of words (split by space) in the current article : ', end='')
print(sum([len(article['abstract'].split(' ')) for story in data if qualify(data[story]) for article in data[story]]))