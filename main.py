from bs4 import BeautifulSoup
import requests
import json


def get_title_and_name(full_url, headers):
    html_text = requests.get(full_url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    summaries = soup.find_all('div', class_='relative hidden tablet:flex')
    ret = {}
    for summary in summaries:
        titles = summary.find_all('h4', class_='text-22 leading-11')
        names = summary.find_all('div', class_='flex bg-light-light rounded-full px-1 py-1/2 gap-8px items-center dark:bg-dark-light')
        assert len(names) == 1
        assert len(titles) == 1
        ret[names[0].text.strip()] = titles[0].text.strip()
    return ret

if __name__ == '__main__':

    url = "https://ground.news"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                             "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    section = soup.find_all('section', id='newsroom-feed-tablet-and-mobile')[0]

    hrefs = [a['href'] for a in section.find_all('a', href=True)]

    result = {}
    for href in hrefs:
        full_url = url + href
        name_title = get_title_and_name(full_url, headers)
        result[href.split('/')[-1].split('_')[0]] = name_title

    print('Found stories: ', len(result))
    print('Title per story: ', len(list(result.values())[0]))
    with open('title_name.json', 'w') as f:
        json.dump(result, f, indent=4)