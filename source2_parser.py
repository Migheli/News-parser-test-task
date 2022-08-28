from bs4 import BeautifulSoup
import datetime
import os
import django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Parser.settings")
django.setup()
from newsparser.models import Tag, Channel, Article

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import locale
from environs import Env

env = Env()
env.read_env()

PARSE_TASK_NUMBER=10

def get_articles_links(url, next_button_xpath, driver):
    driver.get(url)
    next_page_button = driver.find_element(By.XPATH, next_button_xpath)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    article_link_items = soup.find_all('a', class_=env.str('CHANNEL_TWO_LINK_CLASS'))

    while len(article_link_items) < PARSE_TASK_NUMBER:
        next_page_button.click()
        time.sleep(5)
        article_link_items += soup.find_all('a', class_=env.str('CHANNEL_TWO_LINK_CLASS'))

    article_dates_serialized = []
    article_dates = soup.find_all('span', class_=env.str('CHANNEL_TWO_DATE_CLASS'))
    for article_date in article_dates:
        article_dates_serialized.append(article_date.text)

    news_source = env.str('CHANNEL_TWO_BASELINK')
    article_links = [news_source + article_link_item['href'] for article_link_item in article_link_items]
    time.sleep(5)
    return list(zip(article_links, article_dates_serialized))


def get_article_dataset(article_url, article_date, driver):
    driver.get(article_url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    article_dataset = {}
    article_dataset['channel'] = env.str('CHANNEL_TWO_NAME')

    article_dataset['title'] = soup.find('h1', class_=env.str('CHANNEL_TWO_TITLE_CLASS')).text.replace('  ', '').replace('\n', '')
    article_dataset['text'] = soup.find('section', class_=env.str('CHANNEL_TWO_TEXT_CLASS')).text.replace('  ', '').replace('\n', '')
    article_dataset['tags'] = None
    tags = soup.find('div', class_=env.str('CHANNEL_TWO_TAG_CLASS'))

    if tags:
        tags = tags.text
        if ',' in tags:
            tags = tags.split(',')
        else:
            tags = [tags]
        tags = [tag.replace(' ', '').replace('\n', '').replace('#', '') for tag in tags]
        article_dataset['tags'] = tags

    locale.setlocale(locale.LC_TIME, "rus")
    months = {'января': 'январь',
              'февраля': 'февраль',
              'марта': 'март',
              'апреля': 'апрель',
              'мая': 'май',
              'июня': 'июнь',
              'июля': 'июль',
              'августа': 'август',
              'сентября': 'сентябрь',
              'октября': 'октябрь',
              'ноября': 'ноябрь',
              'декбаря': 'декабрь',
              }
    for k, v in months.items():
        article_date = article_date.replace(k, v)
    article_date += env.str('CURRENT_YEAR')
    published_at = datetime.date(datetime.strptime(article_date, "%d %B %Y"))
    article_dataset['published_at'] = published_at
    return article_dataset

def update_or_create_article(article_dataset):
    if article_dataset['tags']:
        tags = []
        for article_tag in article_dataset['tags']:
            tag, created = Tag.objects.get_or_create(
                title=article_tag
            )
            tags.append(tag)
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
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(chrome_options=options)

    next_button_xpath = env.str('CHANNEL_TWO_NEXT_PAGE_BTN_XPATH')
    url = env.str('CHANNEL_TWO_NEWS_LINK')
    article_links= get_articles_links(url, next_button_xpath, driver)

    for article_link in article_links:
        link, date = article_link
        article_dataset = get_article_dataset(link, date, driver)
        update_or_create_article(article_dataset)
        time.sleep(5)
    driver.close()


if __name__ == '__main__':
    main()
