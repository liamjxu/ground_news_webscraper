import time
import pathlib
import json
import argparse
from newsplease import NewsPlease


def main(args):
    if args.source != 'all':
        tic = time.time()
        get_news_for_topic(args.source)
        toc = time.time()
        print(f'The topic {args.source} took {toc - tic} seconds')

    else:
        bad_topics = []
        pathlib.Path(f'full_text_collection/{args.tag}_bad_topics.json').unlink(missing_ok=True)
        with open(f'topic_collection/{args.tag}_topic_list.json', 'r', encoding='utf-8') as f:
            topic_list = [_[10:] for _ in json.load(f).values()]  # the 10 here corresponds to "/interest/"
        for topic in topic_list:
            try:
                get_news_for_topic(topic)
            except BaseException as e:
                bad_topics.append({
                    'topic': topic,
                    'error_message': str(e)
                })
                with open(f'full_text_collection/{args.tag}_bad_topics.json', 'w', encoding='utf-8') as f:
                    json.dump(bad_topics, f, indent=4, ensure_ascii=False)


def get_news_for_topic(topic):
    with open(f'story_collection/{args.tag}_interest/{topic}.json', 'r', encoding='utf-8') as f:
        stories = json.load(f)
    # if the loading succeeded, make directory
    pathlib.Path(f'{args.tag}_news/{topic}').mkdir(parents=True, exist_ok=True)
    logs = {'Topic Progress': f'-1 / {len(stories)}'}
    with open(f'{args.tag}_news/{topic}/0-logs.json', 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

    tic = time.time()
    for story_idx, (story, all_metadata) in enumerate(stories.items()):
        if story == 'stats':
            continue
        story_log = []
        all_article = []
        for article_idx, metadata in enumerate(all_metadata):
            try:
                # get article and process
                article = NewsPlease.from_url(metadata['source_link'], timeout=6)
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
                with open(f'{args.tag}_news/{topic}/{story}.json', 'w', encoding='utf-8') as f:
                    json.dump(all_article, f, indent=4, ensure_ascii=False)

                # store the successful story_log
                story_log.append({
                    'article_idx': metadata['index'],
                    'status': 'Successful',
                })
                logs[story] = story_log
                toc = time.time()
                logs['Topic Progress'] = f'{story_idx + 1} / {len(stories)}, time elapsed: {toc - tic: .2f}'
                with open(f'{args.tag}_news/{topic}/0-logs.json', 'w', encoding='utf-8') as f:
                    json.dump(logs, f, indent=4, ensure_ascii=False)

            except BaseException as e:
                # store the failed story_log
                story_log.append({
                    'article_idx': metadata['index'],
                    'status': 'Failed',
                    'error_message': str(e)
                })
                logs[story] = story_log
                logs['Topic Progress'] = f'{story_idx + 1} / {len(stories)}, time elapsed: {toc - tic: .2f}'
                with open(f'{args.tag}_news/{topic}/0-logs.json', 'w', encoding='utf-8') as f:
                    json.dump(logs, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='gun-control',
                        help='the source topic, being "all" means collecting all topics')
    parser.add_argument('--tag', type=str, default='latest',
                        help='the tag to use for data version labeling')
    args = parser.parse_args()
    main(args)
