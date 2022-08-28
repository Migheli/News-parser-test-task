import requests
from bs4 import BeautifulSoup
import os
import json
import datetime
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parser.settings")
django.setup()
from newsparser.models import Tag, Channel, Article

def get_articles_links(url):
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.text, 'html.parser')
    news_source = 'https://market.yandex.ru'
    return [news_source + news_item.a['href'] for news_item in
            soup.select(".news-list__item")]


def get_article_dataset(article_url):
    page_content = requests.get(article_url)
    soup = BeautifulSoup(page_content.text, 'html.parser')
    print(f'ПЭЙДЖ_КОНТЕНТ========={page_content.text}==============')
    article_dataset = {}
    article_dataset['channel'] = 'Yandex'
    article_dataset['title'] = soup.find('div', class_='news-info__title').text
    date, time = soup.find('time', class_='news-info__published-date')[
        'datetime'].split('T')
    year, month, day = list(map(int, date.split('-')))
    article_dataset['published_at'] = datetime.date(year, month, day)
    article_dataset['text'] = soup.find('div',
                                        class_='news-info__post-body html-content page-content').text
    article_tags = soup.find_all('a',
                                 class_='link link_theme_light-gray news-info__tag i-bem')
    article_tags_headers = []
    for news_tag in article_tags:
        article_tags_headers.append(news_tag.text)
    article_dataset['tags'] = article_tags_headers
    return article_dataset



def update_or_create_article(article_dataset):
    if article_dataset['tags']:
        tags = []
        print(article_dataset['tags'])
        for article_tag in article_dataset['tags']:
            tag, created = Tag.objects.get_or_create(
                title=article_tag
            )
            tags.append(tag)
        print(tags)
    else:
       tags = None
    channel, created = Channel.objects.get_or_create(
            title=article_dataset['channel']
        )

    article, created = Article.objects.update_or_create(
        title=article_dataset['title'],

        defaults={
            'channel': channel,
            'text': article_dataset.get('text', ''),
            'published_at': article_dataset['published_at']
        }

    )
    if tags:
        article.tags.set(tags)





def main():
    articles_url = 'https://market.yandex.ru/partners/news'
    articles_links = get_articles_links(articles_url)
    articles_datasets = [get_article_dataset(article_link) for article_link in articles_links]

    for article_dataset in articles_datasets:
        update_or_create_article(article_dataset)

    a = Article.objects.filter(tags__title__contains='#FBY')
    print(a)
# Запуск кода
if __name__ == '__main__':
    main()