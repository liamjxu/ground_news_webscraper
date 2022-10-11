import pathlib
import json
from tqdm import tqdm
from stats import qualify
from newsplease import NewsPlease


def get_news_for_topic(topic):
    pathlib.Path(f'news/{topic}').mkdir(parents=True, exist_ok=True)
    with open(f'interest/{topic}.json', 'r', encoding='utf-8') as f:
        stories = json.load(f)
    bad_cases = []
    for idx, (story, all_metadata) in enumerate(stories.items()):
        if idx % 5 == 0:
            print('idx: ', idx)
        if not qualify(all_metadata):
            continue
        all_article = []
        for metadata in tqdm(all_metadata):
            try:
                article = NewsPlease.from_url(metadata['source link'])
                article.__setattr__('bias', metadata['bias'])
                article.__setattr__('factuality', metadata['factuality'])
                article.__setattr__('name', metadata['name'])
                if article.date_publish is not None:
                    article.__setattr__('date_publish', article.date_publish.strftime('%m/%d/%Y'))
                else:
                    article.__setattr__('date_publish', None)
                all_article.append({
                    key: article.__getattribute__(key) for key in [
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
                with open(f'news/{topic}/{story}.json', 'w', encoding='utf-8') as f:
                    json.dump(all_article, f, indent=4, ensure_ascii=False)
            except BaseException as e:
                bad_cases.append({
                    'story': story,
                    'idx': metadata['index'],
                    'error_message': str(e)
                })
                with open(f'news/{topic}/bad_cases.json', 'w', encoding='utf-8') as f:
                    json.dump(bad_cases, f, indent=4, ensure_ascii=False)




if __name__ == '__main__':
    get_news_for_topic('gun-control')
