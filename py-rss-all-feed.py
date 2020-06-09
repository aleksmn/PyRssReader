from xml.etree import ElementTree as etree
from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime
import requests

URLS = [
    'https://www.interfax.ru/rss.asp',
    'http://tass.ru/rss/v2.xml'

]

for url in URLS:
    print ("Processing feed from <{}>\n".format(url))
    data = requests.get(url = url).text
    
    RSS = etree.fromstring(data)
    items = RSS.findall('channel/item')

    for entry in items[::-1]:   #reversed(items)
        # print("Found entry: {}".format(entry))  

        article_raw_time_string = entry.findtext('pubDate') # Tue, 26 May 2020 13:27:00 +0300
        t = datetime.strptime(article_raw_time_string, '%a, %d %b %Y %H:%M:%S %z')
        article_time_string = datetime.strftime(t, '%H:%M') # '%d.%m.%y %H:%M' --> 26.05.20 13:27

        article_title = entry.findtext('title')
        article_url = entry.findtext('guid')

        # Output time and title
        print("[{}] {}\n{}'\n'".format(article_time_string, article_title,article_url))
