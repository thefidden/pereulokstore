import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.utils import timezone

from api.models.Product import Product


class CartQuerySet(models.QuerySet):
    """QuerySet для модели Cart с методами фильтрации и оптимизации."""

    def user_items(self, user: User):
        """Возвращает товары в корзине конкретного пользователя."""
        return self.filter(user = user)

    def include_total_price(self):
        """Добавляет аннотацию с общей стоимостью (количество × цена)."""
        return self.annotate(total_price = F('amount') * F('product__price'))

    def optimized(self):
        """Оптимизирует запрос с select_related для пользователя и товара."""
        return self.select_related('user', 'product')


class CartManager(models.Manager.from_queryset(CartQuerySet)):
    pass


class Cart(models.Model):
    """Модель корзины покупок пользователя.

    Attributes:
        id: Уникальный идентификатор записи (UUID).
        user: Пользователь-владелец корзины.
        product: Товар в корзине.
        amount: Количество товара.
        creation_date: Дата добавления товара в корзину.
    """
    objects = CartManager()

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False, unique = True)
    user = models.ForeignKey(User, on_delete = models.PROTECT, related_name = 'cart', verbose_name = 'Пользователь')
    product = models.ForeignKey(Product, on_delete = models.PROTECT, verbose_name = 'Товар')
    amount = models.IntegerField(default = 1, verbose_name = 'Количество')
    creation_date = models.DateTimeField(default = timezone.now, verbose_name = 'Дата добавления')

    class Meta:
        verbose_name = 'Товары в корзине пользователей'
        verbose_name_plural = 'Товары в корзине пользователей'
        ordering = ['user__username', 'product__name']

        constraints = [
            models.UniqueConstraint(
                fields = ['user', 'product'],
                name = 'unique_user_product'
            )
        ]

    def __str__(self) -> str:
        return f"Product {self.product.name} in user {self.user.first_name}'s cart"
