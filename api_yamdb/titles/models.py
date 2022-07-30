from datetime import datetime as dt

from django.core.exceptions import ValidationError
from django.db import models


def validate_year(year):
    if year > dt.now().year:
        raise ValidationError(
            f'Дата выхода: {year} - больше нынешнего года'
        )


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=256,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=256,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        max_length=256,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_year],
        verbose_name='Дата выхода',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True,
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        null=True,
        default=None,
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name[:15]
