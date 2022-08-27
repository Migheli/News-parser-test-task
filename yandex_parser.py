import requests
from bs4 import BeautifulSoup
import os
import json
import datetime


# from newsparser.models import Tag, Channel, Article

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
    article_dataset['date'] = datetime.date(year, month, day)
    article_dataset['text'] = soup.find('div',
                                        class_='news-info__post-body html-content page-content').text
    article_tags = soup.find_all('a',
                                 class_='link link_theme_light-gray news-info__tag i-bem')
    article_tags_headers = []
    for news_tag in article_tags:
        article_tags_headers.append(news_tag.text)
    article_dataset['tags'] = article_tags_headers
    return article_dataset


'''
def update_or_create_article(article_dataset):
    article, created = Article.objects.update_or_create(
        title=article_dataset['title'],
        channel = Channel.objects.get_or_create(
            title = article_dataset['channel']
        )

    )
'''


def main():
    articles_url = 'https://market.yandex.ru/partners/news'
    articles_links = get_articles_links(articles_url)
    print(articles_links)
    articles_datasets = []
    for article_link in articles_links:
        print(f'ВНИМАНИЕ==========={article_link}===========')
        article_dataset = get_article_dataset(article_link)
        print(article_dataset)
        articles_datasets.append(article_dataset)
    '''
    channel, created = Channel.objects.get_or_create(
        title=article_dataset['channel']
    )

    tags = []
    for article_tag in article_dataset['tags']:
        tag, created = Tag.objects.get_or_create(
            title=article_tag
        )
        tags.append(tag)
    '''


# Запуск кода
if __name__ == '__main__':
    main()