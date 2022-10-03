from bs4 import BeautifulSoup

import requests
import json

url = "https://ground.news/my/discover/topic"
headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                         "KHTML, like Gecko) Version/4.0 Safari/534.30"}

html_text = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')

divs = soup.find_all('div', class_='flex flex-grow text-18 items-center justify-between')
topics = [div.find('span').text for div in divs]

with open('topic_list.json', 'w', encoding='utf-8') as f:
    json.dump(topics, f, indent=4)


# TODO: Get topics from related topics