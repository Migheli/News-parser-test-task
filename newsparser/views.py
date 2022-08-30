from django.http import JsonResponse
from newsparser.models import Article, Tag


def get_serialized_dataset(articles):
    serialized_articles = [
        {
            "title": article.title,
            "published_at": article.published_at,
            "channel": article.channel.title,
            "text": article.text,
            "tags": [tag.title for tag in Tag.objects.filter(articles=article) if
                     article.tags]
        }
        for article in articles
    ]
    return {'related_news': [serialized_articles]}


def show_news_by_tagname(request, hashtag):
    target_articles = Article.objects.filter(tags__title__contains=hashtag)
    serialized_dataset = get_serialized_dataset(target_articles)
    return JsonResponse(serialized_dataset, json_dumps_params={'ensure_ascii': False})


def show_all_news(request):
    articles = Article.objects.all().order_by('-published_at')
    serialized_dataset = get_serialized_dataset(articles)
    return JsonResponse(serialized_dataset, json_dumps_params={'ensure_ascii': False})