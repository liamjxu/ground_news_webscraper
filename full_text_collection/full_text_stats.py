import json
import os
import argparse
from tqdm import tqdm

def main(args):
    # some topics don't contain stories
    all_topic = []
    for topic in os.listdir(f'{args.tag}_news'):
        if len(list(os.listdir(f'{args.tag}_news/' + topic))) > 1:
            all_topic.append(topic)
    print(f'The number of collected topics: {len(all_topic)}')

    # the number of stories
    all_story = []
    for topic in os.listdir(f'{args.tag}_news'):
        for story in os.listdir(f'{args.tag}_news/{topic}')[1:]:  # get rid of the 0-logs.json file
            all_story.append(f'{args.tag}_news/{topic}/{story}')
    print(f'The number of collected stories: {len(all_story)}')

    # the number of articles
    all_article = []
    for story in tqdm(all_story):
        with open(story, 'r', encoding='utf-8') as f:
            article = json.load(f)
            all_article += article
    print(f'The number of collected articles: {len(all_article)}')

    # the number of unique articles
    urls = [_['url'] for _ in all_article]
    print(f'The number of unique urls: {len(list(set(urls)))}')

    # the number of words
    counted_url = []
    word_cnt = 0
    url_cnt = 0
    for article in tqdm(all_article):
        if article['url'] in counted_url:
            continue
        else:
            url_cnt += 1
            counted_url.append(article['url'])
            if article['maintext'] is None:
                continue
            word_cnt += len(article['maintext'].replace('\n', ' ').split(' '))
    print(f'The number of words in the unique articles is {word_cnt}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--tag', type=str, default='latest',
                        help='the tag to use for data version labeling')
    args = parser.parse_args()
    main(args)
