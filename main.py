from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
import time


def get_one_story(full_url):
    html_text = get_html_with_all_articles(full_url)
    soup = BeautifulSoup(html_text, 'lxml')
    summaries = soup.find_all('div', class_='relative hidden tablet:flex')
    ret = []
    for idx, summary in enumerate(summaries):
        titles = summary.find_all('h4', class_='text-22 leading-11')
        names = summary.find_all('div', class_='flex bg-light-light rounded-full px-1 py-1/2 gap-8px items-center dark:bg-dark-light')
        abstracts = summary.find_all('p', class_='font-normal text-18 leading-9 break-words')
        buttons = summary.find_all('button')
        hrefs = [a['href'] for a in summary.find_all('a', href=True, class_='flex flex-col gap-8px cursor-pointer w-full')]
        #TODO: elegant verification
        if len(abstracts) > 1:
            print(titles, names, abstracts)
        assert len(names) == 1
        assert len(titles) == 1
        assert len(abstracts) == 1
        assert len(hrefs) == 1
        entry = {
            'index': idx,
            'title': titles[0].text,
            'name': names[0].text,
            'abstract': abstracts[0].text,
            'bias': buttons[0].text if len(buttons) > 0 else "Unknown",
            'factuality': buttons[1].text if len(buttons) > 0 else "Unknown",
            'additional badges': [button.text for button in buttons[2:]],
            'source link': hrefs[0]
        }
        ret.append(entry)
    return ret


def get_html_with_all_articles(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    yes_more_stories = True
    while yes_more_stories:
        try:
            driver.find_element(By.ID, 'more-stories').click()
        except:
            yes_more_stories = False

    html_text = driver.page_source
    driver.quit()
    return html_text


if __name__ == '__main__':
    tic = time.time()
    url = "https://ground.news"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                             "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    section = soup.find_all('section', id='newsroom-feed-tablet-and-mobile')

    hrefs = [a['href'] for a in section.find_all('a', href=True)]

    result = {}
    for href in hrefs[:2]:
        full_url = url + href
        story_data = get_one_story(full_url)
        
        result[href.split('/')[-1].split('_')[0]] = story_data

    print('Found stories: ', len(result))
    print('# Titles: ', len([y for x in list(result.values()) for y in x]))
    with open('ground_news.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    toc = time.time()
    print(toc - tic)