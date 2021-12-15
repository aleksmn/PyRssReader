from xml.etree import ElementTree as etree
# from collections import Counter
# from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import sys
import os
import sqlite3

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def get_num_feeds(URLS):
    """Getting number of urls to scrap, max value is len of URLs list."""
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

def time_to_string(time_object):
    return datetime.strftime(time_object, '%H:%M') # '%d.%m.%y %H:%M' --> 26.05.20 13:27

def sort_by_time(articles, reverse=False):
    """Sort articles by time, by default do not reverse: 
    most recent at the bottom."""
    return sorted(articles, key=lambda k: k['time'], reverse=reverse)

def get_items_from_feed(feed):
    """Getting items from URL of RSS feed"""
    data = requests.get(url = feed['url']).text
    print (f"Собираем данные с {feed['feedname']}...")
    RSS = etree.fromstring(data)
    return RSS.findall('channel/item')

def get_article(entry, feed):
    """Get article from the entry on RSS feed. Return article as dictionary with atributes time, date, url."""
    article = {}
    article['time'] = datetime.strptime(entry.findtext('pubDate'), '%a, %d %b %Y %H:%M:%S %z')
            # Example of 'pubdate':  Tue, 26 May 2020 13:27:00 +0300 
    article['title'] = entry.findtext('title')
    article['url'] = entry.findtext('guid')
    article['feedname'] = feed['feedname']
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
        feedname = article['feedname']
        if len(title_output) > string_limit:
                title_output = title_output[:string_limit-1] + '~'
                        
        # print(f"[{time_output}] {title_output}\n{' ' * 8}({feedname}) {url_output}")

        # Compact view:
        print(f"[{time_output}] {title_output}")
        time.sleep(sleep_time)    

def add_to_db(articles):
    """Add article to the news.db"""
    path_to_db = get_script_path() + '/news.db'
    conn = sqlite3.connect(path_to_db)
    c = conn.cursor()
    
    # find most recent title in db
    most_recent_time = ''
    c.execute("SELECT * FROM titles ORDER BY time DESC LIMIT 1")
    most_recent_row = c.fetchone()
    if most_recent_row is not None:
        most_recent_time = most_recent_row[0]

    for a in articles:
        # add only new titles to db
        if str(a['time']) > most_recent_time:
            c.execute("INSERT INTO titles VALUES (?, ?, ?, ?)", 
                        (a['time'], a['title'], a['url'], a['feedname']))

        else:
            continue

    conn.commit()
    conn.close()
    

if __name__ ==  "__main__":
    path_to_db = get_script_path() + '/' + 'news.db'
    print(path_to_db)

    # Create db
    conn = sqlite3.connect(path_to_db)
    c = conn.cursor()
    # c.execute("""CREATE TABLE titles (

    #             time text,
    #             title text,
    #             url text,
    #             feedname text
    #         )""")   
    
    c.execute("SELECT * FROM titles WHERE feedname=='Meduza' ORDER BY time")
    for i in c.fetchall():
        print(i[0], i[1])

    c.execute("SELECT * FROM titles ORDER BY time DESC LIMIT 1") 
    print('Last title: ', c.fetchone())

    conn.commit()
    conn.close()
