from xml.etree import ElementTree as etree
from collections import Counter
from bs4 import BeautifulSoup
from datetime import datetime
import requests

EXCEPTED_WORDS = ['без', 'будет', 'вне', 'все', 'где', 'год', 'году', 'для', 
    'из-за', 'или', 'как', 'когда', 'кроме', 'между', 'над', 'них', 'нужно', 'перед',
    'под', 'при', 'про', 'ради', 'раз', 'среди', 'тем', 'того', 'только', 'уже',
    'через', 'что', 'этим', 'этим', 'это', 'этом']

URLS = [
    'https://www.interfax.ru/rss.asp'
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
        print("[{}] {}\n{}".format(article_time_string, article_title,article_url))


        urldata = requests.get(url = entry.findtext('guid'))

        urldata.encoding = 'cp1251'

        article = BeautifulSoup(urldata.text, 'html.parser').find('article')

        ParagraphContent = ""

        for paragraph in article.find_all('p'):
            ParagraphContent += paragraph.text

        for anchor in article.find_all('a'):
            ParagraphContent += anchor.text
        
        common_words = Counter([word.strip('.,') for word in ParagraphContent.replace('\r\n',' ')
                .split(' ') if word and not word in EXCEPTED_WORDS and len(word) > 2])

        for i in common_words.most_common(n = 5):
            print(f'{i[0]}: {i[1]}', end='; ')
        
        print('\n')