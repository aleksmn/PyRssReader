from xml.etree import ElementTree as etree
from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import sys

def time_to_string(time_object):
    return datetime.strftime(time_object, '%H:%M') # '%d.%m.%y %H:%M' --> 26.05.20 13:27


def sort_by_time(articles, reverse=False):
    """Sort articles by time, by default do not reverse: 
    most recent at the bottom."""
    return sorted(articles, key=lambda k: k['time'], reverse=reverse)



URLS = [
    'https://www.interfax.ru/rss.asp',
    'http://tass.ru/rss/v2.xml'
]


if len(sys.argv) > 1:
    num = sys.argv[1]
else:
    #num = input(f'Введите количество источников (не более {len(URLS)}): ')
    num = len(URLS)

try: 
    num = int(num)
except:
    num = len(URLS)

articles = []

print(f'\nПодключаемся к источникам новостей ({num} из {len(URLS)})...')

def get_items_from_url(url):
    """Getting items from URL of RSS feed"""
    data = requests.get(url = url).text
    print (f"Собираем данные с <{url}>...")
    RSS = etree.fromstring(data)
    return RSS.findall('channel/item')

def get_article(entry):
    """Get article from the entry on RSS feed. Return article as dictionary with atributes time, date, url."""
    article = {}
    article['time'] = datetime.strptime(entry.findtext('pubDate'), '%a, %d %b %Y %H:%M:%S %z')
            # Example of 'pubdate':  Tue, 26 May 2020 13:27:00 +0300 
    article['title'] = entry.findtext('title')
    article['url'] = entry.findtext('guid')
    return article

try:
    for url in URLS[:num]:
        items = get_items_from_url(url)

        for entry in items:
            articles.append(get_article(entry))

        
    articles = sort_by_time(articles)

    # Выводим время публикации и заголовки на экран
    for article in articles:
        if 'novosti-partnerov' in article['url']:
            continue
        time_output = time_to_string(article['time'])
        title_output = article['title']
        url_output = article['url']
        
        string_limit = 86
        if len(title_output) > string_limit:
                title_output = title_output[:string_limit-1] + '~'
                      
        # print(f"[{time_output}] {title_output}\n{' ' * 8}{url_output}")

        # Compact view:
        print(f"[{time_output}] {title_output}")

        time.sleep(0.01)

except requests.exceptions.ConnectionError as error:
    print('Нет соединения с интернетом.')
