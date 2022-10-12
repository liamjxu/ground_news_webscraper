import time
import pathlib
import json
import argparse
# from tqdm import tqdm
from stats import qualify
from newsplease import NewsPlease


def get_news_for_topic(topic):
    with open(f'interest/{topic}.json', 'r', encoding='utf-8') as f:
        stories = json.load(f)
    # if the loading succeeded, make directory
    pathlib.Path(f'news/{topic}').mkdir(parents=True, exist_ok=True)
    logs = {'Topic Progress': f'-1 / {len(stories)}'}
    with open(f'news/{topic}/0-logs.json', 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)
    for story_idx, (story, all_metadata) in enumerate(stories.items()):
        story_log = []
        if not qualify(all_metadata):
            continue
        all_article = []
        for article_idx, metadata in enumerate(all_metadata):
            # print(f'current article: {article_idx} / {len(all_metadata)}')
            try:
                # get article and process
                article = NewsPlease.from_url(metadata['source link'], timeout=6)
                article.__setattr__('article_idx', metadata['index'])
                article.__setattr__('bias', metadata['bias'])
                article.__setattr__('factuality', metadata['factuality'])
                article.__setattr__('name', metadata['name'])
                if article.date_publish is not None:
                    article.__setattr__('date_publish', article.date_publish.strftime('%m/%d/%Y'))
                else:
                    article.__setattr__('date_publish', None)

                # store the collected full text
                all_article.append({
                    key: article.__getattribute__(key) for key in [
                        'article_idx',
                        'bias',
                        'factuality',
                        'name',
                        'date_publish',
                        'image_url',
                        'language',
                        'url',
                        'source_domain',
                        'title',
                        'authors',
                        'maintext'
                    ]
                })
                # store the data, update the logs
                with open(f'news/{topic}/{story}.json', 'w', encoding='utf-8') as f:
                    json.dump(all_article, f, indent=4, ensure_ascii=False)

                # store the successful story_log
                story_log.append({
                    'article_idx': metadata['index'],
                    'status': 'Successful',
                })
                logs[story] = story_log
                logs['Topic Progress'] = f'{story_idx} / {len(stories)}'
                with open(f'news/{topic}/0-logs.json', 'w', encoding='utf-8') as f:
                    json.dump(logs, f, indent=4, ensure_ascii=False)

            except BaseException as e:
                # store the failed story_log
                story_log.append({
                    'article_idx': metadata['index'],
                    'status': 'Failed',
                    'error_message': str(e)
                })
                logs[story] = story_log
                logs['Topic Progress'] = f'{story_idx} / {len(stories)}'
                with open(f'news/{topic}/0-logs.json', 'w', encoding='utf-8') as f:
                    json.dump(logs, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    RANK_WIDTH = 10  # 5 topics, usually takes ~8 hours
    parser = argparse.ArgumentParser()
    parser.add_argument('--rank', type=int, default=1,
                        help='the local rank of the current process')
    parser.add_argument('--source', type=str, default='gun-control',
                        help='the source topic, being "all" means collecting all topics')
    args = parser.parse_args()

    if args.source != 'all':
        tic = time.time()
        get_news_for_topic(args.source)
        toc = time.time()
        print(f'The topic {args.source} took {toc - tic} seconds')

    else:
        bad_topics = []
        with open('topic_list.json', 'r', encoding='utf-8') as f:
            topic_list = [_[10:] for _ in json.load(f).values()]
        for topic in topic_list[args.rank * RANK_WIDTH: (args.rank + 1) * RANK_WIDTH]:
            print('current rank:', args.rank, 'current topic:', topic)
            try:
                tic = time.time()
                get_news_for_topic(topic)
                toc = time.time()
                print(f'Rank {args.rank} ({args.rank * RANK_WIDTH} to {(args.rank + 1) * RANK_WIDTH}) took {toc - tic} seconds')
            except BaseException as e:
                bad_topics.append({
                    'topic': topic,
                    'error_message': str(e)
                })
                with open('bad_topics.json', 'w', encoding='utf-8') as f:
                    json.dump(bad_topics, f, indent=4, ensure_ascii=False)
