from django.contrib import admin
from .models import Tag, Channel, Article


class ArticleInline(admin.TabularInline):
    model = Article.tags.through

class TagInline(admin.TabularInline):
    model = Tag.articles.through



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    model = Article
    #raw_id_fields = ['tags']
    list_display = ['title', 'text', 'published_at']
    inlines = [TagInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['title', 'articles', 'get_articles']
    inlines = [ArticleInline]

# Register your models here.
