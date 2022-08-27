from django.contrib import admin
from .models import Tag, Channel, Article

class ArticleInline(admin.TabularInline):
    model = Article.tags.through


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    raw_id_fields = ['tags']
    list_display = ['title', 'text', 'published_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    raw_id_fields = ['articles']
    list_display = ['title', 'articles']


# Register your models here.
