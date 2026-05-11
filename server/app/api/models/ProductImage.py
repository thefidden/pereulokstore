import uuid

from django.db import models

from api.utils import get_product_image_path
from api.models.Product import Product


class ProductImage(models.Model):
    """Модель изображения товара.

    Attributes:
        id: Уникальный идентификатор изображения (UUID).
        product: Товар, к которому относится изображение.
        image: Файл изображения.
    """
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    product = models.ForeignKey(Product, related_name = 'images', on_delete = models.CASCADE, verbose_name = 'Товар')
    image = models.ImageField(upload_to = get_product_image_path, null = True, default = None,
                              verbose_name = 'Изображение')

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'

    def __str__(self) -> str:
        return f'Image for {self.product.name}'
