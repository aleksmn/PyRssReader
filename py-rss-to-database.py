from xml.etree import ElementTree as etree
# from collections import Counter
# from bs4 import BeautifulSoup
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

def clear_from_spam(articles):
    """Clear articles from spam based on url"""
    spam_list = ['novosti-partnerov']
    for w in spam_list:
        articles = [x for x in articles if w not in x['url']]
    return articles

def print_titles(articles):
    string_limit = 86 #set limit of characters in line
    sleep_time = 0.01
    for article in articles:
        time_output = time_to_string(article['time'])
        title_output = article['title']
        url_output = article['url']
        
        if len(title_output) > string_limit:
                title_output = title_output[:string_limit-1] + '~'
                        
        print(f"[{time_output}] {title_output}\n{' ' * 8}{url_output}")

        # Compact view:
        # print(f"[{time_output}] {title_output}")
        time.sleep(sleep_time)    

def get_num_feeds():
    if len(sys.argv) > 1:
        num = sys.argv[1]
    else:
        # num = input(f'Введите количество источников (не более {len(URLS)}): ')
        num = len(URLS)

    try: 
        num = int(num)
        if num > len(URLS):
            num = len(URLS)
            print("Максимальное количестов источников: ", num)
    except:
        num = len(URLS)

    return num

URLS = [
    'https://www.interfax.ru/rss.asp',
    'http://tass.ru/rss/v2.xml'
]

num_feeds = get_num_feeds()

print(f'Подключаемся к источникам новостей ({num_feeds} из {len(URLS)})...')

articles = []

try:
    for url in URLS[:num_feeds]:
        for entry in get_items_from_url(url):
            articles.append(get_article(entry))

        
    articles = sort_by_time(clear_from_spam(articles))

    # Выводим время публикации и заголовки на экран
    print_titles(articles)

except requests.exceptions.ConnectionError as error:
    print('Нет соединения с интернетом.')
