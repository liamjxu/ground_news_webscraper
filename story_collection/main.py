import json
import time
import argparse
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.common.exceptions import WebDriverException


def main(source: str = 'main'):
    href_name = source.split('/')[-1]
    root_url = "https://ground.news"

    hrefs = get_hrefs(source)
    print('length of found hrefs:', len(hrefs))

    result = {}
    for idx, href in enumerate(hrefs):
        full_url = root_url + href
        story_data = get_one_story(full_url)
        result[href.split('/')[-1].split('_')[0]] = story_data
        # Save the stored stories every 5 discoveries
        if (idx + 1) % 5 == 0:
            with open(f'story_collection/interest/{href_name}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
    with open(f'story_collection/interest/{href_name}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    story_num = len(result)
    article_num = len([y for x in list(result.values()) for y in x])
    return source, story_num, article_num


def get_hrefs(source: str = 'topic_list'):
    root_url = "https://ground.news"

    if source.startswith('/interest/'):
        url = root_url + source
        html_text = get_html_with_more_stories(url, more=15)
        soup = BeautifulSoup(html_text, 'lxml')
        top_news = soup.find('div', class_='col-span-12 desktop:col-span-12 flex flex-col gap-3_2 desktop:pr-1_6')
        latest_news = soup.find('div', class_='col-span-12 desktop:col-span-9 flex flex-col gap-3_2 desktop:pr-1_6')
        hrefs_top = []
        hrefs_latest = []
        if top_news is not None:
            hrefs_top = [a['href'] for a in top_news.find_all('a', href=True)]
        if latest_news is not None:
            hrefs_latest = [a['href'] for a in latest_news.find_all('a', href=True)]
        hrefs = hrefs_top + hrefs_latest

    else:
        raise Exception(f'the href "{source}" does not comply with the format "/interest/<topic_name>"')

    return hrefs


def get_one_story(full_url):
    html_text = get_html_with_more_stories(full_url, more='all', no_login=True)
    soup = BeautifulSoup(html_text, 'lxml')
    summaries = soup.find_all('div', class_='relative hidden tablet:flex')
    ret = []
    for idx, summary in enumerate(summaries):
        titles = summary.find_all('h4', class_='text-22 leading-11')
        names = summary.find_all('div', class_='flex bg-light-light rounded-full px-1 '
                                               'py-1/2 gap-8px items-center dark:bg-dark-light')
        abstracts = summary.find_all('p', class_='font-normal text-18 leading-9 break-words')
        buttons = summary.find_all('button')
        anchors = summary.find_all('a', href=True, class_='flex flex-col gap-8px cursor-pointer w-full')
        hrefs = [a['href'] for a in anchors]
        # TODO: elegant verification
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
            'factuality': buttons[1].text if len(buttons) > 1 else "Unknown",
            'additional badges': [button.text for button in buttons[2:]],
            'source link': hrefs[0]
        }
        ret.append(entry)
    return ret


def get_html_with_more_stories(url, more=5, no_login=False, suppress_browser=True):
    if suppress_browser:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    if no_login is False:
        try:
            login(driver)
        except BaseException:
            pass

    # Get more story id
    button_id = 'more-stories'
    try:
        driver.find_element(By.ID, 'more-stories')
    except BaseException:
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
            time.sleep(1)
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
    driver.quit()
    return html_text


def login(driver: webdriver.Chrome):
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
    parser.add_argument('--rank', type=int, default=1,
                        help='the local rank of the current process')
    parser.add_argument('--source', type=str, choices=['href', 'topic_list'],
                        default='href',
                        help='the source of input')
    parser.add_argument('--href', type=str,
                        default='/interest/gun-control',
                        help='the href to use if source is "href"')

    args = parser.parse_args()
    rank = args.rank

    # Credentials
    with open('credentials.json', 'r', encoding='utf-8') as f:
        creds = json.load(f)
    username = creds['username']
    password = creds['password']

    if args.source == 'topic_list':
        # Initialize the logs of the current process.
        logs = ['In Progress']
        if not os.path.exits('story_collection/logs/'):
            os.mkdir('story_collection/logs/')

        with open(f'story_collection/logs/rank_{rank}.json', 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)

        # Get topic_list and preprocessing to get the segment the current process is responsible for.
        with open('topic_collection/topic_list.json', 'r') as f:
            topic_list = json.load(f)
        topic_list = list(sorted(topic_list.items()))
        SEGMENT_WIDTH = 20
        start = rank * SEGMENT_WIDTH
        end = min(len(topic_list), start + SEGMENT_WIDTH)

        # Go through the segment and log each the status of each topic.
        for idx, (name, href) in enumerate(topic_list[start:end]):
            log = {'name': name}
            try:
                tic = time.time()
                source, story_num, article_num = main(href)
                toc = time.time()
                log['status'] = 'Successful'
                log['time'] = toc - tic
                log['source'] = source
                log['story_num'] = story_num
                log['article_num'] = article_num
                logs.append(log)
            except (BaseException, WebDriverException) as e:
                log['status'] = 'Failed'
                log['time'] = 0
                log['error message'] = e.msg if isinstance(e, WebDriverException) else str(e)
                logs.append(log)
            # Each time a topic is finished, save the log of the current process.
            # Each topic takes ~10mins
            with open(f'story_collection/logs/rank_{rank}.json', 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=4)

        # At the end, mark the process as finished.
        with open(f'story_collection/logs/rank_{rank}.json', 'w', encoding='utf-8') as f:
            logs = ['Finished'] + logs[1:]
            json.dump(logs, f, ensure_ascii=False, indent=4)

    elif args.source == 'href':
        source, story_num, article_num = main('/' + '/'.join(args.href.split('/')[-2:]))
        print(source, story_num, article_num)
