import uuid

from django.contrib.postgres.indexes import GinIndex
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count, Avg, Min, Max
from django.urls import reverse
from django.utils import timezone


class ProductQuerySet(models.QuerySet):
    """QuerySet для модели Product с дополнительными методами фильтрации."""

    def all(self):
        """Возвращает все товары с валидной ценой и датой создания."""
        return (
            self
            .exclude(price__lt = 0)
            .exclude(creation_date__gt = timezone.now())
            .order_by('type', 'name')
        )

    def filter_name_contains(self, name: str):
        """Фильтрует товары по вхождению строки в название."""
        return self.filter(name__contains = name)

    def summary_values(self):
        """Возвращает основные поля товаров в виде словарей."""
        return self.values('id', 'name', 'type', 'price', 'source_url')

    def summary_values_list(self):
        """Возвращает основные поля товаров в виде кортежей."""
        return self.values_list('id', 'name', 'source_url')

    def update_source_url(self, product_id, source_url: str):
        """Обновляет URL источника для товара."""
        return self.filter(id = product_id).update(source_url = source_url)

    def with_images_count(self):
        """Добавляет аннотацию с количеством изображений."""
        return self.annotate(images_count = Count('images', distinct = True))

    def optimized(self):
        """Оптимизирует запрос с prefetch изображений и тегов."""
        return self.prefetch_related('images', 'tags')


class ProductManager(models.Manager.from_queryset(ProductQuerySet)):
    """Manager для модели Product с методами статистики."""

    def stats(self):
        """Возвращает статистику по товарам (средняя/мин/макс цена, количество)."""
        return self.aggregate(
            avg_price = Avg('price'),
            min_price = Min('price'),
            max_price = Max('price'),
            total_products = Count('id')
        )


class Product(models.Model):
    """Модель товара в магазине.

    Attributes:
        id: Уникальный идентификатор товара (UUID).
        type: Категория товара (костюм, фигурка, комиксы).
        name: Название товара.
        slug: URL-friendly идентификатор.
        price: Цена товара в рублях.
        description: Описание товара.
        source_url: Ссылка на источник товара.
        creation_date: Дата добавления товара.
        tags: Теги товара (через промежуточную модель ProductTag).
        remaining: Количество товара на складе.
    """
    PRODUCT_TYPES = (
        ('suit', 'Костюм'),
        ('shape', 'Фигурка'),
        ('comics', 'Комиксы')
    )

    objects = ProductManager()

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)
    type = models.CharField(choices = PRODUCT_TYPES, max_length = 20, verbose_name = 'Категория')
    name = models.CharField(max_length = 50, editable = True, verbose_name = 'Название')
    slug = models.SlugField(max_length = 50, unique = True, null = True, blank = True, verbose_name = 'Slug')
    price = models.IntegerField(editable = True, validators = [MinValueValidator(0), MaxValueValidator(100_000)],
                                verbose_name = 'Цена')
    description = models.CharField(editable = True, max_length = 1000, verbose_name = 'Описание')
    source_url = models.URLField(null = True, blank = True, verbose_name = 'Ссылка на источник')
    creation_date = models.DateTimeField(default = timezone.now, verbose_name = 'Дата создания')
    tags = models.ManyToManyField('Tag', through = 'ProductTag', related_name = 'products', verbose_name = 'Теги')
    remaining = models.IntegerField(null = False, default = 10_000, validators = [MinValueValidator(0)],
                                    verbose_name = 'В наличии')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name', 'creation_date']
        indexes = [
            GinIndex(fields = ['name'], name = 'name_trgm', opclasses = ['gin_trgm_ops'])
        ]

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        """Сохраняет товар с автоматической генерацией slug и source_url.

        При создании нового товара автоматически генерирует slug (из ID)
        и source_url, если они не указаны.

        Args:
            *args: Позиционные аргументы для родительского метода save.
            **kwargs: Именованные аргументы для родительского метода save.
        """
        is_new = self._state.adding

        super().save(*args, **kwargs)

        if is_new:
            update_fields = []

            if not self.slug:
                self.slug = f'{self.id}'
                update_fields.append('slug')

            if not self.source_url:
                self.source_url = f'https://pereulokstore/products/{self.id}/'
                update_fields.append('source_url')

            if update_fields:
                super().save(update_fields = update_fields)

    def get_absolute_url(self):
        """Возвращает абсолютный URL товара.

        Returns:
            str: URL страницы товара.
        """
        return reverse('product-detail', kwargs = {'pk': self.id})
