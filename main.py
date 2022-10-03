from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import json
import time


def main(source):
    root_url = "https://ground.news"
    
    hrefs = get_hrefs(source)
    print(len(hrefs))

    result = {}
    for idx, href in enumerate(hrefs):
        full_url = root_url + href
        story_data = get_one_story(full_url)
        result[href.split('/')[-1].split('_')[0]] = story_data
        if (idx + 1) % 10 == 0:
            with open('ground_news.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

    print('Found stories: ', len(result))
    print('# Articles: ', len([y for x in list(result.values()) for y in x]))


def get_hrefs(source='main'):

    root_url = "https://ground.news"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                             "KHTML, like Gecko) Version/4.0 Safari/534.30"}
    
    if source == 'main':
        url = "https://ground.news"
        html_text = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_text, 'lxml')
        section = soup.find_all('section', id='newsroom-feed-tablet-and-mobile')
        hrefs = [a['href'] for a in section.find_all('a', href=True)]

    elif source == 'interest/politics':
        url = root_url + '/' + source
        html_text = get_html_with_more_stories(url, more=15)
        soup = BeautifulSoup(html_text, 'lxml')
        top_news = soup.find('div', class_='col-span-12 desktop:col-span-12 flex flex-col gap-3_2 desktop:pr-1_6')
        latest_news = soup.find('div', class_='col-span-12 desktop:col-span-9 flex flex-col gap-3_2 desktop:pr-1_6')
        hrefs = [a['href'] for _ in [top_news, latest_news] for a in _.find_all('a', href=True)]

    return hrefs

def get_one_story(full_url):
    html_text = get_html_with_more_stories(full_url, more='all', no_login=True)
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
            'factuality': buttons[1].text if len(buttons) > 1 else "Unknown",
            'additional badges': [button.text for button in buttons[2:]],
            'source link': hrefs[0]
        }
        ret.append(entry)
    return ret


def get_html_with_more_stories(url, more=5, no_login=False):
    driver = webdriver.Chrome()
    driver.get(url)
    if no_login is False:
        try:
            login(driver)
        except:
            pass

    # Get more story id
    button_id = 'more-stories'
    try:
        driver.find_element(By.ID, 'more-stories')
    except:
        button_id = 'more_stories'
    
    if more == 'all':
        yes_more_stories = True
        while yes_more_stories:
            try:
                #close
                close_input = driver.find_element(By.XPATH, "//button[@class='react-responsive-modal-closeButton']")
                close_input.click()
            except:
                pass

            try:
                driver.find_element(By.ID, button_id).click()
            except:
                yes_more_stories = False
    else:
        cnt = 0
        while cnt < more:
            time.sleep(1)
            try:
                #close
                close_input = driver.find_element(By.XPATH, "//button[@class='react-responsive-modal-closeButton']")
                close_input.click()
            except:
                pass

            try:
                driver.find_element(By.ID, button_id).click()
            except:
                pass
            cnt += 1

    html_text = driver.page_source
    driver.quit()
    return html_text


def login(driver):
    login_button = driver.find_element(By.ID, "header-login")
    login_button.click()

    # Login
    username = "lilynette789@gmail.com"
    password = "limanling"
    username_input = driver.find_element(By.XPATH, "//input[@type='email']")
    username_input.send_keys(username)
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    password_input.send_keys(password)
    submit_input = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_input.click()
    time.sleep(1)
    driver.refresh()


if __name__ == '__main__':
  
    tic = time.time()
    main('interest/politics')
    toc = time.time()
    
    print(toc - tic)