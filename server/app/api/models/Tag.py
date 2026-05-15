from django.db import models


class Tag(models.Model):
    """Модель тега для товаров.

    Используется для маркировки товаров (например: новинка, скидка, популярное).

    Attributes:
        name: Название тега.
        slug: URL-friendly идентификатор тега.
    """
    name = models.CharField(max_length = 50, unique = True, verbose_name = 'Название')
    slug = models.SlugField(max_length = 50, unique = True, blank = True, verbose_name = 'Slug')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        """Сохраняет тег с автоматической генерацией slug.

        Если slug не указан, генерирует его из названия тега.
        Для кириллических названий добавляет уникальный суффикс.

        Args:
            *args: Позиционные аргументы для родительского метода save.
            **kwargs: Именованные аргументы для родительского метода save.
        """
        if not self.slug:
            from django.utils.text import slugify
            import uuid
            # Генерируем slug из имени + уникальный суффикс для кириллицы
            base_slug = slugify(self.name) or f'tag-{uuid.uuid4().hex[:8]}'
            self.slug = base_slug

        super().save(*args, **kwargs)
