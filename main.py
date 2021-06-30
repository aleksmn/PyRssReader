from myrsslib import *


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
