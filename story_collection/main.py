import json
import time
import argparse
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.common.exceptions import WebDriverException


def main(args):
    # set up driver
    if args.headless:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome()
    driver.get('https://ground.news')
    with open('credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    username = creds['username']
    password = creds['password']
    login(driver, username, password)

    # set up data folders
    if not os.path.exists(f'story_collection/{args.tag}_logs/'):
        os.mkdir(f'story_collection/{args.tag}_logs/')
    if not os.path.exists(f'story_collection/{args.tag}_interest/'):
        os.mkdir(f'story_collection/{args.tag}_interest/')

    # do the actual collection
    if args.source == 'topic_list':
        # Initialize the logs.
        logs = ['In Progress']
        with open(f'story_collection/{args.tag}_logs/logs.json', 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

        # Get topic_list.
        with open('topic_collection/topic_list.json', 'r') as f:
            topic_list = json.load(f)
        topic_list = list(sorted(topic_list.items()))

        # Go through the segment and log each the status of each topic.
        for topic, topic_href in topic_list:
            try:
                # For each href in the topic_list, get stories for that href.
                tic = time.time()
                source, story_num, article_num = get_all_story_per_href(driver, topic_href, args.tag)
                toc = time.time()
                logs.append({
                    'topic': topic,
                    'status': 'Successful',
                    'time': toc - tic,
                    'source': source,
                    'story_num': story_num,
                    'article_num': article_num
                })
            except (BaseException, WebDriverException) as e:
                logs.append({
                    'topic': topic,
                    'status': 'Failed',
                    'time': 0,
                    'error_message': e.msg if isinstance(e, WebDriverException) else str(e)
                })
            # Each time a topic is finished, save the log of the current process.
            # Each topic takes ~10mins
            with open(f'story_collection/{args.tag}_logs/logs.json', 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=4)

        # At the end, mark the process as finished.
        with open(f'story_collection/{args.tag}_logs/logs.json', 'w', encoding='utf-8') as f:
            logs[0] = 'Finished'
            json.dump(logs, f, ensure_ascii=False, indent=4)

    elif args.source == 'href':
        topic_href = '/' + '/'.join(args.href.split('/')[-2:])
        ret = get_all_story_per_href(driver, topic_href, args.tag)
        print(ret)


def get_all_story_per_href(driver: webdriver.Chrome, href: str = '/interest/example', tag: str = 'latest'):
    '''For each of the topic, get the story informations and dump to a json file'''

    # some initialization
    root_url = 'https://ground.news'
    topic_name = href.split('/')[-1]

    # Get all story hrefs for the topic
    story_hrefs = get_all_shref_per_topic(driver, href)
    print('length of found story_hrefs:', len(story_hrefs))

    # Get article informations
    result = {'stats': 'finished idx: -1 / -1'}
    for story_idx, href in enumerate(story_hrefs):
        story_data = get_all_article_per_story(driver, root_url + href)
        # If somehow the story contains no article, then it should not be included.
        if len(story_data) == 0:
            continue
        result[href.split('/')[-1].split('_')[0]] = story_data

        result['stats'] = f'finished idx: {story_idx} / {len(story_hrefs)}'
        with open(f'story_collection/{tag}_interest/{topic_name}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    # quit driver
    driver.quit()

    # Some basic stats
    story_num = len(result)
    article_num = len([y for x in list(result.values()) for y in x])

    return href, story_num, article_num


def get_all_shref_per_topic(driver: webdriver.Chrome, href: str = '/interest/example'):
    '''For a topic, get the hrefs for stories in that topic'''

    root_url = "https://ground.news"

    if href.startswith('/interest/'):
        # Get and parse the stories displayed under that topic
        html_text = get_html_with_more_stories(driver, root_url + href, more=15)
        soup = BeautifulSoup(html_text, 'lxml')

        # Gather hrefs
        hrefs = []
        for news in [
            soup.find('div', class_='col-span-12 desktop:col-span-12 flex flex-col gap-3_2 desktop:pr-1_6'),
            soup.find('div', class_='col-span-12 desktop:col-span-9 flex flex-col gap-3_2 desktop:pr-1_6')
        ]:
            if news:
                hrefs += [a['href'] for a in news.find_all('a', href=True)]
    else:
        # unknown topic href.
        raise Exception(f'the href "{href}" does not comply with the format "/interest/<topic_name>"')

    return hrefs  # This is the hrefs of the stories


def get_all_article_per_story(driver: webdriver.Chrome, full_url):
    ret = []

    # Get all summaries
    html_text = get_html_with_more_stories(driver, full_url, more='all')
    soup = BeautifulSoup(html_text, 'lxml')
    summaries = soup.find_all('div', class_='relative hidden tablet:flex')

    for idx, summary in enumerate(summaries):
        titles = summary.find_all('h4', class_='text-22 leading-11')
        names = summary.find_all('div', class_='flex bg-light-light rounded-full px-1 '
                                               'py-1/2 gap-8px items-center dark:bg-dark-light')
        abstracts = summary.find_all('p', class_='font-normal text-18 leading-9 break-words')
        buttons = summary.find_all('button')
        anchors = summary.find_all('a', href=True, class_='flex flex-col gap-8px cursor-pointer w-full')
        hrefs = [a['href'] for a in anchors]
        assert len(names) == len(titles) == len(abstracts) == len(hrefs) == 1

        # Get bias and factuality for the article.
        bias = 'Unknown'
        factuality = 'Unknown'
        for b in buttons:
            if b.text in ["Left", "Lean Left", "Center", "Lean Right", "Right"]:
                bias = b.text
            if b.text in ["High Factuality", "Low Factuality", "Mixed Factuality"]:
                factuality = b.text

        # Append the article into the story.
        entry = {
            'index': idx,
            'title': titles[0].text,
            'name': names[0].text,
            'abstract': abstracts[0].text,
            'bias': bias,
            'factuality': factuality,
            'all_badges': [button.text for button in buttons],
            'source_link': hrefs[0]
        }
        ret.append(entry)

    return ret


def get_html_with_more_stories(driver, url, more=15):

    driver.get(url)
    time.sleep(1)
    # Get more story id
    try:
        # this is actually for loading more articles, the button has text "More Articles" on the story page
        driver.find_element(By.ID, 'more-stories')
        button_id = 'more-stories'
    except BaseException:
        # this is actually for loading more stories, the button has text "More Stories" on the topic page
        button_id = 'more_stories'

    if more == 'all':
        yes_more_stories = True
        while yes_more_stories:
            try:
                # close
                close_input = driver.find_element(By.XPATH, "//button[@class='react-responsive-modal-closeButton']")
                close_input.click()
            except BaseException:
                pass

            try:
                driver.find_element(By.ID, button_id).click()
            except BaseException:
                yes_more_stories = False
    else:
        cnt = 0
        while cnt < more:
            # time.sleep(1)
            try:
                # close
                close_input = driver.find_element(By.XPATH, "//button[@class='react-responsive-modal-closeButton']")
                close_input.click()
            except BaseException:
                pass

            try:
                driver.find_element(By.ID, button_id).click()
            except BaseException:
                pass
            cnt += 1

    html_text = driver.page_source
    return html_text


def login(driver: webdriver.Chrome, username: str, password: str):
    login_button = driver.find_element(By.ID, "header-login")
    login_button.click()

    # Login
    username_input = driver.find_element(By.XPATH, "//input[@type='email']")
    username_input.send_keys(username)
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys(password)
    submit_input = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_input.click()
    time.sleep(1)
    driver.refresh()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--start_idx', type=int, default=0,
    #                     help='the local rank of the current process')
    # parser.add_argument('--end_idx', type=int, default=-1,
    #                     help='the local rank of the current process')
    parser.add_argument('--source', type=str, choices=['href', 'topic_list'], default='href',
                        help='the source of input')
    parser.add_argument('--href', type=str, default='/interest/gun-control',
                        help='the href to use if source is "href"')
    parser.add_argument('--tag', type=str, default='latest',
                        help='the tag to use for data version labeling')
    parser.add_argument('--headless', action='store_true',
                        help='to use headless mode (leave out if debugging)')
    args = parser.parse_args()
    main(args)
