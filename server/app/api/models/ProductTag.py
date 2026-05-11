from django.db import models

from api.models.Product import Product
from api.models.Tag import Tag


class ProductTag(models.Model):
    """Промежуточная модель для связи Product и Tag.

    Добавляет дополнительные поля к связи многие-ко-многим между
    товарами и тегами (дата добавления, приоритет отображения).

    Attributes:
        product: Товар.
        tag: Тег.
        added_at: Дата и время добавления тега к товару.
        priority: Приоритет отображения тега (больше = выше).
    """
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Товар')
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE, verbose_name = 'Тег')
    added_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата добавления')
    priority = models.IntegerField(default = 0, verbose_name = 'Приоритет отображения')

    class Meta:
        verbose_name = 'Тег товара'
        verbose_name_plural = 'Теги товаров'
        unique_together = [['product', 'tag']]
        ordering = ['-priority', '-added_at']

    def __str__(self) -> str:
        return f'{self.product.name} - {self.tag.name}'
