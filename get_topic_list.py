import json
import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from functools import reduce

class Topic():
    def __init__(self, topic_name, topic_href):
        self.name = topic_name
        self.href = topic_href

    def get_dict(self):
        return {self.name: self.href}

    def get_tuple(self):
        return self.name, self.href

    @classmethod
    def create_list(cls, names, hrefs):
        return [cls(name, href) for name, href in zip(names, hrefs)]


def main():
    url = "https://ground.news/my/discover/topic"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                             "KHTML, like Gecko) Version/4.0 Safari/534.30"}

    # Get seed topics from the topic page
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    divs = soup.find_all('div', class_='flex flex-grow text-18 items-center justify-between')
    seed_topics = [div.find('span').text for div in divs]

    # BFS on the topics
    topic_list = {}
    queue = [Topic(topic_name, name2href(topic_name)) for topic_name in seed_topics]
    while len(queue): 
        if queue[0].name in topic_list:
            queue = queue[1:]
            continue
        else:
            topic_list |= queue[0].get_dict()
            queue = queue[1:] + get_related_topics(queue[0])
            if (len(topic_list) + 1) % 10 == 0:
                with open('topic_list.json', 'w', encoding='utf-8') as f:
                    json.dump(topic_list, f, indent=4)
            with open('topic_list.json', 'w', encoding='utf-8') as f:
                json.dump(topic_list, f, indent=4)
        if len(topic_list) >= 500:
            break
        if (len(topic_list) + 1) % 10 == 0:
            print(len(topic_list))

def get_related_topics(topic: Topic) -> List[Topic]:
    topic, href = topic.get_tuple()
    url = 'https://ground.news' + href
    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                             "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')

    related_topics = soup.find_all('div', class_='col-span-12 tablet:col-span-6 desktop:col-span-3')
    names = [_.find('span').text for _ in related_topics]
    hrefs = [_.find('a', href=True)['href'] for _ in related_topics]
    return Topic.create_list(names, hrefs)


def name2href(topic_name):
    return '/interest/' + topic_name.lower().replace(' ', '-')


if __name__ == '__main__':
    main()