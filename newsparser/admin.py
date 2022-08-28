from django.contrib import admin
from .models import Tag, Channel, Article


class ArticleInline(admin.TabularInline):
    model = Article.tags.through


class TagInline(admin.TabularInline):
    model = Tag.articles.through


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    model = Article
    list_display = ['title', 'text', 'published_at']
    inlines = [TagInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['title', 'get_articles']
    inlines = [ArticleInline]
