import os

from myrsslib import *

FEEDS = [
    {'feedname': 'Interfax', 'url': 'https://www.interfax.ru/rss.asp'},
    # {'feedname': 'TASS', 'url': 'http://tass.ru/rss/v2.xml'}
]

def main():

    num_feeds = get_num_feeds(FEEDS)
    print(f'Подключаемся к источникам новостей ({num_feeds} из {len(FEEDS)})...')
    articles = []
    try:
        for feed in FEEDS[:num_feeds]:
            for entry in get_items_from_feed(feed):
                articles.append(get_article(entry, feed))

            
        articles = sort_by_time(clear_from_spam(articles))
        os.system("cls||clear")    
        # Выводим время публикации и заголовки на экран
        print_titles(articles)

        # Добавляем заголовки в базу данных
        # add_to_db(articles)


    except requests.exceptions.ConnectionError as error:
        print('Нет соединения с интернетом.')


if __name__ == "__main__":
    while True:
        main()
        answer = input("Repeat? (Y/n) ")
        answer = answer.lower().strip()
        if answer == "n" or answer == "н":
            break 