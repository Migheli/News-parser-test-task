import requests
from bs4 import BeautifulSoup
import os
import json
import datetime

def main():
    url = 'https://market.yandex.ru/partners/news'
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.text, 'html.parser')
    news_links = []
    news_source = 'https://market.yandex.ru'
    for news_item in soup.select(".news-list__item"):
        news_links.append((news_source + news_item.a['href']))
    news_datasets = []
    for news_link in news_links:
        page_content = requests.get(news_link)
        soup = BeautifulSoup(page_content.text, 'html.parser')
        news_dataset = {}
        news_dataset['channel_tag'] = 'Yandex'
        news_dataset['title'] = soup.find('div', class_='news-info__title').text
        date, time = soup.find('time', class_='news-info__published-date')['datetime'].split('T')
        year, month, day = list(map(int, date.split('-')))
        news_dataset['date'] = datetime.date(year, month, day)
        print(news_dataset['date'])
        news_dataset['text'] = soup.find('div', class_='news-info__post-body html-content page-content').text
        news_tags = soup.find_all('a', class_='link link_theme_light-gray news-info__tag i-bem')
        news_tags_headers = []
        for news_tag in news_tags:
            news_tags_headers.append(news_tag.text)
        news_dataset['tags']= news_tags_headers
        print(news_dataset)


# Запуск кода
if __name__ == '__main__':
    main()