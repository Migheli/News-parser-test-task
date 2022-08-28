from django.http import JsonResponse
from newsparser.models import Article, Tag
# Create your views here.


def show_news_by_tagname(request, hashtag):
    target_articles = Article.objects.filter(tags__title__contains=hashtag)
    serialized_articles = []
    for article in target_articles:
        tags_data=[]
        if article.tags:
            tags = Tag.objects.filter(articles=article)
            for tag in tags:
                tags_data.append(tag.title)


        serialized_article = {
            "title": article.title,
            "published_at": article.published_at,
            "channel": article.channel.title,
            "text": article.text,
            "tags": tags_data
        }
        serialized_articles.append(serialized_article)
    serialized_dataset = {'related_news': [serialized_articles]}

    return JsonResponse(serialized_dataset, json_dumps_params={'ensure_ascii': False})


def show_all_news(request):
    articles = Article.objects.all().order_by('-published_at')

    serialized_articles = []
    for article in articles:
        tags_data = []
        if article.tags:
            tags = Tag.objects.filter(articles=article)
            for tag in tags:
                tags_data.append(tag.title)


        serialized_article = {
            "title": article.title,
            "published_at": article.published_at,
            "channel": article.channel.title,
            "text": article.text,
            "tags": tags_data
        }
        serialized_articles.append(serialized_article)
    serialized_dataset = {'related_news': [serialized_articles]}

    return JsonResponse(serialized_dataset, json_dumps_params={'ensure_ascii': False})