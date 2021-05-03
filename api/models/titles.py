from datetime import datetime

from django.db import models
from .genres import Genre
from .categories import Category

from django.core.validators import MaxValueValidator


class Title(models.Model):
    name = models.CharField(
        max_length=300,
        blank=False,
        verbose_name='Name',
    )
    year = models.PositiveIntegerField(
        validators=[MaxValueValidator(datetime.now().year)],
        db_index=True,
        verbose_name='Year',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        verbose_name='Genre',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Category',
    )
