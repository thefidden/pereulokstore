import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.models.Order import Order
from api.models.Product import Product


class OrderProduct(models.Model):
    """Промежуточная модель для связи заказа и товара.

    Attributes:
        id: Уникальный идентификатор записи (UUID).
        order: Заказ, к которому относится товар.
        product: Товар в заказе.
        price: Цена товара на момент создания заказа.
        amount: Количество товара в заказе.
    """
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)

    order = models.ForeignKey(Order, related_name = 'products', on_delete = models.CASCADE, verbose_name = 'Заказ')
    product = models.ForeignKey(Product, on_delete = models.PROTECT, verbose_name = 'Товар')
    price = models.IntegerField(default = 0, validators = [MinValueValidator(0), MaxValueValidator(100_000)],
                                verbose_name = 'Цена')
    amount = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(10)],
                                 verbose_name = 'Количество')

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказов'
