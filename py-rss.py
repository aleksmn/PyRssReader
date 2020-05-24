from xml.etree import ElementTree as etree
from collections import Counter
from bs4 import BeautifulSoup
import requests

EXCEPTED_WORDS = ['без','вне','для','кроме','между','над','перед','под',
                'ради','про','через','среди','что','из-за','год',
                'году','все','только','где','когда','тем','того','или','уже',]

URLS = [
    'https://www.interfax.ru/rss.asp'
]

for url in URLS:
    print ("Processing feed from <{}>\n".format(url))
    data = requests.get(url = url).text
    
    RSS = etree.fromstring(data)
    item = RSS.findall('channel/item')

    for entry in item:
        # print("Found entry: {}".format(entry))
        print(entry.findtext('title'))
        print(entry.findtext('guid'))

        urldata = requests.get(url = entry.findtext('guid'))

        urldata.encoding = 'cp1251'

        # Soup = BeautifulSoup(urldata.text, 'html.parser')

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