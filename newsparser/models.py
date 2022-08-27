from django.db import models
#from tinymce.models import HTMLField
from pathlib import Path
from django.utils import timezone
# Create your models here


class Channel(models.Model):
    title = models.CharField('Новостной канал', max_length=100, unique=True)


class Tag(models.Model):
    title = models.CharField('Название тега', max_length=100, unique=True)


class Article(models.Model):
    title = models.CharField('Заголовок статьи', max_length=200, unique=True)
    created_at = models.DateField(
        'Когда создана статья',
        blank=True,
        db_index=True)

    text = models.TextField('Текст статьи', blank=True)
    channel_tag = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        db_index=True,
        related_name='articles'
    )

    tags = models.ManyToManyField(Tag,
                                  verbose_name='Квартиры в собственности',
                                  related_name='owned_by',
                                  db_index=True,
                                  blank=True
                                  )
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

