from myrsslib import *

FEEDS = [
    {'feedname': 'Interfax', 'url': 'https://www.interfax.ru/rss.asp'},
    {'feedname': 'TASS', 'url': 'http://tass.ru/rss/v2.xml'},
    {'feedname': 'Meduza', 'url': 'https://meduza.io/rss2/all'},
]

num_feeds = get_num_feeds(FEEDS)
print(f'Подключаемся к источникам новостей ({num_feeds} из {len(FEEDS)})...')
articles = []
try:
    for feed in FEEDS[:num_feeds]:
        for entry in get_items_from_feed(feed):
            articles.append(get_article(entry, feed))

        
    articles = sort_by_time(clear_from_spam(articles))

    # Выводим время публикации и заголовки на экран
    print_titles(articles)

    # Добавляем заголовки в базу данных
    add_to_db(articles)

except requests.exceptions.ConnectionError as error:
    print('Нет соединения с интернетом.')
