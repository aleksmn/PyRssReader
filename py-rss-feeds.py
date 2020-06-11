from xml.etree import ElementTree as etree
from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime
import requests

def time_to_string(time_object):
    return datetime.strftime(time_object, '%H:%M') # '%d.%m.%y %H:%M' --> 26.05.20 13:27


URLS = [
    'https://www.interfax.ru/rss.asp',
    'http://tass.ru/rss/v2.xml'
]

articles = []

try:
    for url in URLS:
        data = requests.get(url = url).text
        print (f"Собираем данные с <{url}>...")
        RSS = etree.fromstring(data)
        items = RSS.findall('channel/item')

        for entry in items:
            article = {}
            article['time'] = datetime.strptime(entry.findtext('pubDate'), '%a, %d %b %Y %H:%M:%S %z')
            # Example of 'pubdate':  Tue, 26 May 2020 13:27:00 +0300 
            article['title'] = entry.findtext('title')
            article['url'] = entry.findtext('guid')

            articles.append(article)

        
    # Сортируем заголовки по времени:
    # newlist = sorted(list_to_be_sorted, key=lambda k: k['name']) 

    articles = sorted(articles, key=lambda k: k['time'], reverse=False)

    # Выводим время публикации и заголовки на экран
    print()
    for article in articles:
        print(f"[{time_to_string(article['time'])}] {article['title']}\n{article['url']}\n")

except requests.exceptions.ConnectionError as error:
    print('Нет соединения с интернетом.')
