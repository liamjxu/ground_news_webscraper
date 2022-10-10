import os
import json
import time
import requests
from collections import Counter, OrderedDict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
from stats import qualify


root_urls = {
    'theguardian': 'https://www.theguardian.com/',
    'reuters': 'https://www.reuters.com/',
    'cnn': 'https://www.cnn.com/',
    'msn': 'http://www.msn.com'
}

main_content_classes = {
    'theguardian': 'article-body-commercial-selector',
    'reuters': 'paywall-article',
    'cnn': 'article__content',
    'msn': None  # not using main content
}


def collect_from_one_news_source(source, urls, result_dir='news'):
    if not os.path.exists(f'{result_dir}/{source}/'):
        os.makedirs(f'{result_dir}/{source}/')
    root_url = root_urls[source]
    main_content_class = main_content_classes[source]
    url_sublist = [_ for _ in urls if _.startswith(root_url)]
    print(len(url_sublist))

    logs = []
    tic = time.time()
    for idx, url in enumerate(url_sublist):
        try:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')
            title = soup.find('h1').text
            if source == 'msn':
                ps = [title.strip()] + [_.text.strip() for _ in soup.find_all('p', class_='')]
            else:
                main_content = soup.find('div', class_=main_content_class)
                ps = [title.strip()] + [_.text.strip() for _ in main_content.find_all('p')]
            with open(f'{result_dir}/{source}/{idx}.txt', 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(ps))
            toc = time.time()
            logs.append({
                'idx': idx,
                'status': 'Sucessful',
                'URL': url,
                'time': toc - tic
            })
        except BaseException as e:
            toc = time.time()
            logs.append({
                'idx': idx,
                'status': 'Failed',
                'URL': url,
                'time': toc - tic,
                'error message': str(e)
            })
    with open(f'{result_dir}/{source}/logs.json', 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    with open('interest/gun-control.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    hq_urls = [y['source link'] for x in urls.keys() for y in urls[x] if qualify(urls[x])]
    # collect_from_one_news_source('theguardian', urls)
    # collect_from_one_news_source('reuters', urls)
    collect_from_one_news_source('cnn', hq_urls)
    # collect_from_one_news_source('msn', hq_urls)
