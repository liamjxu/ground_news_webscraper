import json
import time
import requests
from collections import Counter, OrderedDict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm


def collect_from_one_news_source(source):
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

    root_url = root_urls[source]
    main_content_class = main_content_classes[source]

    with open('../urls.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    url_sublist = [_ for _ in urls.keys() if _.startswith(root_url)]

    print(len(url_sublist))
    
    logs = []
    tic = time.time()
    for idx, url in enumerate(url_sublist):
        try:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'lxml')
            # for theguardian
            title = soup.find('h1').text
            if source == 'msn':
                ps = [title.strip()] + [_.text.strip() for _ in soup.find_all('p', class_='')]
            else:
                main_content = soup.find('div', class_=main_content_class)
                ps = [title.strip()] + [_.text.strip() for _ in main_content.find_all('p')]
            with open(f'{source}/{idx}.txt', 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(ps))
            toc = time.time()
            logs.append({
                'idx': idx,
                'status': 'Sucessful',
                'URL': url,
                'time': toc-tic
            })
        except BaseException as e:
            toc = time.time()
            logs.append({
                'idx': idx,
                'status': 'Failed',
                'URL': url,
                'time': toc-tic,
                'error message': str(e)
            })
    with open(f'{source}/logs.json', 'w', encoding='utf-8') as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    # collect_from_one_news_source('theguardian')
    # collect_from_one_news_source('reuters')
    # collect_from_one_news_source('cnn')
    collect_from_one_news_source('msn')