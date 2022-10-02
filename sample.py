from bs4 import BeautifulSoup
import requests

url = "https://ground.news/article/yeshiva-university-lgbtq-club-agree-to-delay-recognition-amid-appeal_e238f5"
headers = {"User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 ("
                         "KHTML, like Gecko) Version/4.0 Safari/534.30"}
html_text = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_text, 'lxml')
summaries = soup.find_all('div', class_='relative hidden tablet:flex')

for summary in summaries:
    titles = summary.find_all('h4', class_='text-22 leading-11')
    names = summary.find_all('div', class_='flex bg-light-light rounded-full px-1 py-1/2 gap-8px items-center dark:bg-dark-light')
    for name in names:
        print(name.text.strip())
    for title in titles:
        print(title.text.strip())
    print()