from django.db import models
#from tinymce.models import HTMLField
from pathlib import Path
from django.utils import timezone
# Create your models here


class Channel(models.Model):
    title = models.CharField('Новостной канал', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    def __str__(self):
        return self.title

class Tag(models.Model):
    title = models.CharField('Название тэга', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.title

class Article(models.Model):
    title = models.CharField('Заголовок статьи', max_length=200, unique=True)
    published_at = models.DateField(
        'Дата публикации',
        blank=True,
        db_index=True)

    text = models.TextField('Текст статьи', blank=True)
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='articles'
    )

    tags = models.ManyToManyField(Tag,
                                  verbose_name='Статьи',
                                  related_name='articles',
                                  )
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title
