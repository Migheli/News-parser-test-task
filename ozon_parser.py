import requests
from bs4 import BeautifulSoup
import os
import json
import datetime
import os
import django
import time
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parser.settings")
django.setup()
from newsparser.models import Tag, Channel, Article

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import locale



def get_articles_links(url, next_button_xpath, driver):
    driver.get(url)
    next_page_button = driver.find_element(By.XPATH, next_button_xpath)
    next_page_button.click()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    article_link_items = soup.find_all('a', class_='news-card__link')
    article_dates_serialized = []
    article_dates = soup.find_all('span', class_='news-card__date')
    for article_date in article_dates:
        article_dates_serialized.append(article_date.text)

    print(f'ДАТЫ=================================={article_dates}')

    article_links = []
    news_source = 'https://seller.ozon.ru'
    for article_link_item in article_link_items:
        article_link = news_source + article_link_item['href']
        article_links.append(article_link)
    print(article_links)
    time.sleep(10)
    print(f'ЗАЗИПОВАННЫЕ КОРТЕЖИ ==========================={list(zip(article_links, article_dates_serialized))}')
    return list(zip(article_links, article_dates_serialized))


def get_article_dataset(article_url, article_date, driver):
    driver.get(article_url)
    time.sleep(3)
    print(f'ПЕРЕДАННЫЙ УРЛ====={article_url}')
    #page_content = requests.get(article_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    article_dataset = {}
    article_dataset['channel'] = 'Ozon'

    article_dataset['title'] = soup.find('h1', class_='new-top__title title_Oebvj title_Oebvj title--h1-smaller_RUef6').text.replace('  ', '').replace('\n', '')
    print(article_dataset['title'])
    article_dataset['text'] = soup.find('section', class_='new-section html-content_Ol8P9').text
    print(article_dataset['text'])
    article_dataset['tags'] = None
    tags = soup.find('div', class_='page-info__topic-value')
    #Может быть ситуация, когда тегов у поста нет. Проверяем пост на наличие тегов.
    if tags:
        tags = tags.text
        if ',' in tags:
            tags = tags.split(',')
        else:
            tags = [tags]
        tags = [tag.replace(' ', '').replace('\n', '').replace('#', '') for tag in tags]
        article_dataset['tags'] = tags

    print(tags)


    locale.setlocale(locale.LC_TIME, "rus")
    months = {'августа': 'август', 'июля': 'июль'}
    for k, v in months.items():
        article_date = article_date.replace(k, v)
    article_date += ' 2022'
    published_at = datetime.date(datetime.strptime(article_date, "%d %B %Y"))
    print(published_at)
    article_dataset['published_at'] = published_at
    print(article_dataset)
    return(article_dataset)



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




#element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))
def main():
    options = Options()
    # opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    # opts.add_experimental_option('useAutomationExtension', False)

    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(chrome_options=options)

    next_button_xpath = '//*[@id="__layout"]/div/div[1]/div/div[2]/div/button'
    url = 'https://seller.ozon.ru/news/'
    article_links= get_articles_links(url, next_button_xpath, driver)
    print(article_links)
    for article_link in article_links[:-12]:
        link, date = article_link
        article_dataset = get_article_dataset(link, date, driver)
        update_or_create_article(article_dataset)
        time.sleep(5)

if __name__ == '__main__':
    main()

#print(driver.page_source)
#driver.close()
